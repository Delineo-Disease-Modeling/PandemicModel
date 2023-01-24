from . import person as Person
from . import module as Module
from . import ValueController
from . import submodule as Submodule
from . import phasePlan as PhasePlan
from .jsonCompressionAlgorithm import jsonCompress, jsonDecompress, get_size
import random
import json
import pickle
import pandas as pd
import math
from datetime import datetime
import sciris as sc
from bisect import bisect_left
import xlrd
import os
import copy
import hashlib
from . import db as db
poiID = 0


class MasterController:
    '''
    This class is responsible for instantiaitng a module, which is a flexible synthetic environment equivalent to a town or city. This class essentially acts
    an an API layer that kicks off and runs the simulation, and provides the functionaility necessary to package the simulation results into the formats necessary
    for communicating with the frontend and backend.
    '''
    phasePlan = PhasePlan.PhasePlan(
        3, [60, 40, 16], [99, 99, 99], [60, 45, 60])
    values = ValueController.ValueController('Oklahoma', 'Barnsdall', 650000, {
                                             "MaskWearing": False, "roomCapacity": 100, "StayAtHome": False}, 1, 0, phasePlan, 0, 0, 0, [], [], None, 0.2)
    state = values.getState()
    county = values.getCounty()
    population = values.getPopulation()

    # Default Interventions 1=100% facilitycap
    interventions = values.getInterventions()

    dayOfWeek = values.getDayOfWeek()  # Takes values 1-7 representing Mon-Sun
    # Takes values 0-23 representing the hour (rounded down)
    timeOfDay = values.getTimeOfDay()

    phasePlan = values.getPhasePlan()
    currDay = values.getCurrDay()
    phaseNum = values.getPhaseNum()
    phaseDay = values.getPhaseDay()

    infecFacilitiesTot = values.getInfecFacilitiesTot()
    infecHousesTot = values.getInfecHousesTot()

    visitMatrices = values.getVisitMatrices()  # Save matrices

    # total odds of infecting someone whom they are connected to in a household with
    averageHouseholdInfectionRate = values.getAverageHouseholdInfectionRate()

    '''TOOD: For interventions, we have to take out assigned variables and assign them based off of the values provided by user. There are a lot of assigned variables that are randomly assigned'''

    #####
    # The below booleans turn on a whole bunch of print statements, at some point this should be redesigned to so we can better target specific functions
    # loopDebugMode: targets the ridiculous amount of for-each loops we have, and should be used for seeing if the program is looping through the lists we use
    #                for looking at who's infected, not infected, etc.
    loopDebugMode = False

    # generalDebugMode: targets areas of the codebase responsible for progressing through the simulation at a high level, like going through days, facilities, etc.
    #                   Basically use this for print statements in places that won't immediately clog the terminal with thousands of lines of output
    generalDebugMode = False
    #####

    debugMode = False

    def getUserInput(self, state, county, interventions):
        '''
        This function will assign the state, county, and interventions as the user specifies
        Params:
            state - the state passed by the user
            county - the county passed by the user
            interventions - an dictionary of values corresponding to certain interventions
        '''
        self.state = state
        self.county = county
        self.interventions = interventions

    def createModule(self):
        '''
        This function will create a module with the given state, county, and interventions
        Params:
            state - the state passed by the user
            county - the county passed by the user
            interventions - an dictionary of values corresponding to certain interventions
        '''
        return Module.Module(self.state, self.county, self.debugMode, self.interventions)

    def updateTime(self):
        '''
        This function will advance the time forward one hour
        Params:
            dayOfWeek - current day of the week
            timeOfDay - the current time of day
        '''
        if self.timeOfDay == 23:
            self.dayOfWeek = self.dayOfWeek + 1
        self.timeOfDay = (self.timeOfDay + 1) % 24

    def excelToJson(self, excelfile, jsonfile):
        '''
        WILL BE REMOVED
        This function is used to read dummy data and saves it as a file
        Params:
            excelfile: .xsl to be read
            jsonfile: JSON object to be sent back to frontend
        '''
        workbook = xlrd.open_workbook(excelfile)
        workbook = xlrd.open_workbook(excelfile, on_demand=True)
        worksheet = workbook.sheet_by_index(0)
        data = {'date': [], 'newcases': []}
        for row in range(1, worksheet.nrows):
            data['date'].append({'year': worksheet.cell_value(row, 0),
                                 'month': worksheet.cell_value(row, 1),
                                 'day': worksheet.cell_value(row, 2)})
            data['newcases'].append(worksheet.cell_value(row, 3))
        df = pd.DataFrame(data)
        result = df.to_json(orient="records")
        type_dict = {'school': 23, 'restaurant': 10, 'gym': 38, 'bar': 29}
        json_data = {'case distribution':
                     [{'label': label, 'value': value}
                         for label, value in type_dict.items()],
                     'initial_cases': 0, 'data': result}
        with open(jsonfile, 'w') as outfile:
            json.dump(json_data, outfile)

    def return_json(self, location):
        '''
        Returns a JSON file
        Params:
            location: geographical location that the excel file covers
        '''
        excel_file = location + ' Data.xls'
        json_file = location + ' Data.json'
        self.excelToJson(excel_file, json_file)
        file = open(json_file, 'r')
        return file

    def jsonResponse(self, response):
        '''
        Form json response
        Usage:
            jsonResponse(infectionInFacilitiesHourly)
        Parameters:
            response (obj): Data to load into response. May be of any form accepted by the json.dumps() function
        Returns:
            string: string containing json response of the form {"Response": data}
        '''
        return json.dumps(response)

    def jsonResponseToFile(self, response, filename):
        '''
        Form json response and write to a file
        Usage:
            jsonResponse(infectionInFacilitiesHourly, file)
        Parameters:
            response (obj): Data to load into response. May be of any form accepted by the json.dumps() function
            filename (string): filename to write response to
        '''
        response = self.jsonResponse(response)
        file = open(filename, 'w')
        file.write(response)
        file.close()

    def loadVisitMatrix(self, filename):
        '''
        Load full visit matrix from a pickle file
        Parameters:
            filename (string): pickle file to read from
        Returns:
            (obj): visit matrix with CBGs in x-axis and POIs in y-axis,
        '''
        file = open(filename, 'rb')
        self.visitMatrices = pickle.load(file)
        file.close()

        self.poi_cbg_visit_matrix_history = self.visitMatrices['poi_cbg_visit_matrix_history']
        self.cbgs_idxs_to_ids = self.visitMatrices['cbgs_idxs_to_ids']
        self.pois_idxs_to_ids = self.visitMatrices['pois_idxs_to_ids']

    def BinSearch(self, a, x):
        '''
        Used to speed up calcInfectionsHomes because Python does a linear search for checking lists
        '''
        # print("what u do ")
        # print(a, x)
        i = bisect_left(a, x)
        if i != len(a) and a[i] == x:
            return i
        else:
            return -1

    def in_list(self, item_list, item):
        '''
        Using a binary search to find items in lists, used in calcInfectionsHomes
        '''
        return self.BinSearch(item_list, item) != -1

    def calcInfectionsHomes(self, atHomeIDs, Pop, currentInfected):
        '''
        Used in the simulation() function. Is responsible for handling the spread of infection within household groups.
        Params:
            atHomeIDs - list of people who are at home
            Pop - list of people in the population
            currentInfected - list of people who are currently infected
        Returns:
            (list): list of people who are infected
        '''
        numperhour = 0
        newlyinfectedathome = []

        # TODO: this math needs to be worked out more, along with correct, scientific numbers

        ##### generalDebugMode #####
        if self.generalDebugMode:
            print('===master.py/calcInfectionsHomes: currentInfected length is ',
                  len(currentInfected), '===')
        ##### generalDebugMode #####

        # For each person that's currently infected, we have to loop through their household group and calculate the chance that
        # the people they share living spaces with get infected
        for current in currentInfected:
            id = 0
            try:
                id = current.getID()["ID"]
            except:
                id = current.getID()

            if self.in_list(atHomeIDs, id) and 0 <= current.getInfectionState() <= 3:
                # id's #someone should check that this list is behaving 7/14
                household_group = list(current.getHouseholdMembers())
                r = random.randint(1, 24)
                if r <= 2:
                    # Right now, r determines the chance that someone in household_group gets put on infection track
                    neighborhouse = list(current.getextendedhousehold())[
                        random.randint(0, len(current.getextendedhousehold())-1)]
                    for each in Pop[neighborhouse].getHouseholdMembers():
                        household_group.append(each)

                for each in household_group:

                    ##### loopDebugMode #####
                    if self.loopDebugMode:
                        print(
                            '===master.py/calcInfectionsHomes: looping household_group===')
                    ##### loopDebugMode #####

                    if len(Pop[each].getInfectionTrack()) > 0:
                        continue
                    if (Pop[each].getVaccinatedStatus()):
                        # Multiplying by 20 increases householdRandomVariable, decreasing the chance of infection
                        householdRandomVariable = 20 * random.random()
                    else:
                        householdRandomVariable = random.random()

                    if (householdRandomVariable < (self.averageHouseholdInfectionRate / (24 * (len(
                            current.getInfectionTrack()) - current.getIncubation()))) and self.in_list(atHomeIDs, each)):  # Probability of infection if in same house at the moment
                        Pop[each].assignTrajectory()
                        newlyinfectedathome.append(Pop[each])
                        numperhour += 1

        return newlyinfectedathome

    def update_status(self, interventions, currentInfected, tested):
        '''
        Update everyone's infection status at the beginning of each day
        Params:
            interventions: dictionary of interventions
            currentInfected: list of all currently infected agents
            tested: set of all agents that have been tested for infection
        Returns:
            currentInfected: updated currentInfected set
            tested: updated tested set
        '''
        toremove = []

        ##### Debug added 7/14 ####
        if self.generalDebugMode:
            print('===master.py/update_status: length of currentInfected',
                  len(currentInfected), '===')
        ##### Debug added 7/14 ####

        for person in currentInfected:
            ### Debug added 7/14 ####
            if self.loopDebugMode:
                print('===master.py/update_status: looping currentInfected===')

            timer = person.incrementInfectionTimer()
            state = person.setInfectionState(person.getInfectionTrack()[timer])
            if state == 4:
                # If recovered, remove from infected list
                toremove.append(person)
            else:
                r = random.random()
                if r <= interventions["dailyTesting"] / 100 * .1 + (interventions["dailyTesting"] / 100) * (
                        interventions["contactTracing"] / 100) * .1:
                    tested.add(person)

        for person in toremove:
            #### Debug added 7/14 ####
            if self.loopDebugMode:
                print('===master.py/update_status: looping toremove===')
            ####

            # a person has recovered at this point
            currentInfected.remove(person)

        return (currentInfected, tested)

    def move_people(self, facilities, Pop, interventions, daysDict, openHours, dayOfWeek, hourOfDay, hourOfWeek, isAnytown):
        '''
        Add people to facilities based on data in visit matrices. Loads in the data matrix and uses df.apply() to dump people into POI columns
        Params:
            facilities: dictionary of facilities
            Pop: list of people in the population
            interventions: dictionary of interventions
            daysDict: dictionary of days
            openHours: list of open hours
            dayOfWeek: day of the week
            hourOfDay: hour of the day
            hourOfWeek: hour of the week
            isAnytown: boolean, whether or not the simulation is in the Anytown scenario
        '''

        # Array of facility submodules that are both open and not full
        openFacilities = {id: facility for id, facility in facilities.items()
                          # Finds days of week facility is open
                          if daysDict[dayOfWeek] in facility.getDays()
                          and facility in openHours[hourOfDay]}  # finds hours of day that facility is open

        # A list of IDs not yet assigned to a facility
        notAssigned = [*range(len(Pop))]

        # Assign people to facilities based on visit matrices
        # mod resets h to be the hour in current week ie all mondays at midnight will be 0
        hourVisitMatrix = self.poi_cbg_visit_matrix_history[hourOfWeek % 168]
        dfVisitMatrix = pd.DataFrame(hourVisitMatrix.todense())
        # Sum all CBGs (converts dataframe to series)
        dfVisitMatrix = dfVisitMatrix.sum(axis=1)

        # Use the apply function on the dataframe to move people for each facilitiy
        dfVisitMatrix.to_frame().apply(lambda row: self.move_people_in_facility(
            facilities, notAssigned, interventions, row, Pop, openFacilities, isAnytown), axis=1)

        # returns updated facilities and notAssigned
        return (facilities, notAssigned)

    def move_people_in_facility(self, facilities, notAssigned, interventions, row, Pop, openFacilities, isAnytown):
        '''
        Takes in a specific facility and fills it to maximum capacity with people assigned to the facility. Will stop
        if it runs out of people OR the limit is reached.
        Params:
            facilities: dictionary of facilities
            notAssigned: list of IDs not yet assigned to a facility
            interventions: dictionary of interventions
            row: row of the dataframe
            Pop: list of people in the population
            openFacilities: list of open facilities
            isAnytown: boolean, whether or not the simulation is in the Anytown scenario
        '''
        poiID = row.name  # Get the POI's ID from the dataframe
        # Get the number of people at the facility from the dataframe
        numPeople = row[0]
        # Get the correct facility based on the poiID
        facility = openFacilities.get(poiID)

        # Nothing to do if any of these conditions are met
        if not notAssigned or not facility or facility.getCapacity() == facility.getVisitors():  # check if facility is already full
            return

        # Reduce number of people at facilities by factor of 2 if stay at home orders are in place
        r = 2 if interventions["stayAtHome"] else 1

        # updates number of people in facility given stay at home orders
        num_people_at_facility = math.ceil(numPeople / r)
        if isAnytown:
            # Scale population for Anytown, USA
            num_people_at_facility = math.ceil(
                num_people_at_facility * len(Pop) / 600000)

        facility_capacity = math.ceil(
            (interventions["roomCapacity"] / 100) * facility.getCapacity())  # finds slots of facility

        for _ in range(min(num_people_at_facility, facility_capacity)):
            if not notAssigned:  # Nothing to do if everyone has been assigned
                return
            # randomly determine positions to full in facility
            id_index_to_add = random.randint(0, len(notAssigned) - 1)
            # Add random person to POI
            facilities[poiID].addPerson(Pop[notAssigned.pop(id_index_to_add)])

    def write_to_simulation_db(self, city, params, response):
        response_data = copy.deepcopy(response)
        h = hashlib.sha256()
        hash_tag_unencoded = str(params).encode()
        h.update(hash_tag_unencoded)
        hash_id = h.hexdigest()
        tag = city + "_" + hash_id
        query = {"_id": {"$regex": tag}}
        collection = simulation_data.find(query)
        ids = [doc["_id"] for doc in collection]
        compressed = jsonCompress(response_data)
        print("size of compressed ->", get_size(compressed))

        if len(ids) == 0:
            idx = tag + "_" + str(1)
            simulation_data.insert_one({"_id": idx, "data": compressed})

        else:
            ids.sort(reverse=True, key=lambda x: x[x.index("_") + 1:])
            last_inserted = ids[0]
            last_inserted_id = int(
                last_inserted[last_inserted.rindex("_") + 1:])
            idx = tag + "_" + str(last_inserted_id + 1)
            simulation_data.insert_one({"_id": idx, "data": compressed})

    def get_simulation_data(self, id):
        query = {"_id": id}
        collection = simulation_data.find(query)
        docs = [doc["data"] for doc in collection]
        if len(docs) == 0:
            return f"Run with ID: {id} not found"
        else:
            return jsonDecompress(docs[0])

    def delete_simulation_run(self, id):
        query = {"_id": id}
        if (simulation_data.find(query) is not None):
            simulation_data.delete_one(query)
        else:
            return f"Run with ID: {id} not found"

    def simulation(self, num_days, currentInfected, interventions, totalInfectedInFacilities,
                   facilities, infectionInFacilitiesDaily, infectionInFacilitiesHourly,
                   peopleInFacilitiesHourly, infectionInHouseholds, facilityinfections,
                   houseinfections, infectionInFacilities, daysDict, openHours, Pop, isAnytown):
        '''
        Main simulation loop
        Params:
            num_days: number of days to simulate
            currentInfected: list of all currently infected agents
            interventions: dictionary of interventions
            totalInfectedInFacilities: dictionary of total infections in each facility
            facilities: dictionary of facilities
            infectionInFacilitiesDaily: dictionary of daily infections in each facility
            infectionInFacilitiesHourly: dictionary of hourly infections in each facility
            peopleInFacilitiesHourly: dictionary of hourly people in each facility
            infectionInHouseholds: dictionary of infections in each household
            facilityinfections: dictionary of infections in each facility
            houseinfections: dictionary of infections in each household
            infectionInFacilities: dictionary of infections in each facility
            daysDict: dictionary of days
            openHours: list of open hours
            Pop: list of people in the population
            isAnytown: boolean, whether or not the simulation is in the Anytown scenario
        '''
        # TODO: retention rate within facilities- currently no one stays in a facility longer than one hour, pending ML team

        tested = set()
        for h in range(num_days * 24):

            ### generalDebugMode ###
            if self.generalDebugMode:
                print('master.py/simulation: Hour ', h)

            if h % 24 == 0:
                currentInfected, tested = self.update_status(
                    interventions, currentInfected, tested)

            # Initialize current hour's total infections by previous hour
            totalInfectedInFacilities.append(totalInfectedInFacilities[-1])

            dayOfWeek = (h // 24) % 7
            hourOfDay = h % 24

            for id in facilities:
                ##### loopDebugMode #####
                if self.loopDebugMode:
                    print('===master.py/simulation: looping facilities 1/2===')
                facility = facilities[id]
                facility.setVisitors(0)
                facility.clearPeople()

            # Move agents throughout facilities
            facilities, notAssigned = self.move_people(
                facilities, Pop, interventions, daysDict, openHours, dayOfWeek, hourOfDay, h, isAnytown)

            # Updating the list of people infected via spread within household
            infectedathome = self.calcInfectionsHomes(
                notAssigned, Pop, currentInfected)

            # Update the currentInfected list for the whole simulation
            for each in infectedathome:
                ##### loopDebugMode #####
                if self.loopDebugMode:
                    print('===master.py/simulation: looping infectedathome===')
                ##### loopDebugMode #####
                currentInfected.add(each)

            # Updating the number of infections that occured in households this timestep
            numinfectedathome = len(infectedathome)
            houseinfections += numinfectedathome

            # Updating the list that keeps track of household infections throughout course of simulation
            if h == 0:
                infectionInHouseholds.append(numinfectedathome)
            else:
                infectionInHouseholds.append(
                    numinfectedathome + infectionInHouseholds[h - 1])

            # Loop through all facilities to assign infection spread
            for i in range(len(facilities)):

                ##### loopDebugMode #####
                if self.loopDebugMode:
                    print('===master.py/simulation: looping facilities 2/2===')

                if daysDict[dayOfWeek] not in facilities[i].getDays():
                    infectionInFacilities[i].append('Not open')
                    continue
                if facilities[i] not in openHours[hourOfDay]:
                    infectionInFacilities[i].append('Not open')
                    continue
                initialInfectionNumber = len(facilities[i].getInfected())
                finalInfectionNumber = initialInfectionNumber

                # Probability of infection in facility i
                # Probability of infection is assigned here
                prob = facilities[i].probability(interventions)

                # get number of people in facilities
                peopleInFacilitiesHourly[i][h] = len(facilities[i].getPeople())
                for person in facilities[i].getPeople():
                    ##### loopDebugMode #####
                    if self.loopDebugMode:
                        print('===master.py/simulation: looping person in facilities')
                    # Don't re-infect
                    if len(person.getInfectionTrack()) > 0:  # continue if already infected

                        continue

                    temp = random.uniform(0, 1)

                    if person.getVaccinatedStatus():
                        # effect of vaccination is 20-fold decrease in chance of infection. (95% decrease)
                        # NOTE: Multiplying by 20 is the same as dividing prob by 20, we're not increasing the
                        # chance of infection we're just getting temp into the same scale as prob
                        temp = 20 * temp

                    # temp = random.uniform(0, 1)
                    if temp < prob:  # Infect

                        person.assignTrajectory()
                        currentInfected.add(person)

                        # Update statistics
                        finalInfectionNumber += 1
                        facilityinfections += 1
                        totalInfectedInFacilities[-1] += 1
                        infectionInFacilitiesDaily[i][h // 24] += 1
                        infectionInFacilitiesHourly[i][h] += 1

                infectionInFacilities[i].append(
                    [initialInfectionNumber, finalInfectionNumber])

        return (totalInfectedInFacilities,
                facilities, infectionInFacilitiesHourly,
                peopleInFacilitiesHourly, facilityinfections,
                houseinfections, infectionInFacilities, Pop)

    def set_interventions(self, intervention_list):
        '''
         Set intervention list based on dictionary of interventions
            Params:
                intervention_list: dictionary of interventions
            Returns:
                interventions: dictionary of interventions with updated values
        '''
        if intervention_list is None:
            intervention_list = {"maskWearing": 0, "dailyTesting": 0, "roomCapacity": 100, "contactTracing": 0,
                                 "stayAtHome": False}
        if "dailyTesting" not in intervention_list:
            intervention_list["dailyTesting"] = 0
        if "maskWearing" not in intervention_list:
            intervention_list["maskWearing"] = 0
        if "roomCapacity" not in intervention_list:
            intervention_list["roomCapacity"] = 100
        if "contactTracing" not in intervention_list:
            intervention_list["contactTracing"] = 0
        if "stayAtHome" not in intervention_list:
            intervention_list["stayAtHome"] = False
        if "vaccinatedPercent" not in intervention_list:
            intervention_list["vaccinatedPercent"] = 0
        return intervention_list

    def set_households(self, Pop):
        '''
        Add people to random households who are randomly selected from population
            Params:
                Pop: list of people in the population
        '''
        for person in Pop:
            for i in range(9):
                extendedtoadd = random.randint(0, len(Pop) - 1)
                if Pop[extendedtoadd] != Pop[person] and extendedtoadd not in Pop[person].getHouseholdMembers():
                    Pop[person].addtoextendedhousehold(extendedtoadd)
                    Pop[extendedtoadd].addtoextendedhousehold(person)
        return Pop

    def run_simulation(self, city, print_infection_breakdown, isAnytown, num_days, interventions, ApiCall, usePop=False):
        '''
        Function that initializes and runs the entire simulation. Depends on simulation(), set_households(), and set_interventions(),
        move_people(), and update_status()
            Params:
                city: what city this simulation belongs to
                print_infection_breakdown: boolean, whether or not to print infection breakdown
                isAnytown: boolean, whether or not to run simulation for anytown
                num_days: number of days to run simulation for
                interventions: dictionary of interventions
            Returns:
                totalInfectedInFacilities: list of total number of infections in each facility
        '''
        interventions = self.set_interventions(interventions)

        M = self.createModule()
        Pop = {}

        # Set initial number of infected people in the module
        if city == 'Anytown':
            initialInfected = 10
        else:
            initialInfected = 100

        # Population created and returned as array of People class objects
        if usePop:
            if os.path.exists('./peopleArray.json'):  # population file exist
                # Pop = {}
                try:
                    file = open('./peopleArray.json', 'r')
                    unformated_peopleArray = json.loads(file.read())
                    for i in range(len(unformated_peopleArray)):
                        Pop[i] = Person(unformated_peopleArray[str(i)])
                        Pop[i].setAllParameters(ID=unformated_peopleArray[str(i)]['ID'], age=unformated_peopleArray[str(i)]['age'],
                                                sex=unformated_peopleArray[str(
                                                    i)]['sex'],
                                                householdLocation=unformated_peopleArray[str(
                                                    i)]['householdLocation'],
                                                householdContacts=unformated_peopleArray[str(
                                                    i)]['householdContacts'],
                                                comorbidities=unformated_peopleArray[str(
                                                    i)]['comorbidities'],
                                                demographicInfo=unformated_peopleArray[str(
                                                    i)]['demographicInfo'],
                                                severityRisk=unformated_peopleArray[str(
                                                    i)]['severityRisk'],
                                                currentLocation=unformated_peopleArray[str(
                                                    i)]['currentLocation'],
                                                vaccinated=unformated_peopleArray[str(
                                                    i)]['vaccinated'],
                                                extendedhousehold=unformated_peopleArray[str(
                                                    i)]['extendedHousehold'],
                                                COVID_type=unformated_peopleArray[str(
                                                    i)]['COVID_type'],
                                                vaccineName=unformated_peopleArray[str(
                                                    i)]['vaccineName'],
                                                shotNumber=unformated_peopleArray[str(
                                                    i)]['shotNumber'],
                                                daysAfterShot=unformated_peopleArray[str(
                                                    i)]['daysAfterShot'],
                                                essentialWorker=unformated_peopleArray[str(
                                                    i)]['essentialWorker'],
                                                madeVaccAppt=unformated_peopleArray[str(
                                                    i)]['madeVaccAppt'],
                                                vaccApptDate=unformated_peopleArray[str(
                                                    i)]['vaccApptDate'],
                                                infectionState=unformated_peopleArray[str(
                                                    i)]['infectionState'],
                                                incubation=unformated_peopleArray[str(
                                                    i)]['incubation'],
                                                disease=unformated_peopleArray[str(
                                                    i)]['disease'],
                                                infectionTimer=unformated_peopleArray[str(
                                                    i)]['infectionTimer'],
                                                infectionTrack=unformated_peopleArray[str(i)]['infectionTrack'])

                    # Displays population visualization
                    dp = displayData(population=Pop, from_json=True, file=None)
                    dp.plot_sex()  # Plots sex distribution
                except:
                    print("File error")
                finally:
                    # Close file even if error occurs
                    file.close()
        else:
            Pop = M.createPopulation(city)

        # Visit matrix: (CBG x POI) x hour = gives number people from CBG at POI in a given hour
        currentInfected = set()
        facilityinfections = 0
        houseinfections = 0

        numVaccinated = math.floor(
            (len(Pop) * interventions["vaccinatedPercent"])/100)

        # Assign initial infection state status for each person

        notInfected = [*range(len(Pop))]  # list from 1 to num in pop
        for i in range(initialInfected):
            nextInfected = notInfected.pop(random.randint(0,
                                                          len(notInfected) - 1))

            # adding to current infected
            currentInfected.add(Pop[nextInfected])
            # function which makes someone start sickness trajectory
            Pop[nextInfected].assignTrajectory()
            # Pop[nextInfected].setInfectionState()

        # randomly assigning vaccinated people
        vaccinatedIDs = random.sample(range(0, len(Pop)), numVaccinated)

        # Setting vaccinated people in population
        for v in vaccinatedIDs:
            Pop[v].setVaccinated(True)

        # Instantiate submodules with format {id: submodule}, int, {hour: set of facilities open}
        facilities, totalFacilityCapacities, openHours = M.createFacilitiesCSV(
            r'src\simulation\data\core_poi_OKCity.csv')

        # facilities, totalFacilityCapacities, openHours = M.createFacilities('submodules2.json')

        # Fill with change in infections as [initial, final] per hour
        # for each facilityID, or "Not Open" if facility is closed
        infectionInFacilities = {id: []
                                 for id in range(len(facilities.keys()))}

        # Statistics for each facility and the households
        totalInfectedInFacilities = [0]
        infectionInFacilitiesDaily = {id: [0 for day in range(num_days)]
                                      for id in range(len(facilities.keys()))}
        infectionInFacilitiesHourly = {id: [0 for hour in range(num_days*24)]
                                       for id in range(len(facilities.keys()))}
        # Number of people in each facility for every hour
        peopleInFacilitiesHourly = {id: [0 for hour in range(num_days*24)]
                                    for id in range(len(facilities.keys()))}
        # TODO: statistics for households
        infectionInHouseholds = []
        infectionInHouseholdsDaily = [0 for day in range(num_days)]

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
            houseinfections, infectionInFacilities, daysDict, openHours, Pop, isAnytown)

        print(
            f'Results for {self.county}, {self.state} over {num_days} days')  # , file=f)

        # Updated the formatting of the json file
        response = {'Buildings': [
                    {"BuildingName": str(facilities[id].getFacilityType()) + str(id),
                     "InfectedDaily": infectionInFacilitiesHourly[id],
                     "PeopleDaily": peopleInFacilitiesHourly[id]}
                    for id in range(len(facilities))]
                    }  # we should probably have households at least as one large "household"
        if not ApiCall:
            self.jsonResponseToFile(response,  r"src\simulation\output\output.json")
            print("Output written to output.txt")

        if (getDB):
            # TODO: Upload this json to a database based on interventions ran, how long, etc.
            params = city + str(isAnytown) + str(num_days) + str(interventions)
            self.write_to_simulation_db(city, params, response)

        num = 0
        for each in Pop:
            if len(Pop[each].getInfectionTrack()) > 0:
                num += 1

        # f = open("simulationOutput.txt","w")
        # if print_infection_breakdown:
        #     f.write("Initial infections:", initialInfected)
        #     f.write("Total infections in households:", houseinfections)
        #     f.write("Total infections in facilities:", facilityinfections)
        # f.write("Total infections:", num)
        # f.close()

        self.infecFacilitiesTot = totalInfectedInFacilities
        self.infecHousesTot = infectionInHouseholds

        return self.jsonResponse(response)

    # TODO: Implement an easier way to run these simultaions for difference cities
    # Function that runs anytown, OKC, or Baltimore with switch case
    # To Finish
    def create_simulation(self, city, print_infection_breakdown, num_days, intervention_list, ApiCall):
        """
        Function that runs simulation for different cities
            Params:
                city: what city this simulation should be run for, options: Anytown, Baltimore, OKC
                print_infection_breakdown: boolean, whether or not to print infection breakdown
                num_days: number of days to run simulation for
                interventions: dictionary of interventions
        """

        if city == 'Anytown':
            self.loadVisitMatrix(
                r'src\simulation\data\Anytown_Jan06_fullweek_dict.pkl')
            self.run_simulation(city='Anytown', print_infection_breakdown=print_infection_breakdown,
                                num_days=num_days, interventions=intervention_list, isAnytown=True, ApiCall=ApiCall)
        elif city == 'Oklahoma_City' or city == 'OKC':
            self.loadVisitMatrix(
                r'src\simulation\data\OKCity_Jan06_fullweek_dict.pkl')
            self.run_simulation('Oklahoma_City', print_infection_breakdown=print_infection_breakdown,
                                num_days=num_days, interventions=intervention_list, isAnytown=False, ApiCall=ApiCall)
        elif city == 'Baltimore':
            self.loadVisitMatrix(
                r'src\simulation\data\Anytown_Jan06_fullweek_dict.pkl')
            self.run_simulation('Baltimore', print_infection_breakdown=print_infection_breakdown,
                                num_days=num_days, interventions=intervention_list, isAnytown=False, ApiCall=ApiCall)
        else:
            print("Invalid city input")

    def implementPhaseDay(self, currDay, phaseNum, phaseDay, phasePlan, population, facilities):
        '''
        NOT USED CURRENTLY, SPRINT 5 BACKLOG ITEM
        This function is responsible for administering vaccines and keeping track of vaccination progress
        Params:
            currDay: current day of simulation
            phaseNum: current phase of simulation
            phaseDay: day of phase
            phasePlan: list of vaccines to be administered
            population: population of the city
            facilities: list of facilities in the city
        Returns:
            population: updated population
        '''
        # If a facility has an appointments on this day, administer appointments to each person.
        for facility in facilities:
            for i in facility.getAppointment(currDay):
                facility.administerShot(i[0], i[1])

        currDay = currDay + 1
        phaseDay = phaseDay + 1

        # if we are at the end of a phase, advance to next one, or if at last phase, stay on last phase.
        if phaseDay > phasePlan.daysInPhase[phaseNum]:
            phaseDay = 0
            phaseNum = min(phaseNum + 1, phasePlan.maxPhaseNum)

        # each person, if vaccinated, adds another day to the nunmber of days after their last shot.
        # they also schedule an appointment if they are eligible
        for person in population.peopleArray:
            if person.shotNumber == 0 or (person.shotNumber == 1 and person.vaccineName != "Johnson&Johnson" and person.daysAfterShot > 21):
                person.incrementDaysAfterShot
            if person.vaccinated != True and person.age >= phasePlan.minAge[phaseNum] and person.age >= phasePlan.maxAge[phaseNum]:
                # schedule an appointment at a random facilities some time after day
                random.randrange(0, facilities.size())
                daysAfter = random.randint(1, 14)
                facilities[i].scheduleAppointment(currDay + daysAfter)

    def runFacilityTests(self, filename):
        '''
        Test facilities by running a simulation for a number of days, and seeing how many people are infected
        Params:
            filename: name of file to save results to
        '''
        M = self.createModule()

        facilities, totalCapacities, openHours = M.createFacilitiesTXT(
            filename, False)
        self.testFacilitiesByCategory(facilities, 'Full-Service Restaurants')
        self.testDayTimeAvailability(openHours, 'T', 11)
        self.testFacilitiesByType(facilities, 'Church')

    def testDayTimeAvailability(self, openHours, day, hour):
        sc.heading("Testing facilities open on " + str(day) + ", "+str(hour))
        validFacilities = []
        for facility in openHours[hour]:
            if day in facility.getDays():
                validFacilities.append(facility.getID())
        print(len(validFacilities))

    def testFacilitiesByCategory(self, facilities, category):
        sc.heading("Testing facilities with category " + category)
        found = []
        for facility in facilities.values():
            if category in facility.categories:
                found.append(facility.getID())
        print(len(found))

    def testFacilitiesByType(self, facilities, facType):
        sc.heading("Testing facilities with type: " + facType)
        found = []
        for facility in facilities.values():
            if (facility.getFacilityType() == facType):
                found.append(facility.getID())
        print("Should find: 495")
        print("Found: " + str(len(found)))

    def sumVisitMatrices(self):
        '''
        For each POI in the visit matrices, add together all the people in the CBGs
        Notes: x-axis (cols) is CBGs, y-axis (rows) is POIs
            dfVisitMatrix.sum(axis=0) for column-wise sum
            dfVisitMatrix.sum(axis=1) for row-wise sum
        '''
        totals = []

        # Access each visit matrix for each hour in the week (total of 168 hours)
        for hour in range(168):
            hourVisitMatrix = self.poi_cbg_visit_matrix_history[hour]
            dfVisitMatrix = pd.DataFrame(hourVisitMatrix.todense())
            # Sum up all the values in the visit matrix
            total_sum = dfVisitMatrix.to_numpy().sum()
            # Round the sum and append to the list
            totals.append(round(total_sum))

        # Uncomment the line below to print out the list of sums
        # print(totals)

    # TODO: use this to get the simulation results from the database
    # def httpRequest(self):
        # Make a GET request
        # r = requests.get('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        # Guys... you're a genius.

        # Check for error
        # if (r != 200):
            # print("Error sending HTTP request")
            # return

        # Print content
        # print(r.content)

    def return_json_okc(self):
        json_file = 'dummy.json'
        file = open(json_file, 'r')
        return file

    def __init__(self, values=None):
        if values is not None:
            values = values


'''
runTest is for testing the code base with preset values. Please run this out of test_master.py.
'''

getDB = False


def runTest():
    mc = MasterController()
    mc.runFacilityTests(r'src\simulation\data\facilites_info.txt')
    # interventions = {"maskWearing":100,"stayAtHome":True,"contactTracing":100,"dailyTesting":100,"roomCapacity": 100, "vaccinatedPercent": 50}
    mc.create_simulation('Anytown', False, 2, {}, ApiCall=True)
    mc.excelToJson(r'src\simulation\data\OKC_Data.xls',
                   r'src\simulation\data\OKC_Data.json')

    if (getDB):
        print(db.get_data())

    # Clears json from file directory, later this can be removed if file is on DB
    if os.path.exists('./peopleArray.json'):
        os.remove('./peopleArray.json')
    else:
        print("The file does not exist")


'''
runSimulation is for testing the code base with preset values. Please run this out of test_master.py.
'''


def runSimulation(location, print_infection_breakdown, num_days, intervention_list, ApiCall=False):
    mc = MasterController()
    response = mc.create_simulation(location, print_infection_breakdown,
                                    num_days, intervention_list, ApiCall=ApiCall)
    return response
