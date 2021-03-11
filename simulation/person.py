class Person:

    # Initialization function, sets all parameters at once.
    # TODO: have some default parameters if we can't set all of them at once, for initializing them with synthpops.
    def __init__(self, ID, age=0, sex=0, householdLocation=0,
            householdMembers=[], comorbidities=0, demographicInfo=0,
            severityRisk=0, currentLocation=0, infectionState=-1, incubation=0):
        self.setAllParameters(ID, age, sex, householdLocation, householdMembers, comorbidities,
                              demographicInfo, severityRisk, currentLocation, infectionState, incubation)

    # Sets all parameters.
    def setAllParameters(self, ID, age=0, sex=0, householdLocation=0,
            householdMembers=[], comorbidities=0, demographicInfo=0,
            severityRisk=0, currentLocation=0, infectionState=0, incubation=0):
        self.ID = ID
        self.age = age
        self.sex = sex
        self.householdLocation = householdLocation
        self.householdMembers = householdMembers
        self.comorbidities = comorbidities
        self.demographicInfo = demographicInfo
        self.severityRisk = severityRisk
        self.currentLocation = currentLocation
        # 0: susceptible, 1: asymptomatic, 2: mild, 3: severe, 4: critical, 5: recovered
        self.infectionState = infectionState
        self.incubation = incubation
        self.disease = []

    def getID(self):
        return self.ID

    # sets specific parameters from the info available in the synthpops generated population.
    #householdLocation = location, householdMembers = contacts
    """
        age, household ID (hhid), school ID (scid), workplace ID (wpid), workplace industry code (wpindcode) if available, and the IDs of their contacts in different layers. Different layers
        available are households ('H'), schools ('S'), and workplaces ('W'). Contacts in these layers are clustered and thus form a network composed of groups of people interacting with each other. For example, all
        household members are contacts of each other, and everyone in the same school is a contact of each other. Else, return None.
    """
    def setSynthPopParameters(self, synthPopsPersonDict):
        for k, v in synthPopsPersonDict.items():
            setattr(self, k, v)
        self.householdContacts = self.contacts['H']
        self.schoolContacts = self.contacts['S']
        self.workplaceContacts = self.contacts['W']

    # setters for remaining variables
    def setComorbidities(self, comorbidity):
        self.comorbidities = comorbidity

    def setDemographicInfo(self, demographic):
        self.demographicInfo = demographic

    def setSeverityRisk(self):
        self.severityRisk = self.calcSeverityRisk(
            self.age, self.sex, self.comorbidities, self.demographicInfo)

    def setCurrentLocation(self, location):
        self.currentLocation = location

    def setInfectionState(self, state):
        self.infectionState = state

    def setIncubation(self, incubation):
        self.incubation = incubation

    # calculate severity risk based on demographic factors, as of now calculation is undefined.
    def calcSeverityRisk(self, age, sex, comorbidities):
        return -1

    # getters for all variables
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

    def addDisease(self, disease):
        self.disease.append(disease)

    def getConditions(self):
        return self.disease
