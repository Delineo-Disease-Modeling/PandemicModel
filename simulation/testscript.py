#Test Script to run sim
import matplotlib.pyplot as plt
from master import MasterController as mc
import statistics
import numpy as np


numRuns = int(input("enter number of runs: "))
runsTotal = []
runsFacilities = []
runsHouses = []
runsPeople = {}
for i in range(numRuns):
    infecTotal = []
    currRun = mc()
    currRun.loadVisitMatrix('Anytown_Jan06_fullweek_dict.pkl')
    interventions = {}
    currRun.WellsRiley(True, 61, interventions)  
    
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

colors = ['r','b','g','m']

for i in range(len(runsTotal)):
	plt.plot(runsTotal[i],colors[i%4])
plt.xlabel('hours')
plt.ylabel('total infected')
plt.title('Test Run for Total Infected')
plt.show()
#runsTotal = np.array(runsTotal)
# ave, var, st dev calculations
ave_runsTotal = []
var_runsTotal = []
stdev_runsTotal = []
for i in range(len(runsTotal)):
    ave_runsTotal.append(statistics.mean(runsTotal[i]))
    var_runsTotal.append(statistics.pvariance(runsTotal[i], ave_runsTotal[i]))
    stdev_runsTotal.append(statistics.pstdev(runsTotal[i]))
print('Total infections statstics:')
print('Average:', ave_runsTotal)
print('Variance:', var_runsTotal)
print('Standard deviation:', stdev_runsTotal)



plt.figure()
#Facilities graph
for i in range(len(runsFacilities)):
	plt.plot(runsFacilities[i],colors[i%4])
plt.xlabel('hours')
plt.ylabel('infected in Facilities')
plt.title('Test Run for Infected in Facilities')
plt.show() 
# ave, var, st dev calculations
ave_runsFacilities = []
var_runsFacilities = []
stdev_runsFacilities = []
for i in range(len(runsFacilities)):
    ave_runsFacilities.append(statistics.mean(runsFacilities[i]))
    var_runsFacilities.append(statistics.pvariance(runsFacilities[i], ave_runsFacilities[i]))
    stdev_runsFacilities.append(statistics.pstdev(runsFacilities[i]))
print('Infections in facilities statistics:')
print('Average:', ave_runsFacilities)
print('Variance:', var_runsFacilities)
print('Standard deviation:', stdev_runsFacilities)



plt.figure()
#Households Graph
for i in range(len(runsHouses)):
	plt.plot(runsHouses[i],colors[i%4])
plt.xlabel('hours')
plt.ylabel('infected in households')
plt.title('Test Run for Infected in Households')
plt.show()
# ave, var, st dev calculations
ave_runsHouses = []
var_runsHouses = []
stdev_runsHouses = []
for i in range(len(runsHouses)):
    ave_runsHouses.append(statistics.mean(runsHouses[i]))
    var_runsHouses.append(statistics.pvariance(runsHouses[i], ave_runsHouses[i]))
    stdev_runsHouses.append(statistics.pstdev(runsHouses[i]))
print('Infection in households statistics:')
print('Average:', ave_runsHouses)
print('Variance:', var_runsHouses)
print('Standard deviation:', stdev_runsHouses)




runsPeople = currRun.peopleInFacilities
plt.figure()
#People in Facilities Graph
for i in range(len(runsPeople)):
    plt.plot(hours, runsPeople[i],colors[i%4])
    break

plt.xlabel('hours')
plt.ylabel('People in facilities')
plt.title('Test Run for people in facilities')
plt.show()