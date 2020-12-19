import pandas as pd
import random
from Normal_Skewed_Distribution_Data import mean_record, standard_deviation
import csv
import pulp
import numpy as np

file_name = 'C:/Users/Michael Arena/Desktop/Football/Solver_Test.csv'
raw_data = pd.read_csv(file_name,engine="python",index_col=False, header=0, delimiter=",", quoting = 3)

file_name_injuries = 'C:/Users/Michael Arena/Desktop/Football/Injured_Or_Backup.csv'

injured = pd.read_csv(file_name_injuries,engine="python",index_col=False, header=0, delimiter=",", quoting = 3)

player_name = list(raw_data['player'])

salary = dict(zip(player_name,raw_data['salary']))

position = dict(zip(player_name,raw_data['position']))

teams = dict(zip(player_name,raw_data['team']))

versus = dict(zip(player_name,raw_data['Opponent']))

estimated_points = dict(zip(player_name,raw_data['Points']))

def write_csv():
  with open('test.csv', 'a', newline='') as myfile:
       wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
       wr.writerow(names)



std_data = dict()
for name in salary:
    # store current name, salary and position of a single player
    current_name = name
    current_salary = salary.get(name,int(0))
    current_pos = position[name]

    # filter ranges for current position
    ranges = standard_deviation.get(current_pos,'')
    #loop through all keys for current position to examine low and high of range
    for salary_range in ranges:
        test = salary_range.split('-')
        lower_bound = int(test[0])
        upper_bound = int(test[1])


        if lower_bound <= current_salary <= upper_bound:
            std_data[str(name)] = standard_deviation[current_pos][salary_range]

for i in range(1,10):
    print(f'Currently on Loop {i}')
    projection_simulation = dict()

    #Loop through for players name
    for person in estimated_points:
        #get their projected points which will be assumed to be their mean points
        mean_points = float(estimated_points.get(person,person))

        #get their projected standard deviation from player salary
        std_assumption = float(std_data.get(person,person))

        # on a normal distribution, simulate their points
        simulated_points = random.gauss(mean_points, std_assumption)

        #save their simulated points to a dictionary with the player name
        projection_simulation[person] = simulated_points


    # Increase projections of specific players by a specific integer


#force one of these QBs to be stacked in lineup
    Stack_Improve_Players = []

    for increase in Stack_Improve_Players:
        #how much you want to increase the value of players in Improve_Player is int
        projection_simulation[increase] *= 2.25


#slightly improve
    Improve_Players = []

    for improve in Improve_Players:
        #how much you want to increase the value of players in Improve_Player is int
        projection_simulation[improve] *= 1.10


#slightly lower projections
    lower_Players = []

    for lower in lower_Players:
        #how much you want to increase the value of players in Improve_Player is int
        projection_simulation[lower] *= .90


#eliminate players due to injury
    #worsen players is a list of all players in CSV file "Injured or backup"
    Worsen_Players = list(injured['Name'].unique())

    for worse in Worsen_Players:
        if worse in player_name:

            #how much you want to decrease the value of players in Improve_Player is int
            projection_simulation[worse] -= 50  


    header_added = False

    with open('Simulation.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file, lineterminator ='\n')
        if not header_added:
            writer.writerow(['Name', 'Projection', 'Position', 'Team', 'Salary', 'Opponent'])
            header_added = True
        for key, value in projection_simulation.items():
            pos = position[key]
            team = teams[key]
            cost = salary[key]
            opponent = versus[key]
            writer.writerow([key, value, pos, team, cost, opponent])



    file_name = 'C:/Users/Michael Arena/Desktop/Football/Simulation.csv'
    raw_data = pd.read_csv(file_name,engine="python",index_col=False, header=0, delimiter=",", quoting = 3)


    player_ids = raw_data.index
    player_vars = pulp.LpVariable.dicts('player', player_ids, cat='Binary')

    prob = pulp.LpProblem("DFS Optimizer", pulp.LpMaximize)

    prob += pulp.lpSum([raw_data['Projection'][i]*player_vars[i] for i in player_ids])

    ##Total Salary upper:
    prob += pulp.lpSum([raw_data['Salary'][i]*player_vars[i] for i in player_ids]) <= 50000

    ##Total Salary lower:
    prob += pulp.lpSum([raw_data['Salary'][i]*player_vars[i] for i in player_ids]) >= 49800

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



    ###Stack QB with 1 opposing player:
    for qbid in player_ids:
        if raw_data['Position'][qbid] == 'QB':
            prob += pulp.lpSum([player_vars[i] for i in player_ids if
                                raw_data['Team'][i] == raw_data['Opponent'][qbid]] +
                               [-1*player_vars[qbid]]) >= 0


    pulp.pulpTestAll()

    prob.status

    prob.solve()

    # for var in prob.variables():
    #   print(var.varValue)

    raw_data["is_drafted"] = 0.0
    for var in prob.variables():
        # Set is drafted to the value determined by the LP
        raw_data.iloc[int(var.name[7:]),6] = var.varValue # column 11 = is_drafted

    my_team = raw_data[raw_data["is_drafted"] != 0]
    my_team = my_team[["Name","Position","Team","Salary","Projection", "Opponent"]]

    print(my_team.head(10))

    print("Total used amount of salary cap: {}".format(my_team["Salary"].sum()))
    print("Projected points: {}".format(my_team["Projection"].sum().round(1)))

    

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

    write_csv()