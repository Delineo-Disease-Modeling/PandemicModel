from population import Population
from submodule import Submodule
import json
import random


class Module:

    def __init__(self, State, County, Interventions):
        self.__State = State
        self.__County = County

    def createPopulation(self):
        print("createPop function")
        Pop = Population(self.__State, self.__County).get_dict()
        return Pop

    def createSubmodules(self):
        with open("submodules.json") as file:
            subdict = json.load(file)

        subList = []
        for each in subdict:
            subList.append(Submodule(each, each[0]))
        return subList


    def movePop(self, TOD, DOW, population, facilities):
        for each in facilities:
            each.clearPeople()
        for each in population:
            fac = (random.randint(0, 19))
            facilities[fac].addPerson(population[each])

    def createFacilities(self, filename):
        # current file format: [facility type(str), capacity(int), open hours per day(list(int)), open days(list(str)), latitude(float), longitude(float), people in it(list[Person])]
        # TODO better format the .json file to make varying hours over the days of a week, and distribute permanant workers into people[]
        with open(filename) as f:
            data = json.load(f)
        facilities = dict()
        totalCapacities = 0
        openHours = {hour: set() for hour in range(24)}
        for key in data:
            # JSON file key is 1-indexed
            nextFacility = Submodule(
                int(key) - 1, facilitytype=data[key][0], capacity=data[key][1], hours=data[key][2], days=data[key][3])
            facilities[int(key) - 1] = nextFacility
            totalCapacities += data[key][1]
            hours=data[key][2]
            for h in hours:
                openHours[h].add(nextFacility)
        return facilities, totalCapacities, openHours
