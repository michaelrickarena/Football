import pandas as pd
import random
import csv

file_name = 'C:/Users/Michael Arena/Desktop/Football/Solver_Test.csv'
raw_data = pd.read_csv(file_name,engine="python",index_col=False, header=0, delimiter=",", quoting = 3)


player_name = list(raw_data['player'])

salary = dict(zip(player_name,raw_data['salary']))

position = dict(zip(player_name,raw_data['position']))

teams = dict(zip(player_name,raw_data['team']))

versus = dict(zip(player_name,raw_data['Opponent']))

estimated_points = dict(zip(player_name,raw_data['Points']))

risk = dict(zip(player_name, raw_data['Risk']))

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
        projection_simulation[improve] *= .90


#eliminate players due to injury
    #worsen players is a list of all players in CSV file "Injured or backup"
    Worsen_Players = list(injured['Name'].unique())

    for worse in Worsen_Players:
        if worse in player_name:

            #how much you want to decrease the value of players in Improve_Player is int
            projection_simulation[worse] -= 50  

# print(projection_simulation)
header_added = False

with open('Simulation.csv', 'w') as csv_file:  
    writer = csv.writer(csv_file, lineterminator ='\n')
    if not header_added:
        writer.writerow(['Name', 'Projection', 'Position', 'Team', 'Salary', 'Opponent', 'Risk'])
        header_added = True
    for key, value in projection_simulation.items():
        pos = position[key]
        team = teams[key]
        cost = salary[key]
        opponent = versus[key]
        std = risk[key]
        writer.writerow([key, value, pos, team, cost, opponent, std])