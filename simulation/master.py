from person import Person
from module import Module
from submodule import Submodule
import random


class MasterController:
    # MasterController class, this runs the simulation by instantiating module

    state = 'Indiana'
    county = 'Barnsdall'
    population = 1243
    # Uncertain exactly what/how many interventions to expect
    interventions = [True, False, True]
    dayOfWeek = 1  # Takes values 1-7 representing Mon-Sun
    timeOfDay = 0  # Takes values 0-23 representing the hour (rounded down)

    # getUserInput: This function will assign the state, county, and interventions as the user specifies
    # params:
    #   state - the state passed by the user
    #   county - the county passed by the user
    #   interventions - an array oof booleans corresponding to certain interventions (size TBD)
    def getUserInput(self, state, county, interventions):
        self.state = state
        self.county = county
        self.interventions = interventions

    # createModules: This function will create a module with the given state, county, and interventions
    # params:
    #   state - the state passed by the user
    #   county - the county passed by the user
    #   interventions - an array oof booleans corresponding to certain interventions (size TBD)
    def createModule(self):
        return Module(self.state, self.county, self.interventions)

    # updateTime: This function will advance the time forward one hour
    # params:
    #   dayOfWeek - current day of the week
    #   timeOfDay - the current time of day
    def updateTime(self):
        if self.timeOfDay == 23:
            self.dayOfWeek = self.dayOfWeek + 1
        self.timeOfDay = (self.timeOfDay + 1) % 24

    # runSim: This function runs the simulation over a desired time interval
    # params:
    #   interval - the number of hours to run the simulation for
    #   population - the population as instantiated by a Module object
    #   facilities - the facility list as instantiated by a Module object
    def runSim(self, interval, population, facilities, module):
        # for each time step, move population, create subgroups, infect the new people
        # uncertain exactly how time works
        for i in range(interval):
            module.movePop(self.dayOfWeek, self.timeOfDay,
                           population, facilities)
            for facility in facilities:
                facility.createGroups()
                G = facility.createGraph()
                facility.calcInfection(G)
            self.updateTime()

    def displayResult(self):
        print('Nothing to show yet')
        # TODO

    def main(self):
        # TODO Get user input
        M = self.createModule()
        Pop = M.createPopulation()
        for i in range(5):
            ran = random.randint(0, len(Pop) - 1)
            Pop[ran].setInfectionState(True)
        Facilities = M.createSubmodules()
        interval = 2
        self.runSim(interval, Pop, Facilities, M)
        count = 0
        for each in Pop:
            if Pop[each].getInfectionState():
                count += 1
        print(count)

    # Wells-Riley
    def main2(self, num_days=7):
        '''
        This function calculates the disease progression by each person in the
        '''
        M = self.createModule()
        Pop = M.createPopulation()

        # assign initial state status for each person
        initialIndected = 10
        assigned = set()
        for i in range(initialIndected):
            nextInfected = random.randint(0, len(Pop) - 1)
            while nextInfected in assigned:
                nextInfected = random.randint(0, len(Pop) - 1)
            Pop[nextInfected] = 1  # mild
            assigned.add(nextInfected)

        # initialize submodules
        # TODO: to pull from actual data of Oklohoma/frontend map.
        # currently assuming a fixed number of each, and using a range of 6 types of facilities representing different essential level and attributes eg ventilation rate
        facilities = []
        totalFacilityCapacities = 0
        # add restaurants
        facilityID = 0
        for i in range(10):
            nextFacility = Submodule(facilityID, 'Restaurant')
            facilityID += 1
            facilities.append(nextFacility)
            totalFacilityCapacities += nextFacility.getCapacity()
        # add church
        for i in range(4):
            nextFacility = Submodule(facilityID, 'Church')
            facilityID += 1
            facilities.append(nextFacility)
            totalFacilityCapacities += nextFacility.getCapacity()
        # add supermarket
        for i in range(5):
            nextFacility = Submodule(facilityID, 'Supermarket')
            facilityID += 1
            facilities.append(nextFacility)
            totalFacilityCapacities += nextFacility.getCapacity()
        # add supermarket
        for i in range(5):
            nextFacility = Submodule(facilityID, 'Retail')
            facilityID += 1
            facilities.append(nextFacility)
            totalFacilityCapacities += nextFacility.getCapacity()
        # add hospital
        for i in range(4):
            nextFacility = Submodule(facilityID, 'Hospital')
            facilityID += 1
            facilities.append(nextFacility)
            totalFacilityCapacities += nextFacility.getCapacity()
        # add hospital
        for i in range(4):
            nextFacility = Submodule(facilityID, 'Gas station')
            facilityID += 1
            facilities.append(nextFacility)
            totalFacilityCapacities += nextFacility.getCapacity()
        infectionInFacilities = {id: [] for id in range(facilityID)}
        total = []  # for infected number across the city
        # iterate through the hours in the days input by user. Assume movements to facilities in the day only (10:00 - 18:00)
        print([i for i in Pop if type(Pop[i]) == type(1)])
        print("DONE!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        for h in range(num_days+7):
            total.append(0)
            if 10 < h % 24 < 18:
                assigned = set()
                # number of people who are not at home/school/work
                numberOut = random.randint(
                    0, min(len(Pop)-1, totalFacilityCapacities))
                # TODO: retention rate within the same facility. currently no one is retained
                for facility in facilities:
                    facility.setVisitors(0)
                    facility.clearPeople()
                for i in range(numberOut):
                    nextID = random.randint(0, len(Pop)-1)
                    while nextID in assigned:
                        nextID = random.randint(0, len(Pop)-1)
                    facility = random.randint(0, facilityID-1)
                    # if facility is full, put the person out to the another facility
                    while facilities[facility].getCapacity() == facilities[facility].getVisitors():
                        facility = random.randint(0, facilityID)
                    facilities[facility].addPerson(Pop[nextID])
                for i in range(len(facilities)):
                    initialInfectionNumber = len(facilities[i].getInfected())
                    finalInfectionNumber = initialInfectionNumber
                    prob = facilities[i].probability()
                    for person in facilities[i].getPeople():
                        if person.infectionState == 0:
                            continue
                        temp = random.uniform(0, 1)
                        if temp > prob:
                            person.infectionState = 1
                            finalInfectionNumber += 1
                            total[-1] += 1
                    infectionInFacilities[i].append(
                        [initialInfectionNumber, finalInfectionNumber])
                # print progression for each facility
                for facility in infectionInFacilities:
                    print(facility.getID(), facility.getFacilityType(),
                          infectionInFacilities[facility])
                print(total)


if __name__ == '__main__':
    mc = MasterController()
    mc.main2(7)
