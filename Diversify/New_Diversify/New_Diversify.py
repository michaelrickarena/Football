import pandas as pd
import numpy as np
import csv
import pandas as pd
import numpy as np
from itertools import chain
import random

Number_of_lines = 200

for i in range(1, 5000):

    with open('New_Diversification_Output.csv') as f:
	    entries = sum(1 for line in f)

    if entries > Number_of_lines:
        break

    print(entries)

    file_name = 'C:/Users/Michael Arena/Desktop/Football/Solver_Test.csv'
    raw_data = pd.read_csv(file_name,engine="python",index_col=False, header=0, delimiter=",", quoting = 3)

    player_name = list(raw_data['player'])

    salary = dict(zip(player_name,raw_data['salary']))

    position = dict(zip(player_name,raw_data['position']))

    teams = dict(zip(player_name,raw_data['team']))

    versus = dict(zip(player_name,raw_data['Opponent']))

    risk = dict(zip(player_name,raw_data['Risk']))

    estimated_points = dict(zip(player_name,raw_data['Points']))

    ownership = dict(zip(player_name,raw_data['Ownership']))

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


    header_added = False
    try:
        with open('Diversify_Simulation.csv', 'w') as csv_file:  
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
        with open('Diversify_Simulation.csv', 'w') as csv_file:  
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

	#open up new simulation file just created with player projections on a normal distribution
    file_name = 'C:/Users/Michael Arena/Desktop/Football/Diversify/New_Diversify/Diversify_Simulation.csv'
    raw_data = pd.read_csv(file_name,engine="python",index_col=False, header=0, delimiter=",", quoting = 3)

    player_name = list(raw_data['Name'])

    projected_points = dict(zip(player_name,raw_data['Projection']))


    all_lineups = [row for row in csv.reader(open("C:/Users/Michael Arena/Desktop/Football/Diversify/New_Diversify/New_Test_Diversify.csv", "r"))]

    lineup_projections = []

    for combinations in all_lineups:
        for i in range(1,10):
            if i-1 == 0:
            	lineup_sum = 0
            else:
            	pass
            lineup_sum = lineup_sum + projected_points[combinations[i-1]]
            if i == 9:
            	lineup_projections.append(lineup_sum)


    df2 = pd.read_csv("C:/Users/Michael Arena/Desktop/Football/Diversify/New_Diversify/New_Test_Diversify.csv", header=None)
    df2['9'] = lineup_projections
    df2 = df2.sort_values(by='9', ascending=False)
    df2.to_csv('cleaned_data.csv', index = False, header = False)

    all_combinations = [row for row in csv.reader(open("C:/Users/Michael Arena/Desktop/Football/Diversify/New_Diversify/cleaned_data.csv", "r"))]

    top_combinations = []

    for index, combination in zip(range(len(all_combinations)), all_combinations):
    	if not any(map(lambda lineup: len(set(combination[:9]) & set(lineup[:9])) >=2, top_combinations)):
    		top_combinations.append(all_combinations.pop(index))

    

    with open('New_Diversification_Output.csv', 'a', newline='') as myfile:
    	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    	for name in top_combinations:
    		wr.writerow(name)

