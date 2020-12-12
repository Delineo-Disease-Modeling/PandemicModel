import synthpops as sp
from person import Person
import random

class Population():
    #constructor
    def __init__(self, state, country, population=[], peopleArray=[], populationSize=0):
        print("Pop constructor")
        self.state = state
        self.country = country
        self.population = population #array of different person classes
        self.peopleArray = peopleArray
        self.populationSize = populationSize


    def get_dict(self):
        print("get_dict")
        sp.validate()
        datadir = sp.datadir
        location = 'seattle_metro'
        state_location = 'Washington'
        country_location = 'usa'
        sheet_name = 'United States of America'
        level = 'county'
        
        num_households = 459
        npop = 1132
        num_workplaces = 200
        
        pop, homes_dic = sp.generate_synthetic_population(npop, datadir, num_households, num_workplaces, location, state_location, country_location, sheet_name, level)
        print(pop)
        return pop, homes_dic
    
    #calls synthpops and generates population (dictionary)
    def generatePopulation(populationSize):
        #call function from person class
        peopleArray = {}
        population = sp(populationSize)
        for i in range(populationSize):
            person = Person()
            person.setSynthPopParameters(population[i]['age'], population[i]['sex'], 
                                         population[i]['location'], population[i]['contacts'])
            peopleArray[i] = person
        return peopleArray
        
        
    def addComorbidities(self):
        comorbiditiesArray = {}
        for i in range(len(self.peopleArray)):
            self.peopleArray[i].setComorbidities(random.randint(0, 5))
        return comorbiditiesArray
        
        
    def addDem(self):
        demographicsArray = {}
        for i in range(len(self.peopleArray)):
            self.peopleArray[i].setDemographicInfo(random.randint(0, 5))
        return demographicsArray
        
        
    #calculates severity risk matrix
    def calcMatrix(self):
        return sum(self.addComorbidities)/len(self.addDem)
        
    
