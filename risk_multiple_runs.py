import pandas as pd
import random
import csv
import pulp
import numpy as np
from time import sleep

#select a stack of 2 or a stack of one players on the team of QB
#IMPORTANT SELECT
#number of loops
number_of_lineups = 25000
#number of stacks
number_of_stacks = 2

#salary upper and lower bound constraints
Salary_Limit = 50000
Salary_Minimum = 49900
#SELECT THESE ABOVE

#number of stacks is the amount of WR's or TE's you want on the same team as the quartback. due to 9 positions, you can have 9 players on dif teams, this will change based off how many stacked
teams_chosen_from = 0
if number_of_stacks == 2:
    #7 teams as 1 stack of 3 and everyone else on a different team
    teams_chosen_from = 7
elif number_of_stacks == 1:
    teams_chosen_from = 8

#pull in the file that has player projections, risk and team data
file_name = 'C:/Users/Michael Arena/Desktop/Football/Solver_Test.csv'
#put this data into a dataframe
raw_data = pd.read_csv(file_name,engine="python",index_col=False, header=0, delimiter=",", quoting = 3)

#if a player is injured and you never want them in a lineup, add their name to this CSV
file_name_injuries = 'C:/Users/Michael Arena/Desktop/Football/Injured_Or_Backup.csv'
injured = pd.read_csv(file_name_injuries,engine="python",index_col=False, header=0, delimiter=",", quoting = 3)


#pair data with player name and factors that you want to examine in the algorithm
player_name = list(raw_data['player'])

salary = dict(zip(player_name,raw_data['salary']))

position = dict(zip(player_name,raw_data['position']))

teams = dict(zip(player_name,raw_data['team']))

versus = dict(zip(player_name,raw_data['Opponent']))

risk = dict(zip(player_name,raw_data['Risk']))

estimated_points = dict(zip(player_name,raw_data['Points']))

ownership = dict(zip(player_name,raw_data['Ownership']))


#loop begins for the algorithm
for i in range(1,number_of_lineups):
    #show how many loops have been iterated through
    if i % 5 == 0:
        print(f'Currently on Loop {i}')

    #create a dictionary that will contain the simulated points of each player through the upcoming normal distribution
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


    #this below is to change player projections if you want more or less exposure to certain players rather than going into the CSV file and changing it manually

    if i <= 5000:
        Stack_Improve_Players = []
    if i <= 10000:
        Stack_Improve_Players = []
    if i <= 15000:
        Stack_Improve_Players = []
    if i <= 20000:
        Stack_Improve_Players = []
    if i <= 25000:
        Stack_Improve_Players = []

    for increase in Stack_Improve_Players:
        #how much you want to increase the value of players in Improve_Player is int
        projection_simulation[increase] *= 10


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


    #eliminate players due to injury
        #worsen players is a list of all players in CSV file "Injured or backup"
    Worsen_Players = list(injured['Name'].unique())

    for worse in Worsen_Players:
        if worse in player_name:

            #how much you want to decrease the value of players in Improve_Player is int
            projection_simulation[worse] -= 500 



    #create a replica of the Solver_test file with simulated points which will then run through a linear optimization.
    #try and except is needed as sometimes the script tries to write the data too quickly and there is a permission error
    header_added = False
    try:
        with open('Simulation.csv', 'w') as csv_file:  
            writer = csv.writer(csv_file, lineterminator ='\n')
            if not header_added:
                writer.writerow(['Name', 'Projection', 'Position', 'Team', 'Salary', 'Opponent', 'Risk', 'Ownership'])
                header_added = True
            #get key, which is player names that have been simulated in Projection simulation
            for key, value in projection_simulation.items():
                #use key to get position from paired data at top of script
                pos = position[key]
                # get team
                team = teams[key]
                #get salary
                cost = salary[key]
                #get opponent
                opponent = versus[key]
                #get the standard deviation or risk
                std = risk[key]
                #get ownership
                own = ownership[key]
                #write this all to a new file that will go through a linear optimization
                writer.writerow([key, value, pos, team, cost, opponent, std, own])
    except:
        #take a small break and try again if there was a permission error
        sleep(10)
        with open('Simulation.csv', 'w') as csv_file:  
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
    file_name = 'C:/Users/Michael Arena/Desktop/Football/Simulation.csv'
    raw_data = pd.read_csv(file_name,engine="python",index_col=False, header=0, delimiter=",", quoting = 3)


    #list of teams, unique teams and players in each team
    organizations = raw_data['Team']  # t_i
    unique_teams = organizations.unique()  # t_j
    player_in_team = organizations.str.get_dummies()  # t_{ij}


    team_vars = pulp.LpVariable.dicts('team', unique_teams, cat='Binary')  # y_j


    player_ids = raw_data.index
    player_vars = pulp.LpVariable.dicts('player', player_ids, cat='Binary')

    prob = pulp.LpProblem("DFS Optimizer", pulp.LpMaximize)

    prob += pulp.lpSum([raw_data['Projection'][i]*player_vars[i] for i in player_ids])

    ##Total Salary upper:
    prob += pulp.lpSum([raw_data['Salary'][i]*player_vars[i] for i in player_ids]) <= Salary_Limit

    ##Total Salary lower:
    prob += pulp.lpSum([raw_data['Salary'][i]*player_vars[i] for i in player_ids]) >= Salary_Minimum

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
                               [-number_of_stacks*player_vars[qbid]]) >= 0

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
                                (raw_data['Team'][i] == raw_data['Opponent'][qbid] and 
                                raw_data['Position'][i] in ('WR', 'TE'))]+
                               [-1*player_vars[qbid]]) >= 0


    #number of unique teams is teams_Chosen_from
    for team in unique_teams:
      prob += pulp.lpSum(
          [player_in_team[team][i] * player_vars[i] for i in player_ids]
      ) >= team_vars[team]

    prob += pulp.lpSum([team_vars[t] for t in unique_teams]) >= teams_chosen_from


    prob.solve()

    #everything below is organization of the output and writing it to a CSV file
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
      with open('output.csv', 'a', newline='') as myfile:
           wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
           wr.writerow(names)
    
    try:
        write_csv()
    except:
        sleep(10)
        write_csv()