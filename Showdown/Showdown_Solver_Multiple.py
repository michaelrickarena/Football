import pulp
import pandas as pd
import numpy as np
from itertools import chain
import csv
import random

def write_csv():
  with open('C:/Users/Michael Arena/Desktop/Football/Showdown/output.csv', 'a', newline='') as myfile:
       wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
       wr.writerow(output)

Number_of_Loops = 5000

for i in range(1, Number_of_Loops):

    file_name = 'C:/Users/Michael Arena/Desktop/Football/Showdown/Solver_Showdown.csv'
    raw_data = pd.read_csv(file_name,engine="python",index_col=False, header=0, delimiter=",", quoting = 3)


    player_name = list(raw_data['Name'])

    salary = dict(zip(player_name,raw_data['Salary']))

    position = dict(zip(player_name,raw_data['Position']))

    teams = dict(zip(player_name,raw_data['Team']))

    versus = dict(zip(player_name,raw_data['Opponent']))

    risk = dict(zip(player_name,raw_data['Risk']))

    estimated_points = dict(zip(player_name,raw_data['Points']))

    ownership = dict(zip(player_name,raw_data['Ownership']))



    if i % 100 == 0:
        print(f'Currently on Loop {i}')
    projection_simulation = dict()

    #Loop through for players name
    for person in estimated_points:
        #get their projected points which will be assumed to be their mean points
        mean_points = float(estimated_points.get(person,person))

        #get their projected standard deviation from player salary
        std_assumption = float(risk.get(person,person))

        # on a normal distribution, simulate their points
        simulated_points = random.gauss(mean_points, std_assumption)

        #save their simulated points to a dictionary with the player name
        projection_simulation[person] = simulated_points



#slightly improve
    Improve_Players = []

    for improve in Improve_Players:
        #how much you want to increase the value of players in Improve_Player is int
        projection_simulation[improve] *= 1.15


#slightly lower projections
    lower_Players = []

    for lower in lower_Players:
        #how much you want to increase the value of players in Improve_Player is int
        projection_simulation[lower] *= .85


    Worsen_Players = []

    for worse in Worsen_Players:
        if worse in player_name:

            #how much you want to decrease the value of players in Improve_Player is int
            projection_simulation[worse] -= 500 




    header_added = False
    try:
        with open('Simulation_Showdown.csv', 'w') as csv_file:  
            writer = csv.writer(csv_file, lineterminator ='\n')
            if not header_added:
                writer.writerow(['Name', 'Projection', 'Position', 'Team', 'Salary', 'Opponent', 'Risk', 'Ownership'])
                header_added = True
            for key, value in projection_simulation.items():
                pos = position[key]
                team = teams[key]
                cost = salary[key]
                opponent = versus[key]
                std = risk[key]
                own = ownership[key]
                writer.writerow([key, value, pos, team, cost, opponent, std, own])
    except:
        sleep(10)
        with open('Simulation_Showdown.csv', 'w') as csv_file:  
            writer = csv.writer(csv_file, lineterminator ='\n')
            if not header_added:
                writer.writerow(['Name', 'Projection', 'Position', 'Team', 'Salary', 'Opponent', 'Risk', 'Ownership'])
                header_added = True
            for key, value in projection_simulation.items():
                pos = position[key]
                team = teams[key]
                cost = salary[key]
                opponent = versus[key]
                std = risk[key]
                own = ownership[key]
                writer.writerow([key, value, pos, team, cost, opponent, std, own])

    file_name = 'C:/Users/Michael Arena/Desktop/Football/Showdown/Simulation_Showdown.csv'
    df = pd.read_csv(file_name,engine="python",index_col=False, header=0, delimiter=",", quoting = 3)

    captains = df.loc[df['Position'] == 'CPT']	
    flex = df.loc[df['Position'] == 'FLEX']


    captains['Name'] = captains['Name'].str.rstrip()


    df2 = captains.append(flex, ignore_index = True)

    df2.to_csv('C:/Users/Michael Arena/Desktop/Football/Showdown/Simulation_Showdown_cleaned.csv', index= False)



    data_file = 'C:/Users/Michael Arena/Desktop/Football/Showdown/Simulation_Showdown_cleaned.csv'
    df = pd.read_csv(data_file, index_col=['Name', 'Position', 'Ownership'], skipinitialspace=True)

    # df.Name = df.Name.str.rstrip()



    legal_assignments = df.index   # tuples of (name, pos)
    name_set = df.index.unique(0)  # a conveniece


    costs = df['Salary'].to_dict()
    values = df['Projection'].to_dict()

	# set up LP
    draft = pulp.LpVariable.dicts('selected', legal_assignments, cat='Binary')

    prob = pulp.LpProblem('the draft', pulp.LpMaximize)

	# obj
    prob += pulp.lpSum([draft[n, p, o]*values[n,p,o] for (n, p, o) in legal_assignments])

	# salary cap
    prob += pulp.lpSum([draft[n, p, o]*costs[n,p,o] for (n, p, o) in legal_assignments]) >= 46500

    prob += pulp.lpSum([draft[n, p,o]*costs[n,p,o] for (n, p, o) in legal_assignments]) <= 50000

	# pick 5 FLEX
    prob += pulp.lpSum([draft[n, p, o] for (n, p, o) in legal_assignments if p == 'FLEX']) == 5

	# pick 1 CPT
    prob += pulp.lpSum([draft[n, p, o] for (n, p, o) in legal_assignments if p == 'CPT']) == 1

   	# pick 1 CPT
    # prob += pulp.lpSum([draft[n, p, o] for (n, p, o) in legal_assignments if o == 'Low']) <= 2

    # pick 1 CPT
    prob += pulp.lpSum([draft[n, p, o] for (n, p, o) in legal_assignments if o == 'High']) <= 4


	# use each player at most only once
    for name in name_set:
        prob += pulp.lpSum([draft[n, p, o] for (n, p, o) in legal_assignments if n == name]) <=1


    prob.solve()

    lineup = {}
    for idx in draft:
        if draft[idx].varValue:
            lineup[f'{idx[0]}'] = idx[1]
	        # print(f'hire {idx[0]} for position {idx[1]}')

    lineup = {k: v for k, v in sorted(lineup.items(), key=lambda item: item[1])}
    print(lineup)

    output = []
    for key in lineup.keys():
        output.append(key)

    write_csv()