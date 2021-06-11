from person import Person
from module import Module
from submodule import Submodule
import random
import json
import pickle
import pandas as pd
import math



class MasterController:
    # MasterController class, this runs the simulation by instantiating module

    state = 'Oklahoma'
    county = 'Barnsdall'
    population = 6000
    # Uncertain exactly what/how many interventions to expect


    interventions = {"MaskWearing": False,"FacilityCap": 1, "StayAtHome": False}  # Default Interventions 1=100% facilitycap
    dayOfWeek = 1  # Takes values 1-7 representing Mon-Sun
    timeOfDay = 0  # Takes values 0-23 representing the hour (rounded down)

    visitMatrices = None # Save matrices 

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

    def displayResult(self):
        print('Nothing to show yet')
        # TODO
    """
    def main(self):

        print("Hello")

        # TODO Integrate Graph approach with current spread model
        M = self.createModule()  # Module instantiated - holds the submodules(facilities), population
        Pop = M.createPopulation()  # Population created and returned as array of People class objects

        # Initialize 5 current infections - This will eventually be customizable. Consider - if we have 20 initial
        # infections how should we spread them through the population?
        for i in range(5):
            ran = random.randint(0, len(Pop) - 1)
            Pop[ran].setInfectionState(True)
        Facilities = M.createSubmodules() # Submodules returned as list of submodule objects.
        interval = 2
        self.runSim(interval, Pop, Facilities, M)
        count = 0
        for each in Pop:
            if Pop[each].getInfectionState():
                count += 1
        print(count)
    """
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
        self.pois_ids_to_name = self.visitMatrices['pois_ids_to_name']


    def calcInfectionsHomes(self, atHomeIDs, Pop, currentInfected):
        numperhour = 0
        newlyinfectedathome = []
        averageinfectiouslength = 24 * 3  # number of days an individual is infectious
        averageinfectionrate = .2  # total odds of infecting someone whom they are connected to in a household with
        # note this math may need to be worked out more, along with correct, scientific numbers
        infectedAndHome = set()
        for each in currentInfected:
            if each.getID() in atHomeIDs and 0 <= each.getInfectionState() <= 3:
                infectedAndHome.add(each)

        while infectedAndHome:
            current = infectedAndHome.pop()
            currentlywith = list(current.getHouseholdMembers()) #id's
            r = random.randint(1,24)
            if r <= 2:
                neighborhouse = list(current.getextendedhousehold())[random.randint(0, len(current.getextendedhousehold())-1)]
                currentlywith.append(neighborhouse)
                for each in Pop[neighborhouse].getHouseholdMembers():
                    currentlywith.append(each)

            for each in currentlywith:
                if len(Pop[each].getInfectionTrack()) > 0:
                    continue

                if (Pop[each].getVaccinatedStatus()):
                    householdRandomVariable = 20 * random.random()
                else:
                    householdRandomVariable = random.random()

                if (householdRandomVariable < (averageinfectionrate / (24 * (len(
                        current.getInfectionTrack()) - current.getIncubation()))) and each in atHomeIDs):  # Probability of infection if in same house at the moment
                    Pop[each].assignTrajectory()
                    newlyinfectedathome.append(Pop[each])
                    numperhour += 1
        return newlyinfectedathome

    # Update everyone's infection status at the beginning of each day
    def update_status(self, interventions, currentInfected, tested):
        toremove = set()
        for each in currentInfected:
            timer = each.incrementInfectionTimer()
            state = each.setInfectionState(each.getInfectionTrack()[timer])
            r = random.random()
            if r <= interventions["dailyTesting"] / 100 * .1 + (interventions["dailyTesting"] / 100) * (
                    interventions["contactTracing"] / 100) * .1:
                tested.add(each)
                rt = random.random()
            if state == 4:
                toremove.add(each)  # if recovered remove from infected list
        for each in toremove:
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
        # list of IDs not yet assigned to a facility
        notAssigned = [*range(len(Pop))]  # about 1200 right now

        # Assign people to facilities based on visit matrices
        hourVisitMatrix = self.poi_cbg_visit_matrix_history[
            h % 168]  # mod resets h to be the hour in current week ie all mondays at midnight will be 0
        dfVisitMatrix = pd.DataFrame(hourVisitMatrix.todense())
        dfVisitMatrix = dfVisitMatrix.sum(axis=1)  # Just sum all cbgs for now

        scale = len(Pop) / 600000.0  # Scale down number of visitors by percentage of OKC population
        for poiID, numPeople in dfVisitMatrix.iteritems():
            facility = openFacilities.get(poiID)
            if not facility:
                break
            if facility.getCapacity() == facility.getVisitors():
                break
            r = 1
            if interventions["stayAtHome"]:
                r = 2  # Reduce number of people at facilities by factor of 2 if stay at home orders.
            traffic = 0
            for i in range(min((math.ceil(numPeople * scale / r)), math.ceil((interventions[
                                                                                  "roomCapacity"] / 100) * facility.getCapacity()))):  # Scale by population of OKC for now
                if not notAssigned:
                    break
                idindextoadd = random.randint(0, len(notAssigned) - 1)
                traffic += 1
                facilities[poiID].addPerson(Pop[notAssigned.pop(idindextoadd)])  # Add random person to POI for now
        return (facilities, notAssigned)

    # Main simulation
    def simulation(self, num_days, currentInfected, interventions, totalInfectedInFacilities,
                    facilities, infectionInFacilitiesDaily, infectionInFacilitiesHourly,
                    peopleInFacilitiesHourly, infectionInHouseholds, facilityinfections,
                    houseinfections, infectionInFacilities, daysDict, openHours, Pop):

        # Main simulation loop
        # Assume movements to facilities in the day only (10:00 - 18:00)
        tested = set()
        for h in range(num_days * 24):
            if h % 24 == 0:
                currentInfected, tested = self.update_status(interventions, currentInfected, tested)
                '''
                toremove = set()
                for each in currentInfected:
                    timer = each.incrementInfectionTimer()
                    state = each.setInfectionState(each.getInfectionTrack()[timer])
                    r = random.random()
                    if r <= interventions["dailyTesting"] / 100 * .1 + (interventions["dailyTesting"] / 100) * (
                            interventions["contactTracing"] / 100) * .1:
                        tested.add(each)
                        rt = random.random()
                    if state == 4: toremove.add(each)  # if recovered remove from infected list
                for each in toremove:
                    currentInfected.remove(each)
                    if each in tested:
                        tested.remove(each)
                '''

            # Initialize current hour's total infections by previous hour
            totalInfectedInFacilities.append(totalInfectedInFacilities[-1])

            # Number of people at facilities

            # numberOut = random.randint(0, min(len(Pop)-1,
            #                       totalFacilityCapacities)) #Not used anymore

            dayOfWeek = (h // 24) % 7
            hourOfDay = h % 24

            # TODO: retention rate within the same facility. currently no one is retained - Retention rate eventually covered by ML team

            for id in facilities:
                facility = facilities[id]
                facility.setVisitors(0)
                facility.clearPeople()

            facilities, notAssigned = self.move_people(facilities, Pop, interventions, daysDict, openHours, dayOfWeek, hourOfDay, h)

            '''
            # Array of facility submodules that are both open and not full

            openFacilities = {id: facility for id, facility in facilities.items()
                              if daysDict[dayOfWeek] in facility.getDays()
                              and facility in openHours[hourOfDay]}
            # list of IDs not yet assigned to a facility
            notAssigned = [*range(len(Pop))]  # about 1200 right now

            # Assign people to facilities based on visit matrices
            hourVisitMatrix = self.poi_cbg_visit_matrix_history[
                h % 168]  # mod resets h to be the hour in current week ie all mondays at midnight will be 0
            dfVisitMatrix = pd.DataFrame(hourVisitMatrix.todense())
            dfVisitMatrix = dfVisitMatrix.sum(axis=1)  # Just sum all cbgs for now


            scale = len(Pop) / 600000.0  # Scale down number of visitors by percentage of OKC population
            for poiID, numPeople in dfVisitMatrix.iteritems():
                facility = openFacilities.get(poiID)
                if not facility:
                    break
                if facility.getCapacity() == facility.getVisitors():
                    break
                r = 1
                if interventions["stayAtHome"]:
                    r = 2  # Reduce number of people at facilities by factor of 2 if stay at home orders.
                traffic = 0
                for i in range(min((math.ceil(numPeople * scale / r)), math.ceil((interventions[
                                                                                      "roomCapacity"] / 100) * facility.getCapacity()))):  # Scale by population of OKC for now
                    if not notAssigned:
                        break
                    idindextoadd = random.randint(0, len(notAssigned) - 1)
                    traffic += 1
                    facilities[poiID].addPerson(Pop[notAssigned.pop(idindextoadd)])  # Add random person to POI for now
            '''

            # Calculate infections for those still not assigned (assume all
            # not in a facility are at home)
            """
            #_____GRAPH VERSION______
            infectedathome = households.calcInfection(G, notAssigned) #TODO return list of persons infected
            """
            # ____SETHOUSEHOLDS_____
            infectedathome = self.calcInfectionsHomes(notAssigned, Pop, currentInfected)
            for each in infectedathome:
                currentInfected.add(each)
            numinfectedathome = len(infectedathome)
            houseinfections += numinfectedathome
            if h == 0:
                infectionInHouseholds.append(numinfectedathome)
            else:
                infectionInHouseholds.append(numinfectedathome + infectionInHouseholds[h - 1])

            for i in range(len(facilities)):
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
        if "vaccinatedPercent" not in interventions:
            interventions["vaccinatedPercent"] = 0
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

        '''
        This function calculates the disease progression by each person in the population
        '''
        '''
        # Module instantiated - holds the submodules(facilities), population
        if interventions is None:
            interventions = {"maskWearing": 0, "dailyTesting": 0, "roomCapacity": 100, "contactTracing": 0,
                             "stayAtHome": False, "vaccinatedPercent": 0}
        if "dailyTesting" not in interventions:
            interventions["dailyTesting"] = 0
        if "maskWearing" not in interventions:
            interventions["maskWearing"] = 0
        if "roomCapacity" not in interventions:
            interventions["roomCapacity"] = 100
        if "contactTracing" not in interventions:
            interventions["contactTracing"] = 0
        if "stayAtHome" not in interventions:
            interventions["stayAtHome"] = False
        if "vaccinatedPercent" not in interventions:
            interventions["vaccinatedPercent"] = 0
        '''
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
        initialInfected = 10  # Should be customizable in  the future
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

        '''
        tested = set()
        # Main simulation loop
        # Assume movements to facilities in the day only (10:00 - 18:00)
        for h in range(num_days * 24):
            if h % 24 == 0:
                toremove = set()
                for each in currentInfected:
                    timer = each.incrementInfectionTimer()
                    state = each.setInfectionState(each.getInfectionTrack()[timer])
                    r = random.random()
                    if r <= interventions["dailyTesting"]/100 * .1 + (interventions["dailyTesting"]/100)*(interventions["contactTracing"]/100) * .1:
                        tested.add(each)
                        rt = random.random()
                    if state == 4: toremove.add(each) #if recovered remove from infected list
                for each in toremove:
                    currentInfected.remove(each)
                    if each in tested:
                        tested.remove(each)

            # Initialize current hour's total infections by previous hour
            totalInfectedInFacilities.append(totalInfectedInFacilities[-1])

            # Number of people at facilities

            #numberOut = random.randint(0, min(len(Pop)-1,
            #                       totalFacilityCapacities)) #Not used anymore

            dayOfWeek = (h // 24) % 7
            hourOfDay = h % 24

            # TODO: retention rate within the same facility. currently no one is retained - Retention rate eventually covered by ML team

            for id in facilities:
                facility = facilities[id]
                facility.setVisitors(0)
                facility.clearPeople()

            # Array of facility submodules that are both open and not full

            openFacilities = {id: facility for id, facility in facilities.items()
                                if daysDict[dayOfWeek] in facility.getDays()
                                and facility in openHours[hourOfDay]}
            # list of IDs not yet assigned to a facility
            notAssigned = [*range(len(Pop))] #about 1200 right now

            # Assign people to facilities based on visit matrices
            hourVisitMatrix = self.poi_cbg_visit_matrix_history[h%168] #mod resets h to be the hour in current week ie all mondays at midnight will be 0
            dfVisitMatrix = pd.DataFrame(hourVisitMatrix.todense())
            dfVisitMatrix = dfVisitMatrix.sum(axis=1) # Just sum all cbgs for now

            scale = len(Pop)/ 600000.0 # Scale down number of visitors by percentage of OKC population
            for poiID, numPeople in dfVisitMatrix.iteritems():
                facility = openFacilities.get(poiID)
                if not facility:
                    break
                if facility.getCapacity() == facility.getVisitors():
                    break
                r = 1
                if interventions["stayAtHome"]:
                    r = 2 # Reduce number of people at facilities by factor of 2 if stay at home orders.
                traffic = 0
                for i in range(min((math.ceil(numPeople * scale / r)),math.ceil((interventions["roomCapacity"]/100)*facility.getCapacity()))): # Scale by population of OKC for now
                    if not notAssigned:
                        break
                    idindextoadd = random.randint(0,len(notAssigned)-1)
                    traffic += 1
                    facilities[poiID].addPerson(Pop[notAssigned.pop(idindextoadd)]) # Add random person to POI for now



            # Calculate infections for those still not assigned (assume all
            # not in a facility are at home)
            """
            #_____GRAPH VERSION______
            infectedathome = households.calcInfection(G, notAssigned) #TODO return list of persons infected
            """
            # ____SETHOUSEHOLDS_____
            infectedathome = self.calcInfectionsHomes(notAssigned, Pop, currentInfected)
            for each in infectedathome:
                currentInfected.add(each)
            numinfectedathome = len(infectedathome)
            houseinfections += numinfectedathome
            if h == 0:
                infectionInHouseholds.append(numinfectedathome)
            else:
                infectionInHouseholds.append(numinfectedathome+infectionInHouseholds[h-1])

            for i in range(len(facilities)):
                if daysDict[dayOfWeek] not in facilities[i].getDays():
                    infectionInFacilities[i].append('Not open')
                    continue
                if facilities[i] not in openHours[hourOfDay]:
                    infectionInFacilities[i].append('Not open')
                    continue
                initialInfectionNumber = len(facilities[i].getInfected())
                finalInfectionNumber = initialInfectionNumber

                #Probability of infection in facility i

                prob = facilities[i].probability(interventions) # Wells-Riley here
                
                #get number of people in facilities
                peopleInFacilitiesHourly[i][h] = len(facilities[i].getPeople())
                for person in facilities[i].getPeople():
                    # Don't re-infect
                    if len(person.getInfectionTrack()) > 0: # continue if already infected
                        continue
                        
                    temp = random.uniform(0, 1)

                    if person.getVaccinatedStatus():
                        # effect of vaccination is 20-fold decrease in chance of infection. (95% decrease)
                        # NOTE: Multiplying by 20 is the same as dividing prob by 20, we're not increasing the
                        # chance of infection we're just getting temp into the same scale as prob
                        temp = 20 * temp 

                    if temp < prob: # Infect

                        person.assignTrajectory()
                        currentInfected.add(person)

                        # Update statistics
                        finalInfectionNumber += 1
                        facilityinfections +=1
                        totalInfectedInFacilities[-1] += 1
                        infectionInFacilitiesDaily[i][h//24] += 1
                        infectionInFacilitiesHourly[i][h] += 1

                infectionInFacilities[i].append(
                    [initialInfectionNumber, finalInfectionNumber])
        '''


        print(
            f'Results for {self.county}, {self.state} over {num_days} days')  # , file=f)

        '''
        for id in infectionInFacilities:
            facility = facilities[id]
            print(facility.getID(), facility.getFacilityType(),
                  infectionInFacilities[id])  # , file=f)
        print()
        print('Infection In Facilities Daily: ', infectionInFacilitiesDaily)
        print('Infection In Facilities Hourly: ', infectionInFacilitiesHourly)
        print('Total number infected in facilities hourly is ',
                totalInfectedInFacilities)
            facility = facilities[id] '''
            # print(facility.getID(), facility.getFacilityType(),   # not useful
            #         infectionInFacilities[id])  # , file=f)


        #print('Total Infected In Households Hourly: ', infectionInHouseholds)

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

        #print("total:",num,"house:", houseinfections, "facilities:", facilityinfections)

        # print("total:",num,"house:", houseinfections, "facilities:", facilityinfections)


        # f.close()
        '''
        totalinf = 0
        for id in range(len(infectionInFacilitiesHourly)):
            individual = 0
            people = 0
            for i in range(len(infectionInFacilitiesHourly[id])):
                #print("num here", peopleInFacilitiesHourly[id][i],"infected here", infectionInFacilitiesHourly[id][i])
                totalinf += infectionInFacilitiesHourly[id][i]
                individual += infectionInFacilitiesHourly[id][i]
                people += peopleInFacilitiesHourly[id][i]

            print(id, individual, people)
        print(totalinf)

            # print(id, individual, people)    # not useful
        '''

        if print_infection_breakdown:
            print("Initial infections:", initialInfected)
            print("Total infections in households:", houseinfections)
            print("Total infections in facilities:", facilityinfections)
        print("Total infections:", num)

    # Function to run Anytown
    def Anytown(self, print_infection_breakdown, num_days, intervention_list):
        self.loadVisitMatrix('Anytown_Jan06_fullweek_dict.pkl')
        self.WellsRiley(print_infection_breakdown, num_days, intervention_list)



if __name__ == '__main__':

    mc = MasterController()  # Instantiate a MasterController
    # TODO* Graph approach for standard facilities is above in main. We want to tweak this for a household model.
    # TODO School and Work spread need to be implemented as well - either through Wells Reilly model or Graph approach.
    # TODO MasterController() should take in json file - load information such as population, interventions, etc
    # TODO Callibration to match realistic/standard data once above is completed.

    mc.loadVisitMatrix('Anytown_Jan06_fullweek_dict.pkl')
    interventions = {"vaccinatedPercent": 50}
    #interventions = {"maskWearing":100,"stayAtHome":True,"contactTracing":100,"dailyTesting":100,"roomCapacity": 100}
    mc.WellsRiley(True, 61, interventions)  # Run Wells Riley

