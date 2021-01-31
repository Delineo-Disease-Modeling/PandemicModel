import synthpops.synthpops as sp
from person import Person
import random


class Population():
    # constructor
    def __init__(self, state, country, population=[], peopleArray=[], populationSize=0):
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

        num_households = 459
        npop = 1132
        num_workplaces = 200

        # TODO: default school sizes are still being used
        population, homes_dic = sp.generate_synthetic_population(npop, datadir, num_households, num_workplaces, location=location,
                                                                 state_location=state_location, country_location=country_location, sheet_name=sheet_name, use_default=True, return_popdict=True)
        peopleArray = {}
        for i in range(npop):
            person = Person(i)
            person.setSynthPopParameters(population[i]['age'], population[i]['sex'],
                                         population[i]['loc'], population[i]['contacts'])
            peopleArray[i] = person
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
    def addCancer():
        cancerDistr = open("cancer.dat", "r")
        distr = {}
        for lines in cancerDistr:
            brackets = lines.split(",")
            distr[brackets[0]] = float(brackets[1])
        for p in peopleArray:
            for key, value in distr.items():
                range = key.split("_")
                if p.age >= int(range[0]) and p.age <= int(range[1]):
                    n = np.random.randint()
                    if n <= value:
                        p.disease.append("cancer")
                        break
                    break

    # assigns a person diabetes based on the percentage for their risk
    def addDiabetes():
        diabetesDistr = open("diabetes.dat", "r")
        distr = {}
        for lines in diabetesDistr:
            brackets = lines.split(",")
            distr[brackets[0]] = float(brackets[1])
        for p in peopleArray:
            for key, value in distr.items():
                range = key.split("_")
                if p.age >= int(range[0]) and p.age <= int(range[1]):
                    n = np.random.randint()
                    if n <= value:
                        p.disease.append("diabetes")
                        break
                    break

    # assigns a person kidney disease based on the percentage for their risk
    def addKidneyDisease():
        kidneyDistr = open("kidney_disease.dat", "r")
        distr = {}
        for lines in kidneyDistr:
            brackets = lines.split(",")
            distr[brackets[0]] = float(brackets[1])
        for p in peopleArray:
            for key, value in distr.items():
                range = key.split("_")
                if p.age >= int(range[0]) and p.age <= int(range[1]):
                    n = np.random.randint()
                    if n <= value:
                        p.disease.append("kidney disease")
                        break
                    break

    # assigns a person COPD based on the percentage for their risk
    def addCOPD():
        copdDistr = open("COPD.data", "r")
        distr = {}
        for lines in copdDistr:
            brackets = lines.split(",")
            distr[brackets[0]] = float(brackets[1])
        for p in peopleArray:
            for key, value in distr.items():
                range = key.split("_")
                if p.age >= int(range[0]) and p.age <= int(range[1]):
                    n = np.random.randint()
                    if n <= value:
                        p.disease.append("COPD")
                        break
                    break

    # assigns a person obesity based on the percentage for their risk
    def addObesity():
        for p in peopleArray:
            if p.age >= 18:
                n = np.random.randint()
                if n <= 0.398:
                    p.disease.append("obesity")

    # assigns a person cystic fibrosis on the percentage for their risk
    def addCysticFibrosis():
        for p in peopleArray:
            if p.age <= 44:
                N = np.random.randint()
                if n <= 0.00009504949:
                    p.disease.append("cystic fibrosis")

    # assigns a person hypertension based on the percentage for their risk
    def addHypertension():
        hypertensionDistr = open("hypertension.data", "r")
        distr = {}
        for lines in hypertensionDistr:
            brackets = lines.split(",")
            distr[brackets[0]] = float(brackets[1])
        for p in peopleArray:
            for key, value in distr.items():
                range = key.split("_")
                if p.age >= int(range[0]) and p.age <= int(range[1]):
                    n = np.random.randint()
                    if n <= value:
                        p.disease.append("hypertension")
                        break
                    break

    # assigns a person smoking based on the percentage for their risk
    def addSmoking():
        smokingDistr = open("smoking.dat", "r")
        distr = {}
        for lines in smokingDistr:
            brackets = lines.split(",")
            distr[brackets[0]] = float(brackets[1])
        for p in peopleArray:
            for key, value in distr.items():
                range = key.split("_")
                if p.age >= int(range[0]) and p.age <= int(range[1]):
                    n = np.random.randint()
                    if n <= value:
                        p.disease.append("smoking")
                        break
                    break

    # assigns a person asthma based on the percentage for their risk
    def addAsthma():
        asthmaDistr = open("asthma.dat", "r")
        distr = {}
        for lines in asthmaDistr:
            brackets = lines.split(",")
            distr[brackets[0]] = float(brackets[1])
        for p in peopleArray:
            for key, value in distr.items():
                range = key.split("_")
                if p.age >= int(range[0]) and p.age <= int(range[1]):
                    n = np.random.randint()
                    if n <= value:
                        p.disease.append("asthma")
                        break
                    break

    # assigns a person liver disease based on the percentage for their risk
    def addLiverDisease():
        liverDistr = open("liver_disease.dat", "r")
        distr = {}
        for lines in liverDistr:
            brackets = lines.split(",")
            distr[brackets[0]] = float(brackets[1])
        for p in peopleArray:
            for key, value in distr.items():
                range = key.split("_")
                if p.age >= int(range[0]) and p.age <= int(range[1]):
                    n = np.random.randint()
                    if n <= value:
                        p.disease.append("liver disease")
                        break
                    break

    # assign all diseases based on the percentage of risk
    def addDisease():
        addCancer()
        addDiabetes()
        addKidneyDisease()
        addCOPD()
        addObesity()
        addSmoking()
        addAsthma()
        addLiverDisease()
        addCysticFibrosis()
        addHypertension()
