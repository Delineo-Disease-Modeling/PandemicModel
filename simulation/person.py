import random
import numpy as np

class Person:

    # Initialization function, sets all parameters at once.
    # TODO: have some default parameters if we can't set all of them at once, for initializing them with synthpops.

    def __init__(self, ID, age=0, sex=0, householdLocation=0, householdMembers=None, comorbidities=0, demographicInfo=0,
                 severityRisk=0, currentLocation=0, infectionState=-1, incubation=0, infectionTimer=-1, infectionTrack=None,
                 extendedhousehold=None):
        self.setAllParameters(ID, age, sex, householdLocation, householdMembers, comorbidities,
                              demographicInfo, severityRisk, currentLocation, infectionState, incubation,
                              infectionTimer, infectionTrack,extendedhousehold)

    # Sets all parameters.
    def setAllParameters(self, ID, age=0, sex=0, householdLocation=0,
                         householdContacts=None, comorbidities=0, demographicInfo=0,
                         severityRisk=0, currentLocation=0, infectionState=-1, incubation=0,
                         infectionTimer=-1, infectionTrack=None,extendedhousehold=None):
        if extendedhousehold is None:
            self.extendedhousehold = set()
        if householdContacts is None: #python specific way of creating mutable defaults
            householdContacts = []
        if infectionTrack is None:
            infectionTrack = []

        self.ID = ID
        self.age = age
        self.sex = sex
        self.householdLocation = householdLocation
        self.householdContacts = householdContacts
        self.comorbidities = comorbidities
        self.demographicInfo = demographicInfo
        self.severityRisk = severityRisk
        self.currentLocation = currentLocation

        # -1: normal, 0: asymp, 1: mild, 2: severe, 3: critical, 4: recovered
        self.infectionState = infectionState
        self.incubation = incubation
        self.disease = []
        self.infectionTimer = infectionTimer
        self.infectionTrack = infectionTrack

    def getextendedhousehold(self):
        return self.extendedhousehold
    def addtoextendedhousehold(self, p):
        self.extendedhousehold.add(p)
    def getID(self):
        return self.ID
    def getInfectionTrack(self):
        return self.infectionTrack
    def getinfectionTimer(self):
        return self.infectionTimer

    # sets specific parameters from the info available in the synthpops generated population.
    #householdLocation = location, householdMembers = contacts
    """
        age, household ID (hhid), school ID (scid), workplace ID (wpid), workplace industry code (wpindcode) if available, and the IDs of their contacts in different layers. Different layers
        available are households ('H'), schools ('S'), and workplaces ('W'). Contacts in these layers are clustered and thus form a network composed of groups of people interacting with each other. For example, all
        household members are contacts of each other, and everyone in the same school is a contact of each other. Else, return None.
    """

    def setSynthPopParameters(self, synthPopsPersonDict): #maybe need changes here

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

        return state


    def setIncubation(self, incubation):
        self.incubation = incubation

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

        return self.householdContacts

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


        # calculate severity risk based on demographic factors, as of now calculation is undefined.

    def calcSeverityRisk(self):
        # numComorbidities = len(self.comorbidities) if list
        numComorbidities = self.comorbidities
        # sex not currently accounted for
        sevRisk = open("diseasedata/severity_risk.dat", "r")
        distrWithComorbidities = {}
        distrWithoutComorbidities = {}
        for lines in sevRisk:
            brackets = lines.split(",")
            distrWithComorbidities[int(brackets[0])] = float(brackets[2])
            distrWithoutComorbidities[int(brackets[0])] = float(brackets[1])
        ageCategory = int((self.age // 10)) * 10
        if ageCategory >= 100: #temporary fix to no data for 100+
            ageCategory = 90
        if numComorbidities == 0:
            srScore = int(distrWithoutComorbidities[ageCategory])
        else:
            srScore = int(distrWithComorbidities[ageCategory] * pow(0.75, numComorbidities))

        sevRisk.close()
        return srScore

    def calcInfectionState(self):
        infectionStateByScore = {
            0: [0.7, 0.1, 0.05, 0.05],
            10: [0.6, 0.2, 0.1, 0.1],
            20: [0.5, 0.3, 0.1, 0.1],
            30: [0.4, 0.3, 0.2, 0.1],
            40: [0.3, 0.2, 0.2, 0.1],
            50: [0.3, 0.2, 0.2, 0.1],
            60: [0.2, 0.2, 0.3, 0.3],
            70: [0.1, 0.2, 0.4, 0.3],
            80: [0.05, 0.05, 0.3, 0.6],
            90: [0.05, 0.05, 0.2, 0.7]
        }
        severityScoreCategory = int(self.calcSeverityRisk() // 10) * 10
        n = np.random.uniform()
        threshold = (infectionStateByScore[severityScoreCategory])[0]
        if n < threshold:
            return 0  # 0 = asymptomatic
        threshold += (infectionStateByScore[severityScoreCategory])[1]
        if n < threshold:
            return 1  # 1 = mild
        threshold += (infectionStateByScore[severityScoreCategory])[2]
        if n < threshold:
            return 2  # 2 = severe
        else:
            return 3  # 3 = critical

    #called once infected and each day that passes.
    #Once infected, infection function should update this value to 0.
    def incrementInfectionTimer(self):
        #once passed 15 days, infection is over.
        #TODO will change depending on severity level.
        if self.infectionTimer >= len(self.infectionTrack) - 1:
            return self.infectionTimer
        #Otherwise, incremement infectionTimer.
        self.infectionTimer += 1
        return self.infectionTimer

    #needs to be called once infected. (and updated each day until 0)
    #TODO incubation days change based on severityRisk/age?
    def incubationAssignment(self):
        #get a random number between 1-3 for incubation days
        randNum = random.randint(1, 3)
        self.incubation = randNum
        return randNum

    #Assign number of days spent at peak state based on severity risk
    #TODO update according to info support research
    def assignNumDaysPeakState(self):

        peakStateDays =0
        #peakStateDays ranging from 4-10 days, based on severityRisk
        if self.severityRisk >= 0 & self.severityRisk <=25:
            peakStateDays = 4

        elif self.severityRisk >= 25 & self.severityRisk <= 50:
            peakStateDays = 6

        elif self.severityRisk >= 50 & self.severityRisk <= 75:
            peakStateDays = 8

        else:
            peakStateDays = 10
        return peakStateDays

    def assignTrajectory(self):
        peakstate = self.calcInfectionState()
        self.severityRisk = self.calcSeverityRisk()
        incubation = self.incubationAssignment()
        peakStateDays = self.assignNumDaysPeakState()
        for i in range(incubation):
            self.infectionTrack.append(-1)
        for i in range(peakStateDays):
            self.infectionTrack.append(peakstate)

        if self.infectionState == 0: #asymptomatic
            #14 to 21 days for recovery
            randNum = random.randint(14, 21)
            recoveryDaysToBeDivided = randNum

        elif self.infectionState == 1: #mild
            # 14 to 21 days for recovery
            randNum = random.randint(14, 21)
            recoveryDaysToBeDivided = randNum

        elif self.infectionState == 2:
            #21 to 42 days for recovery
            randNum = random.randint(21, 42)
            recoveryDaysToBeDivided = randNum
        else:
            #crticial
            randNum = random.randint(21, 42)
            recoveryDaysToBeDivided = randNum
        daysleft = randNum - incubation - peakStateDays
        if peakstate != 0:
            daysPerState = daysleft // (peakstate)  #split evenly through rest of days
        else:
            daysPerState = daysleft
        extraAsymptomatic = 0
        if daysPerState * peakstate < daysleft:
            extraAsymptomatic = daysleft - daysPerState * peakstate
        for i in range(peakstate-1,-1,-1): #Asymptotic recovery??? no state to go after peak state
            for j in range(daysPerState):
                self.infectionTrack.append(i)
        for j in range(extraAsymptomatic):
            self.infectionTrack.append(0)
        self.infectionTrack.append(4)



"""
    def stateUp(self):
        #once incubation period complete, being moving into next states
        if self.incubation <= 0:
        #maximum infection state variable created
        #TODO check to see where implementation of severity risk matrix will be done and how we will get that info.
            if self.infectionState < self.maximumInfectionState:
                #increment infectionState by  1
                self.infectionState += 1



    def stateDown(self):
        #once peakStateDays end, moving down each date
        #Recovered by day 15

        #patient has few more recoveryDays left in their current infectionState
        if self.recoveryDays[self.infectionState] != 0:
            self.recoveryDays[self.infectionState] -= 1

        else:
            #no more days left in the current infectionState
            #move down one state
            self.infectionState -= 1 # infection state becomes -1
            self.recoveryDays[self.infectionState] -= 1 
            """

