import synthpops.synthpops as sp
#If above not working try
#import synthpops as sp
from person import Person
import random


class Population():
    # constructor

    def __init__(self, state, country, population=[], peopleArray={}, populationSize=0):

        self.state = state
        self.country = country
        self.population = population  # array of different person classes
        self.peopleArray = peopleArray
        self.populationSize = populationSize

    def get_dict(self):
        sp.validate()
        datadir = sp.datadir
        location = 'barnsdall'
        state_location = 'Oklahoma'
        country_location = 'usa'
        sheet_name = 'United States of America'
        level = 'county'

        num_households = 3000 # 459
        npop = 6000 #1132 #this is 6000 - but when increased synthpops does not work
        num_workplaces = 200

        # TODO: default school sizes are still being used
        population, homes_dic = sp.generate_synthetic_population(npop, datadir, num_households, num_workplaces, location=location,
                                                              state_location=state_location, country_location=country_location, sheet_name=sheet_name, use_default=True, return_popdict=True)
        peopleArray = {}
        for i in range(npop):
            person = Person(i)
            person.setSynthPopParameters(population[i])
            peopleArray[i] = person
        self.peopleArray = peopleArray

        return peopleArray

    # calls synthpops and generates population (dictionary)
    def generatePopulation(populationSize):
        # call function from person class
        peopleArray = {}
        population = sp.generate_synthetic_population(populationSize)
        for i in range(populationSize):
            person = Person()
            person.setSynthPopParameters(population[i]['age'], population[i]['sex'],
                                         population[i]['location'], population[i]['contacts'])
            peopleArray[i] = person

        self.peopleArray = peopleArray

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

    # calculates severity risk matrix

    def calcMatrix(self):
        return sum(self.addComorbidities)/len(self.addDem)

    # assigns a person cancer based on the percentages for their risk
    def addCancer(self):
        cancerDistr = open("diseasedata/cancer.dat", "r")

        distr = {}
        for lines in cancerDistr:
            brackets = lines.split(",")
            distr[brackets[0]] = float(brackets[1])

        for p in self.peopleArray.values():
            for key, value in distr.items():
                range = key.split("_")
                if p.age >= int(range[0]) and p.age <= int(range[1]):
                    n = random.random()
                    if n <= value:
                        p.addDisease("cancer")
                        break
                    break

    # assigns a person diabetes based on the percentage for their risk
    def addDiabetes(self):
        diabetesDistr = open("diseasedata/diabetes.dat", "r")

        distr = {}
        for lines in diabetesDistr:
            brackets = lines.split(",")
            distr[brackets[0]] = float(brackets[1])

        for p in self.peopleArray.values():
            for key, value in distr.items():
                range = key.split("_")
                if p.age >= int(range[0]) and p.age <= int(range[1]):
                    n = random.random()
                    if n <= value:
                        p.addDisease("diabetes")

                        break
                    break

    # assigns a person kidney disease based on the percentage for their risk

    def addKidneyDisease(self):
        kidneyDistr = open("diseasedata/kidney_disease.dat", "r")

        distr = {}
        for lines in kidneyDistr:
            brackets = lines.split(",")
            distr[brackets[0]] = float(brackets[1])

        for p in self.peopleArray.values():
            for key, value in distr.items():
                range = key.split("_")
                if p.age >= int(range[0]) and p.age <= int(range[1]):
                    n = random.random()
                    if n <= value:
                        p.addDisease("kidney disease")

                        break
                    break

    # assigns a person COPD based on the percentage for their risk

    def addCOPD(self):
        copdDistr = open("diseasedata/COPD.dat", "r")

        distr = {}
        for lines in copdDistr:
            brackets = lines.split(",")
            distr[brackets[0]] = float(brackets[1])

        for p in self.peopleArray.values():
            for key, value in distr.items():
                range = key.split("_")
                if p.age >= int(range[0]) and p.age <= int(range[1]):
                    n = random.random()
                    if n <= value:
                        p.addDisease("COPD")

                        break
                    break

    # assigns a person obesity based on the percentage for their risk

    def addObesity(self):
        for p in self.peopleArray.values():
            if p.age >= 18:
                n = random.random()
                if n <= 0.398:
                    p.addDisease("obesity")

    # assigns a person cystic fibrosis on the percentage for their risk
    def addCysticFibrosis(self):
        for p in self.peopleArray.values():
            if p.age <= 44:
                n = random.random()
                if n <= 0.00009504949:
                    p.addDisease("cystic fibrosis")

    # assigns a person hypertension based on the percentage for their risk
    def addHypertension(self):
        hypertensionDistr = open("diseasedata/hypertension.dat", "r")

        distr = {}
        for lines in hypertensionDistr:
            brackets = lines.split(",")
            distr[brackets[0]] = float(brackets[1])

        for p in self.peopleArray.values():
            for key, value in distr.items():
                range = key.split("_")
                if p.age >= int(range[0]) and p.age <= int(range[1]):
                    n = random.random()
                    if n <= value:
                        p.addDisease("hypertension")

                        break
                    break

    # assigns a person smoking based on the percentage for their risk

    def addSmoking(self):
        smokingDistr = open("diseasedata/smoking.dat", "r")

        distr = {}
        for lines in smokingDistr:
            brackets = lines.split(",")
            distr[brackets[0]] = float(brackets[1])

        for p in self.peopleArray.values():
            for key, value in distr.items():
                range = key.split("_")
                if p.age >= int(range[0]) and p.age <= int(range[1]):
                    n = random.random()
                    if n <= value:
                        p.addDisease("smoking")

                        break
                    break

    # assigns a person asthma based on the percentage for their risk

    def addAsthma(self):
        asthmaDistr = open("diseasedata/asthma.dat", "r")

        distr = {}
        for lines in asthmaDistr:
            brackets = lines.split(",")
            distr[brackets[0]] = float(brackets[1])

        for p in self.peopleArray.values():
            for key, value in distr.items():
                range = key.split("_")
                if p.age >= int(range[0]) and p.age <= int(range[1]):
                    n = random.random()
                    if n <= value:
                        p.addDisease("asthma")

                        break
                    break

    # assigns a person liver disease based on the percentage for their risk

    def addLiverDisease(self):
        liverDistr = open("diseasedata/liver_disease.dat", "r")

        distr = {}
        for lines in liverDistr:
            brackets = lines.split(",")
            distr[brackets[0]] = float(brackets[1])

        for p in self.peopleArray.values():
            for key, value in distr.items():
                range = key.split("_")
                if p.age >= int(range[0]) and p.age <= int(range[1]):
                    n = random.random()
                    if n <= value:
                        p.addDisease("liver disease")

                        break
                    break

    # assign all diseases based on the percentage of risk

    def addDisease(self):
        self.addCancer()
        self.addDiabetes()
        self.addKidneyDisease()
        self.addCOPD()
        self.addObesity()
        self.addSmoking()
        self.addAsthma()
        self.addLiverDisease()
        self.addCysticFibrosis()
        self.addHypertension()

