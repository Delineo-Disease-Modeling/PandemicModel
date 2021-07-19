
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

poiID = 0

class MasterController:
    # MasterController class, this runs the simulation by instantiating module

    state = 'Oklahoma'
    county = 'Barnsdall'
    population = 650000
    # Uncertain exactly what/how many interventions to expect

    interventions = {"MaskWearing": False,"FacilityCap": 1, "StayAtHome": False}  # Default Interventions 1=100% facilitycap
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

    # getUserInput: This function will assign the state, county, and interventions as the user specifies
    # params:
    #   state - the state passed by the user
    #   county - the county passed by the user
    #   interventions - an array oof booleans corresponding to certain interventions (size TBD)
    def getUserInput(self, state, county, interventions):
        self.state = state
        self.county = county
        self.interventions = interventions

    # createModules: This function will create a module with the given state, county, and interventions
    # params:
    #   state - the state passed by the user
    #   county - the county passed by the user
    #   interventions - an array oof booleans corresponding to certain interventions (size TBD)
    def createModule(self):
        return Module(self.state, self.county, self.interventions)

    # updateTime: This function will advance the time forward one hour
    # params:
    #   dayOfWeek - current day of the week
    #   timeOfDay - the current time of day
    def updateTime(self):
        if self.timeOfDay == 23:
            self.dayOfWeek = self.dayOfWeek + 1
        self.timeOfDay = (self.timeOfDay + 1) % 24

    # runSim: This function runs the simulation over a desired time interval
    # params:
    #   interval - the number of hours to run the simulation for
    #   population - the population as instantiated by a Module object
    #   facilities - the facility list as instantiated by a Module object
    def runSim(self, interval, population, facilities, module):
        # for each time step, move population, create subgroups, infect the new people
        # uncertain exactly how time works
        for i in range(interval):
            module.movePop(self.dayOfWeek, self.timeOfDay,
                           population, facilities) #  Moves population at interval steps (eventually move pop will be
                                                   #  Integrated with ML team
            for facility in facilities:
                facility.createGroups() # Groups being created
                G = facility.createGraph() # Graph created
                facility.calcInfection(G)
            self.updateTime()
            if self.timeOfDay == 23:
                self.implementPhaseDay(self.currDay, self.phaseNum, self.phaseDay, self.phasePlan, population, facilities)

    def displayResult(self):
        # TODO
        print('Nothing to show yet')

    def jsonRequest(self, request):
        """ Parse json_string and store values in MasterController members
        Key strings must be valid attribute names.
        Parameters:
        request (string): Json string of the form {"Request": {"key": value, ...}}
        """
        json_dictionary = json.loads(request)['Request']
        print(json_dictionary)
        for k, v in json_dictionary.items():
            setattr(self, k, v)

    def jsonResponse(self, response):
        """ Form json response
        Usage:
        jsonResponse(infectionInFacilitiesHourly)
        Parameters:
        response (obj): Data to load into response. May be of any form accepted by the json.dumps() function
        Returns:
        string: string containing json response of the form {"Response": data}
        """
        return json.dumps(response)

    def jsonResponseToFile(self, response, filename):
        """ Form json response and write to a file
        Usage:
        jsonResponse(infectionInFacilitiesHourly, file)
        Parameters:
        response (obj): Data to load into response. May be of any form accepted by the json.dumps() function
        filename (string): filename to write to
        """
        response = self.jsonResponse(response)
        file = open(filename, 'w')
        file.write(response)
        file.close()

    def loadVisitMatrix(self, filename):
        """Load full visit matrix from a pickle file
        Parameters:
        filename (string): pickle file to read from
        Returns:
        (obj): visit matrix with CBGs in x-axis and POIs in y-axis,
        """
        file = open(filename, 'rb')
        self.visitMatrices = pickle.load(file)
        file.close()

        self.poi_cbg_visit_matrix_history = self.visitMatrices['poi_cbg_visit_matrix_history']
        self.cbgs_idxs_to_ids = self.visitMatrices['cbgs_idxs_to_ids']
        self.pois_idxs_to_ids = self.visitMatrices['pois_idxs_to_ids']
        #self.pois_ids_to_name = self.visitMatrices['pois_ids_to_name']

    def BinSearch(self, a, x):
        i = bisect_left(a, x)
        if i != len(a) and a[i] == x:
            return i
        else:
            return -1

    def in_list(self, item_list, item):
        return self.BinSearch(item_list, item) != -1

    def calcInfectionsHomes(self, atHomeIDs, Pop, currentInfected):
        numperhour = 0
        newlyinfectedathome = []
        averageinfectiouslength = 24 * 3  # number of days an individual is infectious
        averageinfectionrate = .2  # total odds of infecting someone whom they are connected to in a household with
        # note this math may need to be worked out more, along with correct, scientific numbers
        # infectedAndHome = set()

        ##### generalDebugMode #####
        if self.generalDebugMode:
            print('===master.py/calcInfectionsHomes: currentInfected length is ', len(currentInfected),'===')
        ##### generalDebugMode #####

        '''
        ##### generalDebugMode #####
        if self.generalDebugMode:
          print('===master.py/calcInfectionsHomes: infectedAndHome length is ', len(infectedAndHome),'===')
        ##### generalDebugMode #####
        '''


        for current in currentInfected:
            '''
            ##### loopDebugMode #####
            if self.loopDebugMode:
                print('===master.py/calcInfectionsHomes: looping currentInfected===')
            ##### loopDebugMode #####
            '''
            if self.in_list(atHomeIDs, current.getID()) and 0 <= current.getInfectionState() <= 3:
                currentlywith = list(current.getHouseholdMembers()) #id's #someone should check that this list is behaving 7/14
                r = random.randint(1,24)
                if r <= 2:
                    neighborhouse = list(current.getextendedhousehold())[random.randint(0, len(current.getextendedhousehold())-1)]
                    # currentlywith.append(neighborhouse)
                    for each in Pop[neighborhouse].getHouseholdMembers():
                        currentlywith.append(each)
                for each in currentlywith:
                    ##### loopDebugMode #####
                    if self.loopDebugMode:
                        print('===master.py/calcInfectionsHomes: looping currentlywith===')
                    ##### loopDebugMode #####
                    if len(Pop[each].getInfectionTrack()) > 0:
                        continue
                    if (Pop[each].getVaccinatedStatus()):
                        householdRandomVariable = 20 * random.random()
                    else:
                        householdRandomVariable = random.random()

                    if (householdRandomVariable < (averageinfectionrate / (24 * (len(
                            current.getInfectionTrack()) - current.getIncubation()))) and self.in_list(atHomeIDs, each)):  # Probability of infection if in same house at the moment
                        Pop[each].assignTrajectory()
                        newlyinfectedathome.append(Pop[each])
                        numperhour += 1
        return newlyinfectedathome

    # Update everyone's infection status at the beginning of each day
    def update_status(self, interventions, currentInfected, tested):
        toremove = []

        ##### Debug added 7/14 ####
        if self.generalDebugMode:
            print('===master.py/update_status: length of currentInfected', len(currentInfected), '===')

        for each in currentInfected:
            ### Debug added 7/14 ####
            if self.loopDebugMode:
                 print('===master.py/update_status: looping currentInfected===')

            timer = each.incrementInfectionTimer()
            state = each.setInfectionState(each.getInfectionTrack()[timer])
            r = random.random()
            if r <= interventions["dailyTesting"] / 100 * .1 + (interventions["dailyTesting"] / 100) * (
                    interventions["contactTracing"] / 100) * .1:
                tested.add(each)
            if state == 4:
                toremove.append(each)  # if recovered remove from infected list

        for each in toremove:
            ### Debug added 7/14 ####
            if self.loopDebugMode:
                 print('===master.py/update_status: looping toremove===')

            currentInfected.remove(each)
            if each in tested:
                tested.remove(each)

        return (currentInfected, tested)

    # Add people to facilities based on data in visit matrices
    def move_people(self, facilities, Pop, interventions, daysDict, openHours, dayOfWeek, hourOfDay, h):
        # Array of facility submodules that are both open and not full
        openFacilities = {id: facility for id, facility in facilities.items()
                          if daysDict[dayOfWeek] in facility.getDays()
                          and facility in openHours[hourOfDay]}

        # if openFacilities.get(0):
        #     print(str(openFacilities))

        # A list of IDs not yet assigned to a facility
        notAssigned = [*range(len(Pop))]

        # Assign people to facilities based on visit matrices
        hourVisitMatrix = self.poi_cbg_visit_matrix_history[h % 168]  # mod resets h to be the hour in current week ie all mondays at midnight will be 0
        dfVisitMatrix = pd.DataFrame(hourVisitMatrix.todense())
        dfVisitMatrix = dfVisitMatrix.sum(axis=1)  # Sum all CBGs (converts dataframe to series)

        # print("breakpoint one")

        # for poiID, numPeople in dfVisitMatrix.iteritems():
        #     facility = openFacilities.get(poiID)
        #     if not notAssigned:
        #         # what is this? 7/13
        #         # should check if notAssigned is empty, aka no more people to move. should end loop.
        #         break
        #     if not facility:
        #         continue
        #     if facility.getCapacity() == facility.getVisitors():
        #         continue
        #     r = 1
        #     if interventions["stayAtHome"]:
        #         r = 2  # Reduce number of people at facilities by factor of 2 if stay at home orders.
        #     traffic = 0
        #     for i in range(min((math.ceil(numPeople / r)), math.ceil((interventions[ #REMOVED scale, used to be numPeople * scale 7/13
        #                                                                           "roomCapacity"] / 100) * facility.getCapacity()))):  # Scale by population of OKC for now # NOT ANYMORE 7/13
        #         if not notAssigned:
        #             # what is this? 7/13
        #             break
        #         idindextoadd = random.randint(0, len(notAssigned) - 1)
        #         traffic += 1

        #         facilities[poiID].addPerson(Pop[notAssigned.pop(idindextoadd)])  # Add random person to POI for now

        #         ##### loopDebugMode #####
        #         if self.loopDebugMode:
        #             print('=== master.py/move_people: looping to add people to POI')

        # Rather than use a loop, use the apply function to move people for each facilitiy
        dfVisitMatrix.to_frame().apply(lambda row: self.move_people_in_facility(facilities, notAssigned, interventions, row, Pop, openFacilities), axis = 1)

        return (facilities, notAssigned)

    def move_people_in_facility(self, facilities, notAssigned, interventions, row, Pop, openFacilities):
        poiID = row.name  # Get the POI's ID from the dataframe
        numPeople = row[0]  # Get numPeople from the dataframe
        facility = openFacilities.get(poiID)  # Get the correct facility based on the poiID

        # Nothing to do if any of these conditions are met
        if not notAssigned or not facility or facility.getCapacity() == facility.getVisitors():
            return

        # Reduce number of people at facilities by factor of 2 if stay at home orders.
        r = 2 if interventions["stayAtHome"] else 1

        for _ in range(min((math.ceil(numPeople / r)), math.ceil((interventions["roomCapacity"] / 100) * facility.getCapacity()))):
            if not notAssigned:
                break
            idindextoadd = random.randint(0, len(notAssigned) - 1)
            facilities[poiID].addPerson(Pop[notAssigned.pop(idindextoadd)])  # Add random person to POI for now

    # Main simulation
    def simulation(self, num_days, currentInfected, interventions, totalInfectedInFacilities,
                    facilities, infectionInFacilitiesDaily, infectionInFacilitiesHourly,
                    peopleInFacilitiesHourly, infectionInHouseholds, facilityinfections,
                    houseinfections, infectionInFacilities, daysDict, openHours, Pop):

        # Main simulation loop
        # Assume movements to facilities in the day only (10:00 - 18:00)
        tested = set()
        for h in range(num_days * 24):

            ### generalDebugMode ###
            if self.generalDebugMode:
                print('master.py/simulation: Hour ', h)

            if h % 24 == 0:
                currentInfected, tested = self.update_status(interventions, currentInfected, tested)

            # Initialize current hour's total infections by previous hour
            totalInfectedInFacilities.append(totalInfectedInFacilities[-1])

            # Number of people at facilities

            # numberOut = random.randint(0, min(len(Pop)-1,
            #                       totalFacilityCapacities)) #Not used anymore

            dayOfWeek = (h // 24) % 7
            hourOfDay = h % 24

            # TODO: retention rate within the same facility. currently no one is retained - Retention rate eventually covered by ML team

            for id in facilities:
                ##### loopDebugMode #####
                if self.loopDebugMode:
                    print('===master.py/simulation: looping facilities 1/2===')
                facility = facilities[id]
                facility.setVisitors(0)
                facility.clearPeople()

            #print("breakpoint zero")

            facilities, notAssigned = self.move_people(facilities, Pop, interventions, daysDict, openHours, dayOfWeek, hourOfDay, h)

            # print(notAssigned)

            #print("breakpoint three")
            # Calculate infections for those still not assigned (assume all
            # not in a facility are at home)
            """
            #_____GRAPH VERSION______
            infectedathome = households.calcInfection(G, notAssigned) #TODO return list of persons infected
            """
            # ____SETHOUSEHOLDS_____
            infectedathome = self.calcInfectionsHomes(notAssigned, Pop, currentInfected)
            for each in infectedathome:
                ##### loopDebugMode #####
                if self.loopDebugMode:
                    print('===master.py/simulation: looping infectedathome===')
                currentInfected.add(each)
            numinfectedathome = len(infectedathome)
            houseinfections += numinfectedathome
            if h == 0:
                infectionInHouseholds.append(numinfectedathome)
            else:
                infectionInHouseholds.append(numinfectedathome + infectionInHouseholds[h - 1])

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

                prob = facilities[i].probability(interventions)  # Wells-Riley here

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

                    temp = random.uniform(0, 1)
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

    # Set intervention list based on inputs
    def set_interventions(self, intervention_list):
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

    # Add people to households
    def set_households(self, Pop):
        for person in Pop:
            for i in range(9):
                extendedtoadd = random.randint(0, len(Pop) - 1)
                if Pop[extendedtoadd] != Pop[person] and extendedtoadd not in Pop[person].getHouseholdMembers():
                    Pop[person].addtoextendedhousehold(extendedtoadd)
                    Pop[extendedtoadd].addtoextendedhousehold(person)
                    # for each in Pop[extendedtoadd].getHouseholdMembers():
                    #   Pop[person].addtoextendedhousehold(each)
                    #   Pop[each].addtoextendedhousehold(person)
        return Pop


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

        numVaccinated = math.floor( (len(Pop) * interventions["vaccinatedPercent"])/100)

        # Assign initial infection state status for each person
        initialInfected = 100  # Should be customizable in  the future
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

        # TODO: to pull from actual data of Oklahoma/frontend map.
        # Currently assuming a fixed number of each, and using a range of 6
        # types of facilities representing different essential level and attributes eg ventilation rate

        # Instantiate submodules with
        # {id: submodule}, int, {hour: set of facilities open}


        facilities, totalFacilityCapacities, openHours = M.createFacilitiesCSV('core_poi_OKCity.csv') # wasn't this changed to load the .txt? 7/13

        #facilities, totalFacilityCapacities, openHours = M.createFacilitiesTXT('facilites_info.txt')
        # facilities, totalFacilityCapacities, openHours = M.createFacilities(
        #     'submodules2.json')


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

        #Updated the formatting of the json file
        response = {'Buildings': [
                    {"BuildingName": str(facilities[id].getFacilityType())+ str(id),
                    "InfectedDaily": infectionInFacilitiesHourly[id],
                    "PeopleDaily": peopleInFacilitiesHourly[id]}
                    for id in range(len(facilities))]
                    } #we should probably have households at least as one large "household"

        #response = {f'({id}, {facilities[id].getFacilityType()})': array
                    #for id, array in infectionInFacilitiesHourly.items()}
        self.jsonResponseToFile(response, "output.txt")

        num = 0
        for each in Pop:
            if len(Pop[each].getInfectionTrack()) > 0:
                num += 1
                #print(Pop[each].getInfectionState(),Pop[each].getinfectionTimer(), Pop[each].getInfectionTrack())

        # f.close()

        if print_infection_breakdown:
            print("Initial infections:", initialInfected)
            print("Total infections in households:", houseinfections)
            print("Total infections in facilities:", facilityinfections)
        print("Total infections:", num)

        self.infecFacilitiesTot= totalInfectedInFacilities
        self.infecHousesTot= infectionInHouseholds
        return

    # Function to run Anytown
    def Anytown(self, print_infection_breakdown, num_days, intervention_list):
        self.loadVisitMatrix('Anytown_Jan06_fullweek_dict.pkl')
        self.WellsRiley(print_infection_breakdown, num_days, intervention_list)

    def implementPhaseDay(self, currDay, phaseNum, phaseDay, phasePlan, population, facilities):
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

    # Test facilities
    def runFacilityTests(self, filename):
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

    # For each POI in the visit matrices, add together all the people in the CBGs
    # Notes: x-axis (cols) is CBGs, y-axis (rows) is POIs
    #        dfVisitMatrix.sum(axis=0) for column-wise sum
    #        dfVisitMatrix.sum(axis=1) for row-wise sum
    def sumVisitMatrices(self):
        totals = []

        # Access each visit matrix for each hour in the week (total of 168 hours)
        for hour in range(168):
            hourVisitMatrix = self.poi_cbg_visit_matrix_history[hour]
            dfVisitMatrix = pd.DataFrame(hourVisitMatrix.todense())
            total_sum = dfVisitMatrix.to_numpy().sum()  # Sum up all the values in the visit matrix
            totals.append(round(total_sum))  # Round the sum and append to the list

        # Uncomment the line below to print out the list of sums
        # print(totals)

if __name__ == '__main__':
    mc = MasterController()  # Instantiate a MasterController

    #mc.runFacilityTests('facilites_info.txt')  # Run facility tests

    # TODO* Graph approach for standard facilities is above in main. We want to tweak this for a household model.
    # TODO School and Work spread need to be implemented as well - either through Wells Riley model or Graph approach.
    # TODO MasterController() should take in json file - load information such as population, interventions, etc
    # TODO Callibration to match realistic/standard data once above is completed.

    mc.loadVisitMatrix('Oklahoma_Jan06_fullweek_dict.pkl')
    #mc.sumVisitMatrices()  # Verify correctness of visit matrices
    interventions = {}
    #interventions = {"maskWearing":100,"stayAtHome":True,"contactTracing":100,"dailyTesting":100,"roomCapacity": 100, "vaccinatedPercent": 50}
    mc.runFacilityTests('facilities_info.txt')
    mc.WellsRiley(True, 61, interventions)  # Run Wells Riley