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
    def createModules(self):
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
    def runSim(self, interval, population, facilities):
        # for each time step, move population, create subgroups, infect the new people
        # uncertain exactly how time works
        for i in range(interval):
            for facility in facilities:
                population.move(self.dayOfWeek, self.timeOfDay) # Not in UML but I think it is necesssary
                groups = facility.createGroups()
                for group in groups:
                    group.calcInfection()
                    #TODO use these new infections to update the population
            self.updateTime()


    def displayResult(self):
        print('Nothing to show yet')
        #TODO
        