from person import Person
from module import Module
from submodule import Submodule
from phasePlan import PhasePlan
import random
import json
import pickle
import pandas as pd
import math
from datetime import datetime
import sciris as sc
from bisect import bisect_left
import xlrd
import sys


poiID = 0

class MasterController:
    '''
    This class is responsible for instantiaitng a module, which is a flexible synthetic environment equivalent to a town or city. This class essentially acts
    an an API layer that kicks off and runs the simulation, and provides the functionaility necessary to package the simulation results into the formats necessary
    for communicating with the frontend.
    '''

    state = 'Oklahoma'
    county = 'Barnsdall'
    population = 650000

    interventions = {"MaskWearing": False,"roomCapacity": 100, "StayAtHome": False}  # Default Interventions 1=100% facilitycap

    dayOfWeek = 1  # Takes values 1-7 representing Mon-Sun
    timeOfDay = 0  # Takes values 0-23 representing the hour (rounded down)

    phasePlan = PhasePlan(3, [60, 40, 16], [99, 99, 99], [60, 45, 60])
    currDay = 0
    phaseNum = 0
    phaseDay = 0

    infecFacilitiesTot = []
    infecHousesTot = []

    visitMatrices = None # Save matrices

    #####
    # The below booleans turn on a whole bunch of print statements, at some point this should be redesigned to so we can better target specific functions
    # loopDebugMode: targets the ridiculous amount of for-each loops we have, and should be used for seeing if the program is looping through the lists we use
    #                for looking at who's infected, not infected, etc.
    loopDebugMode = False

    # generalDebugMode: targets areas of the codebase responsible for progressing through the simulation at a high level, like going through days, facilities, etc.
    #                   Basically use this for print statements in places that won't immediately clog the terminal with thousands of lines of output
    generalDebugMode = True
    #####
     
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
        return Module(self.state, self.county, self.interventions)

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
                     [{'label': label, 'value': value} for label, value in type_dict.items()],
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
        Used in the simulation() function. Is responsible for handling the spread of infection within household groups right
        '''
        numperhour = 0
        newlyinfectedathome = []

        # TODO: this math needs to be worked out more, along with correct, scientific numbers
        averageinfectionrate = .2  # total odds of infecting someone whom they are connected to in a household with

        ##### generalDebugMode #####
        if self.generalDebugMode:
            print('===master.py/calcInfectionsHomes: currentInfected length is ', len(currentInfected),'===')
        ##### generalDebugMode #####

        # For each person that's currently infected, we have to loop through their household group and calculate the chance that
        # the people they share living spaces with get infected
        for current in currentInfected:
            
            if self.in_list(atHomeIDs, current.getID()) and 0 <= current.getInfectionState() <= 3:
                household_group = list(current.getHouseholdMembers()) #id's #someone should check that this list is behaving 7/14
                r = random.randint(1,24)
                if r <= 2:
                    # Right now, r determines the chance that someone in household_group gets put on infection track
                    neighborhouse = list(current.getextendedhousehold())[random.randint(0, len(current.getextendedhousehold())-1)]
                    for each in Pop[neighborhouse].getHouseholdMembers():
                        household_group.append(each)

                for each in household_group:

                    ##### loopDebugMode #####
                    if self.loopDebugMode:
                        print('===master.py/calcInfectionsHomes: looping household_group===')
                    ##### loopDebugMode #####

                    if len(Pop[each].getInfectionTrack()) > 0:
                        continue
                    if (Pop[each].getVaccinatedStatus()):
                        householdRandomVariable = 20 * random.random() # Multiplying by 20 increases householdRandomVariable, decreasing the chance of infection
                    else:
                        householdRandomVariable = random.random()

                    if (householdRandomVariable < (averageinfectionrate / (24 * (len(
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
            print('===master.py/update_status: length of currentInfected', len(currentInfected), '===')
        ##### Debug added 7/14 ####

        for person in currentInfected:
            ### Debug added 7/14 ####
            if self.loopDebugMode:
                 print('===master.py/update_status: looping currentInfected===')

            timer = person.incrementInfectionTimer()
            state = person.setInfectionState(person.getInfectionTrack()[timer])
            if state == 4:
                toremove.append(person)  # If recovered, remove from infected list
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

            currentInfected.remove(person) # a person has recovered at this point

        return (currentInfected, tested)

    def move_people(self, facilities, Pop, interventions, daysDict, openHours, dayOfWeek, hourOfDay, h, isAnytown):
        '''
        Add people to facilities based on data in visit matrices. Loads in the data matrix and uses df.apply() to dump people into POI columns
        '''

        # Array of facility submodules that are both open and not full
        openFacilities = {id: facility for id, facility in facilities.items()
                          if daysDict[dayOfWeek] in facility.getDays()
                          and facility in openHours[hourOfDay]}

        # A list of IDs not yet assigned to a facility
        notAssigned = [*range(len(Pop))]

        # Assign people to facilities based on visit matrices
        hourVisitMatrix = self.poi_cbg_visit_matrix_history[h % 168]  # mod resets h to be the hour in current week ie all mondays at midnight will be 0
        dfVisitMatrix = pd.DataFrame(hourVisitMatrix.todense())
        dfVisitMatrix = dfVisitMatrix.sum(axis=1)  # Sum all CBGs (converts dataframe to series)

        # Use the apply function on the dataframe to move people for each facilitiy
        dfVisitMatrix.to_frame().apply(lambda row: self.move_people_in_facility(facilities, notAssigned, interventions, row, Pop, openFacilities, isAnytown), axis=1)

        return (facilities, notAssigned)

    def move_people_in_facility(self, facilities, notAssigned, interventions, row, Pop, openFacilities, isAnytown):
        '''
        Takes in a specific facility and fills it to maximum capacity with people assigned to the facility. Will stop
        if it runs out of people OR the limit is reached.
        '''
        poiID = row.name  # Get the POI's ID from the dataframe
        numPeople = row[0]  # Get the number of people at the facility from the dataframe
        facility = openFacilities.get(poiID)  # Get the correct facility based on the poiID

        # Nothing to do if any of these conditions are met
        if not notAssigned or not facility or facility.getCapacity() == facility.getVisitors():
            return

        # Reduce number of people at facilities by factor of 2 if stay at home orders are in place
        r = 2 if interventions["stayAtHome"] else 1

        num_people_at_facility = math.ceil(numPeople / r)
        if isAnytown:
            num_people_at_facility = math.ceil(num_people_at_facility * len(Pop) / 600000) # Scale population for Anytown, USA

        facility_capacity = math.ceil((interventions["roomCapacity"] / 100) * facility.getCapacity())

        for _ in range(min(num_people_at_facility, facility_capacity)):
            if not notAssigned:  # Nothing to do if everyone has been assigned
                return
            id_index_to_add = random.randint(0, len(notAssigned) - 1)
            facilities[poiID].addPerson(Pop[notAssigned.pop(id_index_to_add)])  # Add random person to POI

    def simulation(self, num_days, currentInfected, interventions, totalInfectedInFacilities,
                    facilities, infectionInFacilitiesDaily, infectionInFacilitiesHourly,
                    peopleInFacilitiesHourly, infectionInHouseholds, facilityinfections,
                    houseinfections, infectionInFacilities, daysDict, openHours, Pop, isAnytown):

        '''
        Main simulation loop
        '''

        # TODO: retention rate within facilities- currently no one stays in a facility longer than one hour, pending ML team

        tested = set()
        for h in range(num_days * 24):

            ### generalDebugMode ###
            if self.generalDebugMode:
                print('master.py/simulation: Hour ', h)

            if h % 24 == 0:
                currentInfected, tested = self.update_status(interventions, currentInfected, tested)

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
            facilities, notAssigned = self.move_people(facilities, Pop, interventions, daysDict, openHours, dayOfWeek, hourOfDay, h, isAnytown)

            # Updating the list of people infected via spread within household 
            infectedathome = self.calcInfectionsHomes(notAssigned, Pop, currentInfected)

            # Update the currentInfected list for the whole simulation
            for each in infectedathome:
                ##### loopDebugMode #####
                if self.loopDebugMode:
                    print('===master.py/simulation: looping infectedathome===')
                ##### loopDebugMode #####
                currentInfected.add(each)

            numinfectedathome = len(infectedathome) # Updating the number of infections that occured in households this timestep
            houseinfections += numinfectedathome 

            # Updating the list that keeps track of household infections throughout course of simulation
            if h == 0:
                infectionInHouseholds.append(numinfectedathome)
            else:
                infectionInHouseholds.append(numinfectedathome + infectionInHouseholds[h - 1])

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
                prob = facilities[i].probability(interventions)  # Probability of infection is assigned here

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
        Add people to households
        '''
        for person in Pop:
            for i in range(9):
                extendedtoadd = random.randint(0, len(Pop) - 1)
                if Pop[extendedtoadd] != Pop[person] and extendedtoadd not in Pop[person].getHouseholdMembers():
                    Pop[person].addtoextendedhousehold(extendedtoadd)
                    Pop[extendedtoadd].addtoextendedhousehold(person)
        return Pop

    def run_simulation(self, city, print_infection_breakdown, isAnytown, num_days=7, interventions=None):
        '''
        Function that initializes and runs the entire simulation. Depends on simulation(), set_households(), and set_interventions(),
        move_people(), and update_status()
        '''
        interventions = self.set_interventions(interventions)

        M = self.createModule()

        #Set initial number of infected people in the module
        if city == 'Anytown':
            initialInfected = 10
        else:
            initialInfected = 100 

        # Population created and returned as array of People class objects
        Pop = M.createPopulation(city)

        # Visit matrix: (CBG x POI) x hour = gives number people from CBG at POI in a given hour
        currentInfected = set()
        facilityinfections = 0
        houseinfections = 0

        numVaccinated = math.floor( (len(Pop) * interventions["vaccinatedPercent"])/100)

        # Assign initial infection state status for each person
        
        notInfected = [*range(len(Pop))] # list from 1 to num in pop
        for i in range(initialInfected):
            nextInfected = notInfected.pop(random.randint(0,
                                                len(notInfected) - 1))

            currentInfected.add(Pop[nextInfected]) #adding to current infected
            Pop[nextInfected].assignTrajectory() #function which makes someone start sickness trajectory
            #Pop[nextInfected].setInfectionState()

        vaccinatedIDs = random.sample(range(0, len(Pop)), numVaccinated) #randomly assigning vaccinated people

        # Setting vaccinated people in population
        for v in vaccinatedIDs:
            Pop[v].setVaccinated(True)


        # Instantiate submodules with format {id: submodule}, int, {hour: set of facilities open}
        facilities, totalFacilityCapacities, openHours = M.createFacilitiesCSV('core_poi_OKCity.csv') 

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
        #Number of people in each facility for every hour
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

        #Updated the formatting of the json file
        response = {'Buildings': [
                    {"BuildingName": str(facilities[id].getFacilityType()) + str(id),
                    "InfectedDaily": infectionInFacilitiesHourly[id],
                    "PeopleDaily": peopleInFacilitiesHourly[id]}
                    for id in range(len(facilities))]
                    } #we should probably have households at least as one large "household"

        self.jsonResponseToFile(response, "output.txt")

        num = 0
        for each in Pop:
            if len(Pop[each].getInfectionTrack()) > 0:
                num += 1

        if print_infection_breakdown:
            print("Initial infections:", initialInfected)
            print("Total infections in households:", houseinfections)
            print("Total infections in facilities:", facilityinfections)
            output['Initial infections'] = initialInfected
            output['Total infections in households'] = houseinfections
            output['Total infections in facilities'] = facilityinfections
            
        print("Total infections:", num)
        output['Total infections'] = num
        self.infecFacilitiesTot= totalInfectedInFacilities
        self.infecHousesTot= infectionInHouseholds

        return response

    # Function to run Anytown
    def Anytown(self, print_infection_breakdown, num_days, intervention_list):
        self.loadVisitMatrix('Anytown_Jan06_fullweek_dict.pkl')
        self.run_simulation(city='Anytown', print_infection_breakdown=print_infection_breakdown, num_days=num_days, interventions=intervention_list, isAnytown = True)

    # Function to run Oklahoma City
    def Run_OKC(self, print_infection_breakdown, num_days, intervention_list):
        self.loadVisitMatrix('Oklahoma_Jan06_fullweek_dict.pkl')
        self.run_simulation('Oklahoma_City', print_infection_breakdown=print_infection_breakdown, num_days=num_days, interventions=intervention_list, isAnytown = False)

    def implementPhaseDay(self, currDay, phaseNum, phaseDay, phasePlan, population, facilities):
        '''
        NOT USED CURRENTLY, SPRINT 5 BACKLOG ITEM
        This function is responsible for administering vaccines and keeping track of vaccination progress
        '''
        #If a facility has an appointments on this day, administer appointments to each person.
        for facility in facilities:
            for i in facility.getAppointment(currDay):
                facility.administerShot(i[0], i[1])

        currDay = currDay + 1
        phaseDay = phaseDay + 1

        #if we are at the end of a phase, advance to next one, or if at last phase, stay on last phase.
        if phaseDay > phasePlan.daysInPhase[phaseNum]:
            phaseDay = 0
            phaseNum = min(phaseNum + 1, phasePlan.maxPhaseNum)

        #each person, if vaccinated, adds another day to the nunmber of days after their last shot.
        #they also schedule an appointment if they are eligible
        for person in population.peopleArray:
            if person.shotNumber == 0 or (person.shotNumber == 1 and person.vaccineName != "Johnson&Johnson" and person.daysAfterShot > 21):
                person.incrementDaysAfterShot
            if person.vaccinated != True and person.age >= phasePlan.minAge[phaseNum] and person.age >= phasePlan.maxAge[phaseNum]:
                #schedule an appointment at a random facilities some time after day
                random.randrange(0, facilities.size())
                daysAfter = random.randint(1, 14)
                facilities[i].scheduleAppointment(currDay + daysAfter)

    def runFacilityTests(self, filename):
        '''
        Test facilities
        '''
        M = self.createModule()

        facilities, totalCapacities, openHours = M.createFacilitiesTXT(filename, False)
        self.testFacilitiesByCategory(facilities, 'Full-Service Restaurants')
        self.testDayTimeAvailability(openHours, 'T', 11)
        self.testFacilitiesByType(facilities, 'Church')

    def testDayTimeAvailability(self, openHours, day, hour):
        sc.heading("Testing facilities open on "+  str(day)+  ", "+str(hour))
        validFacilities = []
        for facility in openHours[hour]:
            if day in facility.getDays():
               validFacilities.append(facility.getID())
        print(len(validFacilities))
        output['Testing facilities open on '] = (day,hour)
    def testFacilitiesByCategory(self, facilities, category):
        sc.heading("Testing facilities with category " + category)
        found = []
        for facility in facilities.values():
            if category in facility.categories:
                found.append(facility.getID())
        print(len(found))
       
        heading = 'Testing facilities with category '
        heading += category
        output[heading] = len(found)
    def testFacilitiesByType(self, facilities, facType):
        sc.heading("Testing facilities with type: " + facType)
        found = []
        for facility in facilities.values():
            if (facility.getFacilityType() == facType):
                found.append(facility.getID())
        print("Should find: 495")
        print("Found: " + str(len(found)))
       
        output['Should find'] = 495
        output['Found'] = str(len(found))
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
            total_sum = dfVisitMatrix.to_numpy().sum()  # Sum up all the values in the visit matrix
            totals.append(round(total_sum))  # Round the sum and append to the list

        # Uncomment the line below to print out the list of sums
        # print(totals)
    def outputToJson(self,jsonFile):
        print(output)
        with open(jsonFile,'w') as outputFile:
            json.dump(output,outputFile)
    
if __name__ == '__main__':
    mc = MasterController()  # Instantiate a MasterController
    
    output = {}
    #mc.sumVisitMatrices()  # Verify correctness of visit matrices
    interventions = {}
    
    #interventions = {"maskWearing":100,"stayAtHome":True,"contactTracing":100,"dailyTesting":100,"roomCapacity": 100, "vaccinatedPercent": 50}
    mc.runFacilityTests('facilities_info.txt')
    
    #mc.Run_OKC(print_infection_breakdown=False, num_days=61, intervention_list=interventions)  # Run entire simulation for 61 days
    mc.outputToJson('Output.json')
    mc.excelToJson('OKC Data.xls', 'OKC Data.json')

