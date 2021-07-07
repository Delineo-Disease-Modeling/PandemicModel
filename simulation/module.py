from population import Population
from submodule import Submodule
import json
import random
import pandas as pd
import math
import pandas as pd
import math
from datetime import datetime

class Module:

    def __init__(self, State, County, Interventions):
        self.__State = State
        self.__County = County

    def createPopulationObj(self):
        Pop = Population(self.__State, self.__County)
        return Pop


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
                int(key), facilitytype=data[key][0], capacity=data[key][1], hours=data[key][2], days=data[key][3])
            facilities[int(key)] = nextFacility
            totalCapacities += data[key][1]
            hours=data[key][2]
            for h in hours:
                openHours[h].add(nextFacility)
        return facilities, totalCapacities, openHours

    def createFacilitiesCSV(self, filename):
        df = pd.read_csv(filename)
        dfList = df.values.tolist()
        facilities = dict()
        totalCapacities = 0
        openHours = {hour: set() for hour in range(24)}
        capacities = {
            "Full Service Restaurants": 20,
            "Offices of Physicians (except Mental Health Specialists)": 60
        }
        key = 0
        for row in dfList:
            categoryList = {}
            if isinstance(row[18], str):
                categoryList = str(row[18]).split(',')
            hours = []
            days = []
            cap = 0
            if isinstance(row[17], str):
                hours = json.loads(str(row[17]))
                days = list(hours.keys())

            if isinstance(row[7], str):
                if "Restaurant" in row[6]:
                    cap = 20
                elif "Physicians" in row[6]:
                    cap = 60
                elif "Grocery" in row[6]:
                    cap = 50;
                elif "Retail" in row[6]:
                    cap = 20
                elif "School" in row[6]:
                    cap = 20
                elif "Gym" in row[6]:
                    cap = 30
                totalCapacities += cap
            nextFacility = Submodule(id = int(key), facilitytype = row[7], capacity=cap, latitude = row[9], longitude = row[10], categories = categoryList, hours = hours, days = days)
            facilities[int(key)] = nextFacility
            if days:
                for timeInterval in hours[days[0]]:
                    start = int(timeInterval[0].split(':')[0])
                    end = int(timeInterval[1].split(':')[0])
                    for i in range(start, end):
                        openHours[i].add(nextFacility)
            key = key + 1
       
        return facilities, totalCapacities, openHours
        # print(alist)

