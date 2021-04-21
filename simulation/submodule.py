import networkx as nx
import random as rnd
import matplotlib.pyplot as plt
import math


# SHOULD visualize/show the number of people infected after SEVERAL WEEKS


class Submodule:

    def __init__(self, id, facilitytype, capacity=None, hours=[], days=[], numGroups=0, Groups=[], People=[], Area=0, Contact=0, Mobility=0, Density=0, Cleanliness=0, Infected=[]):
        # Either initialize parameterized or empty and fill in with methods.
        self.__id = id
        self.__Facilitytype = facilitytype
        capacities = {                          # TODO: add to the default/medium number of capacity
            'Supermarket': 100,
            'Restaurant': 20,
        }
        self.__Capacity = capacities[facilitytype] if facilitytype in capacities else 20
        self.__Visitors = 0  # the current number of customers in the facility
        self.__Hours = hours
        self.__Days = days
        self.__Area = Area
        self.__Contact = Contact
        self.__Mobility = Mobility
        self.__Density = Density
        self.__Cleanliness = Cleanliness
        self.__numGroups = numGroups
        self.__Groups = Groups
        self.__People = People
        self.__Infected = Infected
        self.__MedianRetentionHour = 1  # TODO: research and add

    def getID(self):
        return self.__id

    def getFacilityType(self):
        return self.__Facilitytype

    def getCapacity(self):
        return self.__Capacity

    def getDays(self):
        return set(self.__Days)

    def getVisitors(self):
        return self.__Visitors

    def setVisitors(self, num):
        self.__Visitors = num

    def getPeople(self):
        return self.__People

    def addPerson(self, person):
        self.__People.append(person)

    def addInfected(self, person):
        self.__Infected.append(person)

    def clearPeople(self):
        self.__People = []
        self.__Infected = []

    def calcContact(self):
        contact = 0  # placeholder
        return contact

    def calcMobility(self):
        mobility = 0  # placeholder
        return mobility

    def calcDensity(self):
        density = 0  # placeholder
        return density

    def calcNumGroups(self):
        numGroups = 0  # placeholder
        return numGroups


    #TODO This code will be adapted to fit household model - Likely want to instantiate houses as groups

    def createGroups(self):
        count = 0
        groups = []
        while count < len(self.__People):
            ran = min(rnd.randint(4, 5), len(self.__People) - count)
            group = []
            for i in range(ran):
                group.append(self.__People[count])
                count += 1
            groups.append(group)
        """
        groups = []
        group = []
        for each in self.__People:
            group.append(each)
        groups.append(group)
        """
        self.__numGroups = len(groups)
        self.__Groups = groups

        
    #create groups based on household network
    def createGroupsHH(self):
        groupsDict = {} # If we know total number households here, we can just use a list
        for person in self.__People:
            # Create new group if household not yet instantiated
            # Else, add to existing household group
            if not groupsDict.get(person.hhid):
                groupsDict[person.hhid] = [person]
            else:
                groupsDict[person.hhid].append(person)
        # Map dictionary to an array
        groups = [group for group in groupsDict.values()]
        self.__numGroups = len(groups)
        self.__Groups = groups

    def calcCleanliness(self):
        cleanliness = 0  # placeholder
        return cleanliness

    def getInfected(self):
        # infected TODO in the future incorporate recovered state
        # return self.__Infected
        return [person for person in self.__People if
                0 <= person.getInfectionState() <= 3]

    # This is a potential new function to create the graph, which calcInfection will then traverse
    def createGraph(self):
        sizes = [0] * self.__numGroups
        print("Number of groups: ",self.__numGroups)
        idList = []
        p = []
        for i in range(self.__numGroups):
            sizes[i] = len(self.__Groups[i])

            for person in self.__Groups[i]:
                idList.append(person.getID())

            tmp_p = [0] * self.__numGroups
            for j in range(self.__numGroups):
                if j == i:
                    tmp_p[j] = .8  # If you're in the same group as an infected person, this is the likelihood you are in contact
                else:
                    tmp_p[
                        j] = .001  # Likelihood of connections between groups, arbitrary formula - #TODO change to based on number of households

            p.append(tmp_p)
        # nx.draw(nx.stochastic_block_model(sizes, p, idList))
        # plt.show()
        # print(idList)
        G = nx.stochastic_block_model(sizes, p, idList, sparse=True)  # Creates graph based on sizes of groups, prob of edges, list of people
        infected_ids = [person.getID() for person in self.getInfected()]
        options = {'node_size': 400, 'alpha': 0.8}
        pos = nx.spring_layout(G)
        nx.generate_edgelist(G) #Generates edges

        """
        # hide visualization for now
        #visualize graph

        labels = {}
        for i in range(len(self.__People)):
            labels[self.__People[i].getID()] = r"$" + \
                str(self.__People[i].getID()) + "$"
        nx.draw_networkx_labels(G, pos, labels, font_size=8)
        nx.draw_networkx_nodes(G, pos, nodelist=idList,
                               node_color="g", label=labels, **options)
        nx.draw_networkx_nodes(G, pos, nodelist=infected_ids,
                               node_color="r", label=labels, **options)
        nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
        plt.title("Facility " + str(self.__Facilitytype))

        neighbours_ids = []

        # OPTIMIZE THIS: WE DO NOT LIKE TRINARY NESTED LOOPS
        for person in infected_ids:
            for i in list(G.neighbors(person)):
                for j in range(len(self.__People)):
                    if self.__People[j].getID() == i:
                        neighbours_ids.append(self.__People[j].getID())
        print(neighbours_ids)
        # Colouring edges vs. exposed nodes???
        nx.draw_networkx_nodes(
            G, pos, nodelist=neighbours_ids, node_color="blue", label=labels, **options)

        plt.show()
        """

        return G

    # It seems for simplicity, it would make the most sense to calcInfection here

    def calcInfection(self, stochGraph, atHomeIDs):
        numperhour = 0
        newlyinfectedathome = []
        averageinfectiouslength = 24 * 3 # number of days an individual is infectious
        averageinfectionrate = .2 # total odds of infecting someone whom they are connected to in a household with
        # note this math may need to be worked out more, along with correct, scientific numbers
        peopleDict = {person.getID(): person for person in self.__People}
        infectedAndHome = [person for person in self.__People if
                           0 <= person.getInfectionState() <= 3 and person.getID() in atHomeIDs]
        for person in infectedAndHome:
            neighborIDs = list(stochGraph.neighbors(person.getID()))
            for neighborID in neighborIDs:
                neighbor = peopleDict[neighborID]
                if len(neighbor.getInfectionTrack()) > 0:
                    continue
                if (rnd.random() < (averageinfectionrate/(24*(len(person.getInfectionTrack())-person.getIncubation())))): # Probability of infection if edge exists
                    neighbor.assignTrajectory()
                    newlyinfectedathome.append(neighbor)
                    numperhour += 1
        return newlyinfectedathome


    # Wells Riley
    def pulmonaryVentilation(self):
        d = {'susceptible' : -1,
            'asymptomatic': 0,
            'mild':        1,
            'severe':      2,
            'critical':    3,
            'recovered':   4}
        infected = []
        peopleInfected = self.getInfected()
        for person in peopleInfected:
            if (person.infectionState == d['critical']): #critical
                infected.append(3.4)
            elif (person.infectionState == d['severe']):#severe
                infected.append(1.4)
            elif (person.infectionState == d['mild']):#mild
                infected.append(0.55)
            elif (person.infectionState == d['asymptomatic']): #asymptomatic
                infected.append(0.55)
        return sum(infected)/len(infected) if infected else 0

    def facVentRate(self, facility):
        facilities = [set(['Church', 'Prison']),
                      set(['Airplane']),
                      set(['Casino', 'Airport', 'Supermarket',
                           'Restaurant', 'Retail', 'School']),
                      set(['Movie theater']),
                      set(['Community center', 'Gym', 'Spa']),
                      set(['Nursing home', 'Hospital']),
                      set(['Gas station', 'Park', 'Zoo'])]
        # 50 is placeholder for outdoor facilities. todo: find actual air flow rate
        ventRate = [2.5, 3.5, 3.8, 5, 10, 13, 50]
        # todo add more types of facilities
        for i in range(len(facilities)):
            if facility in facilities[i]:
                return ventRate[i]

    def quantaGen(self, facility):
        # 14 - 48
        if (facility == 'Gas station' or 'Park' or 'Zoo'):
            return 14
        if (facility == 'Casino' or 'Movie theater'):
            return 20
        if (facility == 'Gym' or 'Community center' or 'Church'):
            return 48


    def probability(self, interventions):  # Code for the Wells Reilly Model
        maskwear = interventions["maskWearing"] / 100
        r = 1 + maskwear # maskwearing can reduce pulmonary ventilation by up to a factor of 2

        p = self.pulmonaryVentilation() / r # Reduce pulmonary ventilation by factor r
        Q = self.facVentRate(self.__Facilitytype)
        q = self.quantaGen(self.__Facilitytype)
        I = len(self.getInfected())
        t = 1
        #print("p:",p,"Q:",Q,"q:",q,"I:",I,"prob", 1 - math.exp(-(I*q*p*t)/(Q*100)) )
        temporarytuningfactor = 105
        return 1 - math.exp(-(I*q*p*t)/(Q*temporarytuningfactor)) # This needs to be fixed so wells reilly is actually implemented with better numbers!
        #return 1 - math.exp(-(I * q * p * t) / (Q) # Q has been edited such that it is multiplied by a factor for rough parameter tuning, more wells reilly research required!
