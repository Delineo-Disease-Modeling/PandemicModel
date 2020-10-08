# Get user input on which data to scrape e.g. age, sex, race etc.
# Move into the folder and get the file
# Read csv format and translate table ID using .json file
# Create a .dat file containing all distribution brackets
# Format data as [bracket], [percentage] and output to a .dat file

import pandas as pd

fage_identifiers = open("female_age_identifiers.txt", "r")
mage_identifiers = open("male_age_identifiers.txt", "r")
age_sex_distr = pd.read_csv("age_sex_distr.csv", index_col = 0)

age_distr = [0] * 9
fage_distr = [0] * 9
mage_distr = [0] * 9
for index, row in age_sex_distr.iterrows():
    female_pop = row['B01001026']
    male_pop = row['B01001002']
    index = 0
    total_pop = 0
    for age_bracket in fage_identifiers:
        table_id = age_bracket.split(',')
        for id in table_id:
            age_distr[index] += row[id[0:9]]
            fage_distr[index] += row[id[0:9]]
            total_pop += row[id[0:9]]
        index += 1
    index = 0
    for age_bracket in mage_identifiers:
        table_id = age_bracket.split(',')
        for id in table_id:
            age_distr[index] += row[id[0:9]]
            mage_distr[index] += row[id[0:9]]
            total_pop += row[id[0:9]]
        index += 1

fage_identifiers.close()
mage_identifiers.close()

bracket_dict = {0 : "0_9", 1 : "10_19", 2 : "20_29", 3 : "30_39", 4 : "40_49" , 5 : "50_59", 6 : "60_69", 7 : "70_79", 8 : "80_100"}
age_data = open("barnsdell_age_bracket_distr.dat", "w")
age_data.write("age bracket,percent\n")
for bracket in range(9):
    age_data.write(bracket_dict[bracket] + "," + (str)(age_distr[bracket] / total_pop) + "\n")
age_data.close()

gender_data = open("barnsdell_gender_fraction_by_age_bracket.dat", "w")
gender_data.write("age_bracket,fraction_male,fraction_female\n")
for bracket in range(9):
    gender_data.write(bracket_dict[bracket] + "," + (str)(mage_distr[bracket] / age_distr[bracket]) + "," 
    + (str)(fage_distr[bracket] / age_distr[bracket]) + "\n")
gender_data.close()



