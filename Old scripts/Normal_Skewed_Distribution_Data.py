import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
import math

#read in file
file_name = 'C:/Users/Michael Arena/Desktop/Football/2019_dfs_data.csv'
raw_data = pd.read_csv(file_name,engine="python",index_col=False, header=0, delimiter=";", quoting = 3)

#clean week string and turn it into an int by removing the quotation
raw_data['Week'] = raw_data['Week'].str.replace(r'"', '')
raw_data['Week'] = raw_data['Week'].astype(int)

#clean salary string and turn it into an int by removing the quotation
raw_data['DK salary'] = raw_data['DK salary'].str.replace(r'"$', '')
raw_data['DK salary'] = raw_data['DK salary'].astype(int)

raw_data['Pos'] = raw_data['Pos'].replace({'Def':'DST'})

# print(raw_data[raw_data['Pos'].str.contains("DST")])

#creating conditions
player_played = raw_data['DK points'] >= 0.1
salary_constraint = raw_data['DK salary'] >= 1400

#List of avaiable postions in Dataframe
positions = ['RB', 'WR', 'QB', 'TE', 'DST']

salary_range1 = []
salary_range2 = []
for x_ in range(1500,12600,300):
    salary_range1.append(x_)

for y_ in range(1800,12900,300):
    salary_range2.append(y_)

#Initialize dictonaries to save key variables of mean, std and max for each salary range of each position
mean_record = dict()
max_record = dict()
min_record = dict()
standard_deviation = dict()

#filter through each position in list of positions
for pos in positions:
	#temp dicts to created a nested dictionary
	temp_mean = dict()
	temp_max = dict()
	temp_min = dict()
	temp_std = dict()

	#filter through salary ranges in parallel to apply on each position
	for s, m in zip(salary_range1, salary_range2):
		#Filter for current position being looped through in first for loop
		player_position = raw_data['Pos'] == pos
		#filter pandas dataframe for constraints
		Points_Filter = raw_data.loc[(player_position) & (player_played) & (salary_constraint)]
		#filter pandas dataframe to calc distribution numbers for each salary range
		range_count = Points_Filter.loc[(Points_Filter['DK salary'] <= m) & (Points_Filter['DK salary'] >= s)]

		if math.isnan(range_count['DK points'].mean()):
			pass
		else:
			temp_mean[f'{s}-{m}'] = range_count['DK points'].mean()
		mean_record[pos] = temp_mean


		if math.isnan(range_count['DK points'].max()):
			pass
		else:
			temp_max[f'{s}-{m}'] = range_count['DK points'].max()
		max_record[pos] = temp_max


		if math.isnan(range_count['DK points'].min()):
			pass
		else:
			temp_min[f'{s}-{m}'] = range_count['DK points'].min()
		min_record[pos] = temp_min

		if math.isnan(range_count['DK points'].std()):
			temp_std[f'{s}-{m}'] = 5
		else:
			temp_std[f'{s}-{m}'] = range_count['DK points'].std()
		standard_deviation[pos] = temp_std


# print(f'returning the MAXIMUM DK Points for each salary range using dictonary max_record\n\n {max_record}')
# print('--------------')
# print(f'returning the MINIMUM DK Points for each salary range using dictonary max_record\n\n {min_record}')
# print('--------------')
# print(f'returning the AVERAGE DK Points for each salary range using dictonary mean_record\n\n {mean_record}')
# print('--------------')
# print(f'returning the STANDARD DEVIATION of DK Points for each salary range using dictonary standard_deviation\n\n {standard_deviation}')