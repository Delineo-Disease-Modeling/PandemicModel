from person import Person
from module import Module
from submodule import Submodule
import random


class MasterController:
    # MasterController class, this runs the simulation by instantiating module

    state = 'Oklahoma'
    county = 'Barnsdall'
    population = 1243
    # Uncertain exactly what/how many interventions to expect
    interventions = [True, False, True]  # Interventions represented as boolean list
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
                           population, facilities) #  Moves population at interval steps (eventually move pop will be
                                                   #  Integrated with ML team
            for facility in facilities:
                facility.createGroups() # Groups being created
                G = facility.createGraph() # Graph created
                facility.calcInfection(G)
            self.updateTime()

    def displayResult(self):
        print('Nothing to show yet')
        # TODO

    def main(self):
        # TODO Integrate Graph approach with current spread model
        M = self.createModule()  # Module instantiated - holds the submodules(facilities), population
        Pop = M.createPopulation()  # Population created and returned as array of People class objects

        # Initialize 5 current infections - This will eventually be customizable. Consider - if we have 20 initial
        # infections how should we spread them through the population?
        for i in range(5):
            ran = random.randint(0, len(Pop) - 1)
            Pop[ran].setInfectionState(True)
        Facilities = M.createSubmodules() # Submodules returned as list of submodule objects.
        interval = 2
        self.runSim(interval, Pop, Facilities, M)
        count = 0
        for each in Pop:
            if Pop[each].getInfectionState():
                count += 1
        print(count)

    # Wells-Riley
    def WellsRiley(self, num_days=7):
        '''
        This function calculates the disease progression by each person in the
        '''
        M = self.createModule()  # Module instantiated - holds the submodules(facilities), population
        Pop = M.createPopulation() # Population created and returned as array of People class objects

        # Assign initial state status for each person
        initialInfected = 10  # Should be customizable in  the future
        assigned = set()
        for i in range(initialInfected):
            nextInfected = random.randint(0, len(Pop) - 1)
            while nextInfected in assigned:
                nextInfected = random.randint(0, len(Pop) - 1)
            Pop[nextInfected].infectionState = 1  # mild, to be callibrated with disease driver. Consider what initial states should be.
            assigned.add(nextInfected)

        # initialize submodules
        # TODO: to pull from actual data of Oklahoma/frontend map.
        # currently assuming a fixed number of each, and using a range of 6 types of facilities representing different essential level and attributes eg ventilation rate
        facilities, totalFacilityCapacities, openHours = M.createFacilities(
            "submodules.json")  # Facilities is dictionary of id: submodule object, openHours dict of hour: set of facilities open,
                                # totalFacilityCapacities is int
        infectionInFacilities = {id: []
                                 for id in range(len(facilities.keys()))} # dictionary with id as keys, empty list as vals
        households = Submodule(len(facilities), "Household", len(Pop),
                                range(24), ["M", "T", "W", "Th", "F", "Sat", "Sun"])
        total = [0]  # for infected number across the city
        # iterate through the hours in the days input by user. Assume movements to facilities in the day only (10:00 - 18:00)
        daysDict = {
            0: "Sun",
            1: "M",
            2: "T",
            3: "W",
            4: "Th",
            5: "F",
            6: "Sat"
        }
        numFacilities = len(facilities)
        for h in range(num_days * 24):
            total.append(total[-1])  # initialize num infected based on end of last day
            assigned = set()  # keeping track of people assigned to a facility
            # number of people who are not at home/school/work
            numberOut = random.randint(
                0, min(len(Pop)-1, totalFacilityCapacities))
            day = (int(h / 24)) % 7
            hour = h % 24
            # TODO: retention rate within the same facility. currently no one is retained - Retention rate eventually covered by ML team
            households.setVisitors(0)
            households.clearPeople()
            for id in facilities:
                facility = facilities[id]
                facility.setVisitors(0)
                facility.clearPeople()
            for i in range(numberOut):
                nextID = random.randint(0, len(Pop)-1)
                while nextID in assigned:
                    nextID = random.randint(0, len(Pop)-1)
                facility = random.randint(0, numFacilities-1)
                # if facility is full, put the person out to the another facility
                facilityIsOpen = (daysDict[day] in facilities[facility].getDays()
                                    and facilities[facility] in openHours[hour])
                while (facilities[facility].getCapacity() ==
                facilities[facility].getVisitors() and not facilityIsOpen):
                    facility = random.randint(0, numFacilities-1)
                facilities[facility].addPerson(Pop[nextID]) 

            # TODO* This is where we create, populate and calculate infections for household submodule.
            numberIn = len(Pop) - numberOut
            for i in range(len(Pop)):
                if i not in assigned:
                    households.addPerson(Pop[i])
            """
            households.createGroups()
            G = households.createGraph()
            households.calcInfection(G)
            """

            for i in range(len(facilities)):  # iterate through facilities
                open = False
                # check if open in this hour on this day
                # h % 24, h / 24
                if daysDict[day] not in facilities[i].getDays():
                    infectionInFacilities[i].append("Not open")
                    continue
                if facilities[i] not in openHours[hour]:
                    infectionInFacilities[i].append("Not open")
                    continue
                initialInfectionNumber = len(facilities[i].getInfected())
                finalInfectionNumber = initialInfectionNumber
                prob = facilities[i].probability() # returns a probability of others in the same submodule contracting covid
                for person in facilities[i].getPeople():
                    if person.infectionState == 0:
                        continue
                    temp = random.uniform(0, 1)
                    if temp > prob: # Infects according to prob model
                        person.infectionState = 1
                        finalInfectionNumber += 1  # TODO* Submodules should have a tracker as to how many people get infected there per day ie a list.
                        total[-1] += 1
                infectionInFacilities[i].append(
                    [initialInfectionNumber, finalInfectionNumber])
        # print progression for each facility
        #f = open('output.txt', 'w')
        print(
            f"Results for {self.county}, {self.state} over {num_days} days")  # , file=f)
        for id in infectionInFacilities:
            facility = facilities[id]
            print(facility.getID(), facility.getFacilityType(),
                  infectionInFacilities[id])  # , file=f)
        print()
        # , file=f)
        print("Change in total infection number in the population is ", total)
        # f.close()


if __name__ == '__main__':
    mc = MasterController()  # Instantiate a MasterController
    # TODO* Graph approach for standard facilities is above in main. We want to tweak this for a household model.
    # TODO School and Work spread need to be implemented as well - either through Wells Reilly model or Graph approach.
    # TODO MasterController() should take in json file - load information such as population, interventions, etc
    # TODO Callibration to match realistic/standard data once above is completed.
    mc.WellsRiley(7)  # Run Wells Reilly
