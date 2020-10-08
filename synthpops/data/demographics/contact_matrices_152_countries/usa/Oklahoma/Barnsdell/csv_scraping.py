# Get user input on which data to scrape e.g. age, sex, race etc.
# Move into the folder and get the file
# Read csv format and translate table ID using .json file
# Create a .dat file containing all distribution brackets
# Format data as [bracket], [percentage] and output to a .dat file

import pandas as pd

fage_identifiers = open("female_age_identifiers.txt", mode = 'r')
mage_identifiers = open("male_age_identifiers.txt", mode = 'r')
age_sex_distr = pd.read_csv("age_sex_distr.csv", index_col = 0)

age_distribution = []
for identifier in fage_identifiers:
