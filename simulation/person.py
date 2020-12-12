class Person:

    #Initialization function, sets all parameters at once.
    #TODO: have some default parameters if we can't set all of them at once, like
    #for initializing them with synthpops.
    def __init__(self ,ID, age = 0, sex = 0, householdLocation = 0, householdMembers=[], comorbidities=0, demographicInfo=0, severityRisk=0, currentLocation=0, infectionState=False, incubation=0):
        self.setAllParameters(ID, age, sex, householdLocation, householdMembers, comorbidities, demographicInfo, severityRisk, currentLocation, infectionState, incubation)
        
    #Sets all parameters.
    def setAllParameters(self, ID, age = 0, sex = 0, householdLocation = 0, householdMembers=[], comorbidities=0, demographicInfo=0, severityRisk=0, currentLocation=0, infectionState=False, incubation=0):
        self.ID = ID
        self.age = age
        self.sex = sex
        self.householdLocation = householdLocation
        self.householdMembers = householdMembers
        self.comorbidities = comorbidities
        self.demographicInfo = demographicInfo
        self.severityRisk = severityRisk
        self.currentLocation = currentLocation
        self.infectionState = infectionState
        self.incubation = incubation


    def getID(self):
        return self.ID

    #sets specific parameters from the info available in the synthpops generated population.
    #householdLocation = location, householdMembers = contacts
    def setSynthPopParameters(self, age, sex, householdLocation, householdMembers):
        self.age = age
        self.sex = sex
        self.householdLocation = householdLocation
        self.householdMembers = householdMembers
    
    #setters for remaining variables
    def setComorbidities(self, comorbidity):
        self.comorbidities = comorbidity
        
    def setDemographicInfo(self, demographic):
        self.demographicInfo = demographic
    
    def setSeverityRisk(self):
        self.severityRisk = self.calcSeverityRisk(self.age, self.sex, self.comorbidities, self.demographicInfo)
    
    def setCurrentLocation(self, location):
        self.currentLocation = location
        
    def setInfectionState(self, state):
        self.infectionState = state
        
    def setIncubation(self, incubation):
        self.incubation = incubation
    
    #calculate severity risk based on demographic factors, as of now calculation is undefined.
    def calcSeverityRisk(age, sex, comorbidities, demographicInfo):
        return -1
    
    #getters for all variables
    def getAge(self):
        return self.age
    
    def getSex(self):
        return self.sex
    
    def getComorbidities(self):
        return self.comorbidities
    
    def getDemographicInfo(self):
        return self.demographicInfo
    
    def getHouseholdLocation(self):
        return self.householdLocation
    
    def getHouseholdMembers(self):
        return self.householdMembers
    
    def getSeverityRisk(self):
        return self.severityRisk
    
    def getCurrentLocation(self):
        return self.currentLocation
    
    def getInfectionState(self):
        return self.infectionState
    
    def getIncubation(self):
        return self.incubation
    
    def updateIncubation(self):
        self.incubation = self.incubation - 1
    
    def updateState(self):
        return self.incubation + self.severityRisk