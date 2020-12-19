from pulp import *
import pandas as pd
import numpy as np

file_name = 'C:/Users/Michael Arena/Desktop/Football/Simulation.csv'
raw_data = pd.read_csv(file_name,engine="python",index_col=False, header=0, delimiter=",", quoting = 3)

QBs = raw_data.loc[raw_data['Position']=='QB']
not_QBs = raw_data.loc[raw_data['Position']!='QB']

print(QBs.head())

teams = raw_data.Team.unique()
opponent = raw_data.Opponent.unique()


# we fill a dictionary that, for each team, stores a list of the players on that team.
QBs_from_team = {team: list(QBs[QBs['Team']==team]['Name']) for team in teams}
not_QBs_from_team = {team: list(not_QBs[not_QBs['Team']==team]['Name']) for team in teams}

print(QBs_from_team)


#create new columns that has binary numbers if player == a specific position
raw_data["RB"] = (raw_data["Position"] == 'RB').astype(float)
raw_data["WR"] = (raw_data["Position"] == 'WR').astype(float)
raw_data["QB"] = (raw_data["Position"] == 'QB').astype(float)
raw_data["TE"] = (raw_data["Position"] == 'TE').astype(float)
raw_data["DST"] = (raw_data["Position"] == 'DST').astype(float)
raw_data["Salary"] = raw_data["Salary"].astype(float)

# print(raw_data.head())

model = pulp.LpProblem("Draft Kings", pulp.LpMaximize)

#create dictionaries for each parameter 
total_points = {}
cost = {}
QBs = {}
RBs = {}
WRs = {}
TEs = {}
DST = {}
number_of_players = {}

# i = row index, player = player attributes
for i, player in raw_data.iterrows():
    var_name = 'x' + str(i) # Create variable name
    decision_var = pulp.LpVariable(var_name, cat='Binary') # Initialize Variables

    total_points[decision_var] = player["Projection"] # Create Projection Dictionary
    cost[decision_var] = player["Salary"] # Create Cost Dictionary
    
    # Create Dictionary for Player Types
    QBs[decision_var] = player["QB"]
    RBs[decision_var] = player["RB"]
    WRs[decision_var] = player["WR"]
    TEs[decision_var] = player["TE"]
    DST[decision_var] = player["DST"]
    number_of_players[decision_var] = 1.0
# print(total_points)
# print('---------------')
# print(cost)
# print('---------------')
# print(QBs)
# print('---------------')
# print(RBs)
# print('---------------')
# print(WRs)
# print('---------------')
# print(TEs)
# print('---------------')
# print(DST)
# print('---------------')
# print(number_of_players)
# print('---------------')

#LP CONSTRAINT!!!**************



# Define ojective function and add it to the model
objective_function = pulp.LpAffineExpression(total_points,)
model += objective_function

#Define cost constraint and add it to the model
total_cost = pulp.LpAffineExpression(cost)
model += (total_cost <= 50000)
model += (total_cost >= 49800)


# Add player type constraints
QB_constraint = pulp.LpAffineExpression(QBs)
RB_constraint = pulp.LpAffineExpression(RBs)
WR_constraint = pulp.LpAffineExpression(WRs)
TE_constraint = pulp.LpAffineExpression(TEs)
DST_constraint = pulp.LpAffineExpression(DST)
# DST_op_constraint = pulp.LpAffineExpression(DST_constraint)
#DST has an opponent value, no1 in the 8 other players can have that opponent value as their team value
total_players = pulp.LpAffineExpression(number_of_players)



for team in teams:
	model += pulp.lpSum(QB_constraint[player] for player in QBs_from_team[team]) <= 3
	pulp.lpSum(total_players[player] for player in not_QBs_from_team[team])


model += (QB_constraint == 1)
model += (RB_constraint <= 3)
model += (RB_constraint >= 2)
model += (WR_constraint <= 4)
model += (WR_constraint >= 3)
model += (TE_constraint <= 2)
model += (TE_constraint >= 1)
model += (DST_constraint == 1)
model += (total_players == 9)

# pulp.pulpTestAll()

# model.status

# model.solve()

raw_data["is_drafted"] = 0.0
for var in model.variables():
    # Set is drafted to the value determined by the LP
    raw_data.iloc[int(var.name[1:]),11] = var.varValue # column 11 = is_drafted

my_team = raw_data[raw_data["is_drafted"] == 1.0]
my_team = my_team[["Name","Position","Team","Salary","Projection", "Opponent"]]

# print(my_team.head(10))

# print("Total used amount of salary cap: {}".format(my_team["Salary"].sum()))
# print("Projected points: {}".format(my_team["Projection"].sum().round(1)))


'''
#DST's Team cannot be facing anyone else in the list
#QB must have 2 other players on his team in the list
#1 player must be playing against the QB
'''