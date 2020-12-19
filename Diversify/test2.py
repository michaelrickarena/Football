import csv

all_combinations = [row for row in csv.reader(open("C:/Users/Michael Arena/Desktop/Football/Diversify/test.csv", "r"))]

top_combinations = []

all_combinations.sort(key=lambda row: row[-1], reverse=True)

for index, combination in zip(range(len(all_combinations)), all_combinations):
	if not any(map(lambda lineup: len(set(combination[:9]) & set(lineup[:9])) >=5, top_combinations)):
		top_combinations.append(all_combinations.pop(index))

print(top_combinations)

