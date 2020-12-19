import pandas as pd
file_name = "New_Diversification_Output.csv"
file_name_output = "Upload_output.csv"

df = pd.read_csv(file_name, sep=",", engine ='python', header = None)

df.drop_duplicates(subset=None, inplace = True)

# Write the results to a different file
df.to_csv(file_name_output, index=False, header = None)


with open(file_name_output) as f:
	entries = sum(1 for line in f)
print(entries)