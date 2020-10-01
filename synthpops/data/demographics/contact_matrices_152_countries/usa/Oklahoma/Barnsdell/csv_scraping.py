# Get user input on which data to scrape e.g. age, sex, race etc.
# Move into the folder and get the file
# Read csv format and translate table ID using .json file
# Create a .dat file containing all distribution brackets
# Format data as [bracket], [percentage] and output to a .dat file

import csv
import json

type = input("Demographic type: ")
if type == "age" or type == "sex":
    csv = "age_sex_distr.csv"
    json = "age_sex_metada.json"
elif type == "race":
    csv = "race_distr.csv"
    json = "race_metadata.json"
elif type == "income":
    csv = "income_distr.csv"
    json = "income_metadata.json"

# Open json file and populate a dictionary of table IDs
# Read csv file based on dictionary