from simulation.person import Person
from simulation.module import Module

class MasterController:
    # MasterController class, this runs the simulation by instantiating module

    state = 'Indiana'
    county = 'Barnsdall'
    interventions = [True, False, True] # Uncertain exactly what/how many interventions to expect
    dayOfWeek = 1 # Takes values 1-7 representing Mon-Sun
    timeOfDay = 0 # Takes values 0-23 representing the hour (rounded down)

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
            module.movePop(self.dayOfWeek, self.timeOfDay) 
            for facility in facilities:
                G = facility.createGraph()
                facility.calcInfection(G)
            self.updateTime()


    def displayResult(self):
        print('Nothing to show yet')
        #TODO

    def main(self):
        #TODO Get user input

        M = self.createModule()
        Pop = M.createPopulation()
        Facilities = M.createSubmodules()
        interval = 100
        self.runSim(interval, Pop, Facilities, M)
        