import sys
import os
import synthpops as sp
# If the above is not working, try below
# import synthpops.synthpops as sp
from  . import person as Person
import random


class Population():

    '''This class is used to define a population in the simulation.
    It takes in the following parameters:
    state: The state in which the population is located
    country: The country in which the population is located
    population: An array of different person classes
    peopleArray: A dictionary representing people in the population
    populationSize: The size of the population
    phaseNum: The phase of the population
    currPhaseDayNum: The day number of the current phase
    num_households: The number of households in the population
    npop: How many people are in the population, for synthpops
    num_workplaces: The number of workplaces in the population

    '''
    # constructor

    def __init__(self, state, country, population=[], peopleArray={}, populationSize=0, phaseNum=0, currPhaseDayNum=0, num_households=2400, npop=6000, num_workplaces=200):

        self.state = state
        self.country = country
        self.population = population  # array of different person classes
        self.peopleArray = peopleArray
        self.populationSize = populationSize
        self.phaseNum = phaseNum
        self.currPhaseDayNum = currPhaseDayNum

        self.num_households = num_households
        self.npop = npop
        self.num_workplaces = num_workplaces

        ##### Debug flag #####
        self.debugMode = True

    def get_dict(self):
        '''
        This function generates a synthetic population using synthpops for barnsdall, Oklahoma, usa and returns a corresponding dictionary. 

        Params:
            npop(int): The size of the population to be used by sp
            num_workplaces(int): The number of workplaces to be used by sp
        Returns:
            peopleArray: Dictionary of individuals (objects of the "person" class) with parameters from info available in the generated synthpops population
        '''
        sp.validate()
        datadir = sp.datadir
        location = 'barnsdall'
        state_location = 'Oklahoma'
        country_location = 'usa'
        sheet_name = 'United States of America'
        level = 'county'

        num_households = self.num_households  # 459
        npop = self.npop  # 1132 #this is 6000 - but when increased synthpops does not work
        num_workplaces = self.num_workplaces

        # TODO: default school sizes are still being used
        population, homes_dic = cn.generate_synthetic_population(npop, datadir, num_households, num_workplaces, location=location,

                                                                 state_location=state_location, country_location=country_location, sheet_name=sheet_name, use_default=True, return_popdict=True)

        peopleArray = {}
        for i in range(npop):
            person = Person(i)
            person.setSynthPopParameters(population[i])
            peopleArray[i] = person
        self.peopleArray = peopleArray

        if self.debugMode:
            print('=population.py/get_dict: peopleArray length is',
                  len(peopleArray), ' =')
        return peopleArray

    # calls synthpops and generates population (dictionary)
    def generatePopulation(self, populationSize):
        # call function from person class
        '''
        This function generates a population (dictionary) using synthpops and returns a dictionary of persons with parameters corresponding to info in
        the synthpops population
        Params:
            populationSize(int): The size of the population
        Returns:
            peopleArray(dictionary): The dictionary of persons with parameters corresponding to info in the generated synthpops population
        '''
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
        '''
        This function iterates through the people of the population and sets a random comorbidity number to each individual.
        Params:
            peopleArray(dictionary): Dictionary of persons of the population for whom a comorbidity is set.
        Return:
            comorbiditiesArray(dictionary): Dictionary of comorbidities set for the population (might still need to fix?).
        '''
        comorbiditiesArray = {}
        for i in range(len(self.peopleArray)):
            self.peopleArray[i].setComorbidities(random.randint(0, 5))
        return comorbiditiesArray

    def addDem(self):
        '''
        This function iterates through the people of the population and sets a random demographic info number to each individual.
        Params:
            peopleArray(dictionary): Dictionary o persons of the population for whom demographic info is set.
        Return:
            demographicsArray(dictionary): Dictionary of the demographics set for the population (might still need to fix?).
        '''
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

    def generateVacinationPopulation(self):
        '''
        Iterates through the information of the people in the population to assign vaccination status values for each individual.
        Params:
            peopleArray(dictionary): Dictionary of persons in the population.
            populationSize(int): Size of the current population.
        Returns:
            vaccinated(dictionary): Dictionary representing the vaccination statuses of each corresponding person in the population.
        '''
        peopleArray = self.generatePopulation(self.populationSize)
        vaccinated = {}  # create a dictionary of people and their vaccination status
        for i in range(len(peopleArray)):
            if (peopleArray[i].age > 60 or peopleArray[i].essentialWorker == True or peopleArray[i].comorbidities > 2):
                peopleArray[i].vaccinated = True
                vaccinated[peopleArray[i]] = True
            else:
                peopleArray[i].vaccinated = False
                vaccinated[peopleArray[i]] = False
        return vaccinated

    def infectedPop(self):
        '''
        Generates an infected population.
        Returns:
            infectedArray(dictionary): Dictionary of infection status for the population.
        '''
        vaccinated = self.generateVacinationPopulation()
        infectedArray = {}
        for i in vaccinated:
            if (vaccinated[i]):
                infectedArray[i] = i.infectedAfterCompletelyVaccinated()
        return infectedArray

    def incrementPhaseDayNum(self):
        '''
        Increments the phase day of the population by one.
        Params:
            currPhaseDayNum(int): The phase day number of the population, before the method is run.
        '''
        self.currPhaseDayNum += 1

    def implementPhase(self, plan):
        # maxPhaseNum will depend on how many phases there will be
        '''
        Runs the current phase in the population.
        Params:
            currPhaseDayNum(int): The phase day number of the population, before the method is run.
            plan(PhasePlan): An object of the PhasePlan class, which contains the phase plan of the simulation to run the simulation for a phase.
        '''
        while self.phaseNum < plan.maxPhaseNum:
            # phaseNumber will depend on the phase that it is in
            while self.currPhaseDayNum < plan.daysInPhase[self.phaseNum]:
                # vaccinate function constantly while in the phase
                self.incrementPhaseDayNum()

            self.currPhaseDayNum = 0
            self.phaseNum += 1
