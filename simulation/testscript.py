#Test Script to run sim
import matplotlib.pyplot as plt
from master import MasterController as mc


numRuns = int(input("enter number of runs: "))
runsTotal = []
runsFacilities = []
runsHouses = []
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

plt.figure()
#Facilities graph
for i in range(len(runsFacilities)):
	plt.plot(runsFacilities[i],colors[i%4])
plt.xlabel('hours')
plt.ylabel('infected in Facilities')
plt.title('Test Run for Infected in Facilities')
plt.show()

plt.figure()
#Households Graph
for i in range(len(runsHouses)):
	plt.plot(runsHouses[i],colors[i%4])
plt.xlabel('hours')
plt.ylabel('infected in facilities')
plt.title('Test Run for Infected in Households')
plt.show()





