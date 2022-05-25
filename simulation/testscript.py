#Test Script to run sim
import matplotlib.pyplot as plt
from master import MasterController as mc


import numpy as np
import scipy.stats as stats
import statistics
import math

numRuns = int(input("enter number of runs: "))
runsTotal = []
runsFacilities = []
runsHouses = []
value = input('any interventions? y or n ')
interventions = {}
while value != 'n':
    a = input('Enter intervention: ')
    b = int(input("Enter magnitude of intervention: "))
    interventions[a] = b
    value = input('would you like to add another intervention, y or n? ')

for i in range(numRuns):
    infecTotal = []
    currRun = mc()
    currRun.loadVisitMatrix('Baltimore_2020-01-01_2020-02-29.pkl')
    currRun.run_simulation(city='Baltimore', print_infection_breakdown=True, isAnytown=True, num_days=61, interventions=interventions)  
    
    for (i1, i2) in zip(currRun.infecFacilitiesTot, currRun.infecHousesTot):
        infecTotal.append(i1+i2+10)
    runsTotal.append(list(infecTotal))
    runsFacilities.append(list(currRun.infecFacilitiesTot))
    runsHouses.append(list(currRun.infecHousesTot))
    currRun.infecFacilitiesTot = []
    currRun.infecHousesTot = []

#Total Infected Graph
hours = []
for i in range(len(runsTotal[0])):
    hours.append(i)
plt.figure()

colors = ['r','b','g','m','y','k','c']
for i in range(len(runsTotal)):
	plt.plot(runsTotal[i],colors[i%7])
plt.xlabel('hours')
plt.ylabel('total infected')
plt.title('Test Run for Total Infected')
plt.show()

def sum_by_day(arr):
    return np.add.reduceat(arr, np.arange(0, len(arr), 24))

plt.figure()
#Facilities graph
runsFacilities_days = np.array(list(map(sum_by_day, runsFacilities)))
for i in range(len(runsFacilities)):
	plt.plot(runsFacilities_days[i],colors[i%7])
plt.xlabel('days')
plt.ylabel('infected in Facilities')
plt.title('Test Run for Infected in Facilities')
plt.show()

plt.figure()
#Households Graph
for i in range(len(runsHouses)):
	plt.plot(runsHouses[i],colors[i%7])
plt.xlabel('hours')
plt.ylabel('infected in facilities')
plt.title('Test Run for Infected in Households')
plt.show()


# Graph to graph distribution of totals

finalCt = []
for i in runsTotal:
    finalCt.append(i[-1])
plt.figure()
plt.hist(finalCt, bins=50, density = True, alpha=0.6, color='g')
# for implementation of a normal curve, need to add density = true to hist if adding curve

avg = statistics.mean(finalCt)
variance = statistics.variance(finalCt)
sigma = math.sqrt(variance)
x = np.linspace(avg - 3*sigma, avg + 3*sigma, 100)
plt.plot(x, stats.norm.pdf(x, avg, sigma))

plt.xlabel('Number of Infected')
plt.ylabel('Count')
plt.title('Distribution of Runs')
plt.show()





