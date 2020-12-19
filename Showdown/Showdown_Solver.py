import pulp
import pandas as pd
import numpy as np
from itertools import chain
import csv

file_name = 'C:/Users/Michael Arena/Desktop/Football/Simulation.csv'
raw_data = pd.read_csv(file_name,engine="python",index_col=False, header=0, delimiter=",", quoting = 3)

player_ids = raw_data.index
player_vars = pulp.LpVariable.dicts('player', player_ids, cat='Binary')


prob = pulp.LpProblem("DFS Optimizer", pulp.LpMaximize)

prob += pulp.lpSum([raw_data['Projection'][i]*player_vars[i] for i in player_ids])

##Total Salary upper:
prob += pulp.lpSum([raw_data['Salary'][i]*player_vars[i] for i in player_ids]) <= 50000

##Total Salary lower:
prob += pulp.lpSum([raw_data['Salary'][i]*player_vars[i] for i in player_ids]) >= 47500

##Exactly 6 players:
prob += pulp.lpSum([player_vars[i] for i in player_ids]) == 6

## 5 Flex:
prob += pulp.lpSum([player_vars[i] for i in player_ids if raw_data['Position'][i] == 'FLEX']) >= 5

##1 Captain:
prob += pulp.lpSum([player_vars[i] for i in player_ids if raw_data['Position'][i] == 'CPT']) == 1


pulp.pulpTestAll()

prob.status

prob.solve()


raw_data["is_drafted"] = 0.0
for var in prob.variables():
    # Set is drafted to the value determined by the LP
    raw_data.iloc[int(var.name[7:]),7] = var.varValue # column 11 = is_drafted


my_team = raw_data[raw_data["is_drafted"] != 0]
my_team = my_team[["Name","Position","Team","Salary","Projection", "Opponent"]]

print(my_team.head(10))

print("Total used amount of salary cap: {}".format(my_team["Salary"].sum()))
print("Projected points: {}".format(my_team["Projection"].sum().round(1)))



print(my_team["Projection"].sum().round(1))