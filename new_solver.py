import pulp
import pandas as pd
import numpy as np
from itertools import chain
import csv

file_name = 'C:/Users/Michael Arena/Desktop/Football/Simulation.csv'
raw_data = pd.read_csv(file_name,engine="python",index_col=False, header=0, delimiter=",", quoting = 3)


teams = raw_data['Team']  # t_i
unique_teams = teams.unique()  # t_j
player_in_team = teams.str.get_dummies()  # t_{ij}


team_vars = pulp.LpVariable.dicts('team', unique_teams, cat='Binary')  # y_j

player_ids = raw_data.index
player_vars = pulp.LpVariable.dicts('player', player_ids, cat='Binary')

prob = pulp.LpProblem("DFS Optimizer", pulp.LpMaximize)

prob += pulp.lpSum([raw_data['Projection'][i]*player_vars[i] for i in player_ids])

##Total Salary upper:
prob += pulp.lpSum([raw_data['Salary'][i]*player_vars[i] for i in player_ids]) <= 50000

##Total Salary lower:
prob += pulp.lpSum([raw_data['Salary'][i]*player_vars[i] for i in player_ids]) >= 49900

##Exactly 9 players:
prob += pulp.lpSum([player_vars[i] for i in player_ids]) == 9

##2-3 RBs:
prob += pulp.lpSum([player_vars[i] for i in player_ids if raw_data['Position'][i] == 'RB']) >= 2
prob += pulp.lpSum([player_vars[i] for i in player_ids if raw_data['Position'][i] == 'RB']) <= 3

##1 QB:
prob += pulp.lpSum([player_vars[i] for i in player_ids if raw_data['Position'][i] == 'QB']) == 1
##3-4 WRs:
prob += pulp.lpSum([player_vars[i] for i in player_ids if raw_data['Position'][i] == 'WR']) >= 3
prob += pulp.lpSum([player_vars[i] for i in player_ids if raw_data['Position'][i] == 'WR']) <= 4

##1-2 TE's:
prob += pulp.lpSum([player_vars[i] for i in player_ids if raw_data['Position'][i] == 'TE']) == 1
# prob += pulp.lpSum([player_vars[i] for i in player_ids if raw_data['Position'][i] == 'TE']) <= 2

##1 DST:
prob += pulp.lpSum([player_vars[i] for i in player_ids if raw_data['Position'][i] == 'DST']) == 1

##At least 3 people of high ownership:
prob += pulp.lpSum([player_vars[i] for i in player_ids if raw_data['Ownership'][i] == 'High']) >=6

##No more than 2 very low ownerships players:
prob += pulp.lpSum([player_vars[i] for i in player_ids if raw_data['Ownership'][i] == 'Very Low']) <=1


###Stack QB with 2 teammates
for qbid in player_ids:
    if raw_data['Position'][qbid] == 'QB':
        prob += pulp.lpSum([player_vars[i] for i in player_ids if 
                          (raw_data['Team'][i] == raw_data['Team'][qbid] and 
                            raw_data['Position'][i] in ('WR', 'TE'))] + 
                            [-2*player_vars[qbid]]) >= 0

###Don't stack with opposing DST:
for dstid in player_ids:
    if raw_data['Position'][dstid] == 'DST':
        prob += pulp.lpSum([player_vars[i] for i in player_ids if
                            raw_data['Team'][i] == raw_data['Opponent'][dstid]] +
                            [8*player_vars[dstid]]) <= 8



##Stack QB with 1 opposing player:
for qbid in player_ids:
    if raw_data['Position'][qbid] == 'QB':
        prob += pulp.lpSum([player_vars[i] for i in player_ids if
                            (raw_data['Team'][i] == raw_data['Opponent'][qbid] and 
                            raw_data['Position'][i] in ('WR', 'TE'))]+
                            [-1*player_vars[qbid]]) >= 0


for team in unique_teams:
  prob += pulp.lpSum(
      [player_in_team[team][i] * player_vars[i] for i in player_ids]
  ) >= team_vars[team]

prob += pulp.lpSum([team_vars[t] for t in unique_teams]) >= 7


prob.solve()

lineup = {}
raw_data["is_drafted"] = 0.0
for idx in player_vars:
    if player_vars[idx].varValue:
        raw_data.loc[idx,"is_drafted"] = 1




my_team = raw_data[raw_data["is_drafted"] != 0]
my_team = my_team[["Name","Position","Team","Salary","Projection", "Opponent"]]

print(my_team.head(10))

print("Total used amount of salary cap: {}".format(my_team["Salary"].sum()))
print("Projected points: {}".format(my_team["Projection"].sum().round(1)))



print(my_team["Projection"].sum().round(1))

#get names of QB in Team
qb = my_team['Position'] == 'QB'

qb_data = my_team[qb]

qb_name = list(qb_data['Name'].unique())

#get names of RB's in team
rb = my_team['Position'] == 'RB'

rb_data = my_team[rb]

rb_name = list(rb_data['Name'].unique())

#get names of WR's in team
wr = my_team['Position'] == 'WR'

wr_data = my_team[wr]

wr_name = list(wr_data['Name'].unique())

#get names of TE's in team
te = my_team['Position'] == 'TE'

te_data = my_team[te]

te_name = list(te_data['Name'].unique())

#get names of DST in team
dst = my_team['Position'] == 'DST'

dst_data = my_team[dst]

dst_name = list(dst_data['Name'].unique())

names = []
if len(wr_name) == 3:
  names.extend(qb_name + rb_name[:2] + wr_name + te_name + [rb_name[-1]] + dst_name)
elif len(wr_name) == 4:
  names.extend(qb_name + rb_name + wr_name[:3] + te_name + [wr_name[-1]] + dst_name)

projected_points = my_team["Projection"].sum().round(1)
names.append(projected_points)
print(names)

def write_csv():
  with open('test2.csv', 'a', newline='') as myfile:
       wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
       wr.writerow(names)
# write_csv()