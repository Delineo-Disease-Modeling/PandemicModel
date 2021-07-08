from person import Person
from module import Module
from submodule import Submodule
from phasePlan import PhasePlan
import random
import json
import pickle
import pandas as pd
import math

# Wells-Riley

# Modularized: contents can be found in simulation, set_households, set interventions,
# move_people, update_status
def WellsRiley(self, print_infection_breakdown, num_days=7, interventions=None):
    interventions = self.set_interventions(interventions)

    M = self.createModule()

    # Population created and returned as array of People class objects
    Pop = M.createPopulation()

    # Visit matrix: (CBG x POI) x hour = gives number people from CBG at POI in a given hour
    # visitMatrix = loadVisitMatrix('filename')
    currentInfected = set()
    facilityinfections = 0
    houseinfections = 0

    numVaccinated = math.floor((len(Pop) * interventions["vaccinatedPercent"]) / 100)

    # Assign initial infection state status for each person
    initialInfected = 10  # Should be customizable in  the future
    notInfected = [*range(len(Pop))]  # list from 1 to num in pop
    for i in range(initialInfected):
        nextInfected = notInfected.pop(random.randint(0,
                                                      len(notInfected) - 1))

        currentInfected.add(Pop[nextInfected])  # adding to current infected
        Pop[nextInfected].assignTrajectory()  # function which makes someone start sickness trajectory
        # Pop[nextInfected].setInfectionState()

    vaccinatedIDs = random.sample(range(0, len(Pop)), numVaccinated)  # randomly assigning vaccinated people

    # Setting vaccinated people in population
    for v in vaccinatedIDs:
        Pop[v].setVaccinated(True)

    # TODO: to pull from actual data of Oklahoma/frontend map.
    # Currently assuming a fixed number of each, and using a range of 6
    # types of facilities representing different essential level and attributes eg ventilation rate

    # Instantiate submodules with
    # {id: submodule}, int, {hour: set of facilities open}
    facilities, totalFacilityCapacities, openHours = M.createFacilities(
        'submodules2.json')

    # Fill with change in infections as [initial, final] per hour
    # for each facilityID, or "Not Open" if facility is closed
    infectionInFacilities = {id: []
                             for id in range(len(facilities.keys()))}

    # Statistics for each facility and the households
    totalInfectedInFacilities = [0]
    infectionInFacilitiesDaily = {id: [0 for day in range(num_days)]
                                  for id in range(len(facilities.keys()))}
    infectionInFacilitiesHourly = {id: [0 for hour in range(num_days * 24)]
                                   for id in range(len(facilities.keys()))}
    # Number of people in each facility for every hour
    peopleInFacilitiesHourly = {id: [0 for hour in range(num_days * 24)]
                                for id in range(len(facilities.keys()))}
    # TODO: statistics for households
    infectionInHouseholds = []
    infectionInHouseholdsDaily = [0 for day in range(num_days)]

    # ____SET HOUSEHOLDS + NETWORK STRATEGY____
    '''
    for person in Pop:
        for i in range(9):
            extendedtoadd = random.randint(0,len(Pop) - 1)
            if Pop[extendedtoadd] != Pop[person] and extendedtoadd not in Pop[person].getHouseholdMembers():
                Pop[person].addtoextendedhousehold(extendedtoadd)
                Pop[extendedtoadd].addtoextendedhousehold(person)
                # for each in Pop[extendedtoadd].getHouseholdMembers():
                 #   Pop[person].addtoextendedhousehold(each)
                 #   Pop[each].addtoextendedhousehold(person)
    '''
    Pop = self.set_households(Pop)
    daysDict = {
        0: 'Sun',
        1: 'M',
        2: 'T',
        3: 'W',
        4: 'Th',
        5: 'F',
        6: 'Sat'
    }
    numFacilities = len(facilities)

    totalInfectedInFacilities, facilities, infectionInFacilitiesHourly, peopleInFacilitiesHourly, facilityinfections, houseinfections, infectionInFacilities, Pop = self.simulation(
        num_days, currentInfected, interventions, totalInfectedInFacilities,
        facilities, infectionInFacilitiesDaily, infectionInFacilitiesHourly,
        peopleInFacilitiesHourly, infectionInHouseholds, facilityinfections,
        houseinfections, infectionInFacilities, daysDict, openHours, Pop)

    print(
        f'Results for {self.county}, {self.state} over {num_days} days')  # , file=f)

    # Updated the formatting of the json file
    response = {'Buildings': [
        {"BuildingName": str(facilities[id].getFacilityType()) + str(id),
         "InfectedDaily": infectionInFacilitiesHourly[id],
         "PeopleDaily": peopleInFacilitiesHourly[id]}
        for id in range(len(facilities))]
    }  # we should probably have households at least as one large "household"

    # response = {f'({id}, {facilities[id].getFacilityType()})': array
    # for id, array in infectionInFacilitiesHourly.items()}
    self.jsonResponseToFile(response, "output.txt")

    num = 0
    for each in Pop:
        if len(Pop[each].getInfectionTrack()) > 0:
            num += 1
            # print(Pop[each].getInfectionState(),Pop[each].getinfectionTimer(), Pop[each].getInfectionTrack())

    # f.close()

    if print_infection_breakdown:
        print("Initial infections:", initialInfected)
        print("Total infections in households:", houseinfections)
        print("Total infections in facilities:", facilityinfections)
    print("Total infections:", num)

    self.infecFacilitiesTot = totalInfectedInFacilities
    self.infecHousesTot = infectionInHouseholds