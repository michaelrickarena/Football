import pulp
import pandas as pd
import numpy as np
from itertools import chain
import csv


def write_csv():
  with open('test_showdown.csv', 'a', newline='') as myfile:
       wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
       wr.writerow(output)





data_file = 'C:/Users/Michael Arena/Desktop/Football/Showdown/Simulation_Showdown.csv'

df = pd.read_csv(data_file, index_col=['Name', 'Position'], skipinitialspace=True)
#print(df)

legal_assignments = df.index   # tuples of (name, pos)
name_set = df.index.unique(0)  # a conveniece

costs = df['Salary'].to_dict()
values = df['Projection'].to_dict()

# set up LP
draft = pulp.LpVariable.dicts('selected', legal_assignments, cat='Binary')

prob = pulp.LpProblem('the draft', pulp.LpMaximize)

# obj
prob += pulp.lpSum([draft[n, p]*values[n,p] for (n, p) in legal_assignments])

# salary cap
prob += pulp.lpSum([draft[n, p]*costs[n,p] for (n, p) in legal_assignments]) >= 40000

prob += pulp.lpSum([draft[n, p]*costs[n,p] for (n, p) in legal_assignments]) <= 47000

# pick 5 FLEX
prob += pulp.lpSum([draft[n, p] for (n, p) in legal_assignments if p == 'FLEX']) == 5

# pick 1 CPT
prob += pulp.lpSum([draft[n, p] for (n, p) in legal_assignments if p == 'CPT']) == 1

# use each player at most only once
for name in name_set:
    prob += pulp.lpSum([draft[n, p] for (n, p) in legal_assignments if n == name]) <=1


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

print(output)

write_csv()

