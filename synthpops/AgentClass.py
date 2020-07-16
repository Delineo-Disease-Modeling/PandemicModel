class Agent: 
    def __init__(self,id, age, sex, work, household, school):
        self.__id = id
        self.__age = age 
        self.__sex = sex
        self.__workContact = work 
        self.__householdContact = household 
        self.__schoolContact = school
    
    def getId(self):
        return self.__id 
    
    def getAge(self):
        return self.__age

    def getSex(self):
        return self.__sex 

    def setInfection(self, infection):
        self.__infection = infection

    def getInfection(self):
        return self.__infection

    def getInfectionType(self):
        return self.__infectionType
    
    def setInfectioType(self, infectionType):
        self.__infectionType = infectionType

    def setWorkContact(self, contact):
        self.__workContact = contact 
    
    def setSchoolContact(self, contact):
        self.__schoolContact = contact 
    
    def setHouseholdContact(self, contact):
        self.__householdContact = contact

    def getWorkContact(self):
        return self.__workContact
    
    def getSchoolContact(self):
        return self.__schoolContact 
    
    def getHouseholdContact(self):
        return self.__householdContact

    def getContactList(self):
        return self.__contact 

    def getTansMatrix(self):
        return self.__matrix
    
    def setTansMatrix(self, transitionMatrix):
        self.__matrix = matrix

def createAgents(popdict):
    agents = []
    print(popdict)
    for person in popdict:
        agent =  Agent(person, popdict[person]['age'], popdict[person]['sex'], popdict[person]['contacts']['M'], popdict[person]['contacts']['M'], popdict[person]['contacts']['M'])
        agent.setInfection(0)
        agents.append(agent)

    return agents