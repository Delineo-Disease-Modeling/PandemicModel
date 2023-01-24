from . import population as Population
from . import submodule as Submodule
import json
import random
import pandas as pd
import math
import pandas as pd
import math
from datetime import datetime

# Description:
#   This module represents the populations of the simulation. It contains the population and the submodules that are used to create the facilties of the simulation from several files.
#   This module has these capabilities: Creating a population, moving a population, creating facilties for the population


class Module:

    # Initalizer for the module with parameters for the state and county
    def __init__(self, State, County, debugMode, Interventions):
        self.__State = State
        self.__County = County
        self.debugMode = debugMode

    def createPopulationObj(self):  # Creates a population object
        Pop = Population.Population(self.__State, self.__County, self.debugMode)
        return Pop

    def createPopulation(self, city):  # Creates a population object for a specific city
        print("createPop function")
        if city == 'Anytown':
            Pop = Population.Population(self.__State, self.__County,
                             self.debugMode).get_dict()
        if city == 'Oklahoma_City':
            Pop = Population.Population(self.__State, self.__County,  self.debugMode, num_households=250000,
                             npop=650000, num_workplaces=24000).get_dict()
        return Pop

    # Creates a submodule object for every facility to be used in the simulation
    def createSubmodules(self):
        with open("submodules.json") as file:
            subdict = json.load(file)

        subList = []
        for each in subdict:
            subList.append(Submodule(each, each[0]))
        return subList

    # Moves the population from one facility to another randomly by first clearing the facility, then adding the population to the new facility
    def movePop(self, TOD, DOW, population, facilities):
        for each in facilities:
            each.clearPeople()
        for each in population:
            fac = (random.randint(0, 19))
            facilities[fac].addPerson(population[each])

    # Creates a facility object for every facility in the txt file
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
            hours = data[key][2]
            for h in hours:
                openHours[h].add(nextFacility)
        return facilities, totalCapacities, openHours

    # Creates a facility object for every facility in the txt file. Data is based off of the txt file
    def createFacilitiesTXT(self, filename, verbose):
        with open(filename) as f:
            lines = f.readlines()
            lines = lines[:-1]
        totalCapacities = 0
        openHours = {hour: set() for hour in range(24)}
        category = []
        category_num = []
        for row in lines:
            split_row = row.split("  ")
            category.append(split_row[0])
            category_num.append(int(split_row[len(split_row) - 1].strip("\n")))

        facilities = dict()
        hours = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
        days = ["M", "T", "W", "Th", "F", "Sat", "Sun"]
        index = 0
        counter = 0
        facilities_ID = 0
        facility_type = ''

        # create facilities of each category

        # TODO: We might have to assign this based off of what Info support finds for us

        while (index < len(category)):
            counter = 0
            # create n facilities depending on the value in category_num
            while (counter < category_num[index]):
                if "Restaurant" in category[index] or "Bars" in category[index] or "Drinking Places" in category[index]:
                    facility_type = 'Restaurant'
                    cap = 20
                elif "Physicians" in category[index] or "Hospitals" in category[index] or "Health" in category[index] or "Ambulatory Surgical and Emergency" in category[index] or "Kidney Dialysis Centers" in category[index]:
                    facility_type = 'Hospital'
                    cap = 60
                elif "Grocery" in category[index] or "Markets" in category[index]:
                    facility_type = 'Supermarket'
                    cap = 50
                elif "Retail" in category[index] or "Stores" in category[index] or "Wholesalers" in category[index] or "Carriers" in category[index] or "Florists" in category[index]:
                    facility_type = 'Retail'
                    cap = 20
                elif "School" in category[index] or "Child" in category[index] or "Colleges" in category[index]:
                    facility_type = 'School'
                    cap = 20
                elif "Religious" in category[index]:
                    facility_type = 'Church'
                    cap = 30
                elif "Gym" in category[index] or "Weight Reducing Centers" in category[index]:
                    facility_type = 'Gym'
                    cap = 30
                # default for facilities with categories not represented in submodule.py # UPDATE NOT DOING THIS #
                else:
                    # If facility type does not appear in submodule.py we should skip it #
                    break
                    # facility_type = 'Other'
                    # cap = 20

                totalCapacities += cap
                nextFacility = Submodule.Submodule(id=facilities_ID, facilitytype=facility_type, debugMode = self.debugMode,
                                         capacity=cap, categories=category[index], hours=hours, days=days)
                facilities[facilities_ID] = nextFacility
                for h in hours:
                    openHours[h].add(nextFacility)
                facilities_ID += 1
                counter += 1
            index += 1

        if verbose:
            print(len(facilities))

        # There are 10956 total facilities. <- there shouldn't be
        return facilities, totalCapacities, openHours

    # Creates a facility object for every facility in the csv file.
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
            else:
                hours = {"Mon": [["9:00", "17:00"]], "Tue": [["9:00", "17:00"]],
                         "Wed": [["9:00", "17:00"]], "Thu": [["9:00", "17:00"]],
                         "Fri": [["9:00", "17:00"]], "Sat": [["9:00", "17:00"]],
                         "Sun": [["9:00", "17:00"]]}
                days = list(hours.keys())

            facilityName = ""
            if isinstance(row[7], str):
                if "Restaurant" in row[6]:
                    cap = 20
                    facilityName = 'Restaurant'
                elif "Physicians" in row[6] or "Hospitals" in row[6]:
                    cap = 60
                    facilityName = 'Hospital'
                elif "Grocery" in row[6]:
                    cap = 50
                    facilityName = 'Supermarket'
                elif "Retail" in row[6]:
                    cap = 20
                    facilityName = 'Retail'
                elif "School" in row[6]:
                    cap = 20
                    facilityName = 'School'
                elif "Gym" in row[6]:
                    cap = 30
                    facilityName = 'Gym'
                # default for facilities with no categories in submodule.py
                else:
                    cap = 20
                    facilityName = 'Other'
            # default for facilities with no categories in csv file
            else:
                cap = 20
                facilityName = 'Other'
            totalCapacities += cap

            nextFacility = Submodule.Submodule(id=int(key), facilitytype=facilityName, capacity=cap,
                                     latitude=row[9], longitude=row[10], categories=categoryList, hours=hours, days=days, debugMode=self.debugMode)
            facilities[int(key)] = nextFacility
            if days:
                for timeInterval in hours[days[0]]:
                    start = int(timeInterval[0].split(':')[0])
                    end = int(timeInterval[1].split(':')[0])
                    for i in range(start, end):
                        openHours[i].add(nextFacility)
            key = key + 1

        if self.debugMode:
            print(len(facilities))

        return facilities, totalCapacities, openHours

    