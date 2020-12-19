import csv

all_combinations = [row for row in csv.reader(open("C:/Users/Michael Arena/Desktop/Football/Diversify/test.csv", "r"))]

top_combinations = []

# all_combinations.sort(key=lambda row: row[-10], reverse=True)

# print(all_combinations)

for index, combination in zip(range(len(all_combinations)), all_combinations):
	if not any(map(lambda lineup: len(set(combination[:9]) & set(lineup[:9])) >=4, top_combinations)):
		top_combinations.append(all_combinations.pop(index))



print(len(top_combinations))



with open('Diversification_Output.csv', 'w', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for name in top_combinations:
    	wr.writerow(name)