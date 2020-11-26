import pandas as pd 
import numpy as np 

df = pd.read_csv("dat.csv")
male_file = open("male_gender_age.txt")
female_file = open("female_gender_age.txt")
female_age = {}
male_age = {}
total_age = {}
total_pop = 0
female_pop = 0
male_pop = 0

for line in male_file:
    brackets = line.split(",")
    brackets[len(brackets) - 1] = brackets[len(brackets) - 1].replace('\n', '')
    pop = 0
    for i in range(1, len(brackets)):
        pop += df[brackets[i]][0]
    male_pop += pop
    total_pop += pop
    male_age[brackets[0]] = pop

for line in female_file:
    brackets = line.split(",")
    brackets[len(brackets) - 1] = brackets[len(brackets) - 1].replace('\n', '')
    pop = 0
    for i in range(1, len(brackets)):
        pop += df[brackets[i]][0]
    female_pop += pop
    total_pop += pop
    female_age[brackets[0]] = pop

for key, value in female_age.items():
    total_age[key] = 0
for key, value in female_age.items():
    total_age[key] += value
for key, value in male_age.items():
    total_age[key] += value

data = open("barnsdell_age_bracket_distr_16.dat", "w")
data.write("age_bracket,percent\n")
for key, value in total_age.items():
    val = value / total_pop
    data.write(str(key) + "," + str(val) + "\n")
data.close()

data = open("barnsdell_gender_fraction_by_age_bracket_16.dat", "w")
data.write("age_bracket,fraction_male,fraction_female\n")
for key, value in female_age.items():
    data.write(str(key) + "," + str(male_age[key] / male_pop) + "," + 
    str(female_age[key] / female_pop) + "\n")
data.close()





