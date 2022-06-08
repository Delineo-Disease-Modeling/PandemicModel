#Test Script to test simulation locally. First runs the simulation then several generates plots of the results.
#Plots for: Total Infected, Number infected in a Facility, Number infected in a house, and a plot representing the distribution of all runs.

import matplotlib.pyplot as plt
from master import MasterController as mc


import numpy as np
import scipy.stats as stats
import statistics
import math



numRuns = int(input("enter number of runs: "))
runsTotal = [] # how many runs should be ran?
runsFacilities = [] #what facilities should be used?
runsHouses = [] #what homes should be used?
value = input('any interventions? y or n ') #should we use interventions?
interventions = {}

while value != 'n':
    a = input('Enter intervention: ') #TODO: give a list of interventions that can be used
    b = int(input("Enter magnitude of intervention: "))
    interventions[a] = b
    value = input('would you like to add another intervention, y or n? ') # if yes, repeat the above process for each intervention

for i in range(numRuns): # run the simulation numRuns times
    infecTotal = []
    currRun = mc()
    currRun.loadVisitMatrix('Anytown_Jan06_fullweek_dict.pkl')
    currRun.run_simulation(city='Anytown', print_infection_breakdown=True, isAnytown=True, num_days=61, interventions=interventions)  
    
    for (i1, i2) in zip(currRun.infecFacilitiesTot, currRun.infecHousesTot):
        infecTotal.append(i1+i2+10)

    runsTotal.append(list(infecTotal)) # add the total number of infections for each day to the list of runs
    runsFacilities.append(list(currRun.infecFacilitiesTot)) 
    runsHouses.append(list(currRun.infecHousesTot))
    currRun.infecFacilitiesTot = []
    currRun.infecHousesTot = []

#Create Total Infected Graph
hours = []
for i in range(len(runsTotal[0])):
    hours.append(i)
plt.figure()

colors = ['r','b','g','m','y','k','c'] # colors for the different runs
for i in range(len(runsTotal)):
	plt.plot(runsTotal[i],colors[i%7])
plt.xlabel('hours')
plt.ylabel('total infected')
plt.title('Test Run for Total Infected')
plt.show()

plt.figure()
#Facilities graph
for i in range(len(runsFacilities)):
	plt.plot(runsFacilities[i],colors[i%7])
plt.xlabel('hours')
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





