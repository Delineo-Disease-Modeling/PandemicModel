import networkx as nx
import random as rnd
import matplotlib.pyplot as plt
import math


# SHOULD visualize/show the number of people infected after SEVERAL WEEKS


class Submodule:

    def __init__(self, id, facilitytype, numGroups=0, Groups=[], People=[], Area=0, Contact=0, Mobility=0, Density=0, Cleanliness=0, Infected=[]):
        # Either initialize parameterized or empty and fill in with methods.
        self.__id = id
        self.__facilitytype = facilitytype
        self.__Area = Area
        self.__Contact = Contact
        self.__Mobility = Mobility
        self.__Density = Density
        self.__Cleanliness = Cleanliness
        self.__numGroups = numGroups
        self.__Groups = Groups
        self.__People = People
        self.__Infected = Infected

    def clearPeople(self):
        self.__People = []
        self.__Infected = []

    def addPerson(self, person):
        self.__People.append(person)
        if person.getInfectionState():
            self.__Infected.append(person)

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

    def calcCleanliness(self):
        cleanliness = 0  # placeholder
        return cleanliness

    def getInfected(self):
        infected = []
        for person in self.__People:
            if person.isInfected():
                infected.append(person)
        return infected

    # This is a potential new function to create the graph, which calcInfection will then traverse
    def createGraph(self):
        sizes = [0] * self.__numGroups
        idList = []
        p = []
        for i in range(self.__numGroups):
            sizes[i] = len(self.__Groups[i])

            for person in self.__Groups[i]:
                idList.append(person.getID())

            tmp_p = [0] * self.__numGroups
            for j in range(self.__numGroups):
                if j == i:
                    tmp_p[
                        j] = 1  # If you're in the same group as an infected person, this is the likelihood you are in contact
                else:
                    tmp_p[
                        j] = .05  # Likelihood of connections between groups, arbitrary formula
            p.append(tmp_p)
        # nx.draw(nx.stochastic_block_model(sizes, p, idList))
        # plt.show()
        # print(idList)
        G = nx.stochastic_block_model(sizes, p, idList)
        infected_ids = [person.getID() for person in self.__Infected]
        options = {"node_size": 400, "alpha": 0.8}
        pos = nx.spring_layout(G)
        nx.generate_edgelist(G)

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
        plt.title("Facility " + str(self.__facilitytype))

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
        return G

    # It seems for simplicity, it would make the most sense to calcInfection here

    def calcInfection(self, stochGraph):
        # OPTIMIZE THIS: WE DO NOT LIKE TRINARY NESTED LOOPS
        for person in self.__Infected:
            for i in list(stochGraph.neighbors(person.getID())):

                # TODO Make this more accurate
                randNum = rnd.randint(1, 101)
                if (randNum < 30):
                    for j in range(len(self.__People)):
                        if self.__People[j].getID() == i:
                            self.__People[j].setInfectionState(True)

    # Wells Riley
    def pulmonaryVentilation(self):
        return 1
        """infected = []
        for person in self.__Infected:
            if (person.infectionState == "critical"):
                infected.append(3.4)
            elif (person.infectionState == "severe"):
                infected.append(1.4)
            elif (person.infectionState == "mild"):
                infected.append(0.55)
            elif (person.infectionState == "asymptomatic"):
                infected.append(0.55)
        return sum(infected)/len(infected)"""

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

    def probability(self):
        p = self.pulmonaryVentilation()
        Q = self.facVentRate(self.__facilitytype)
        q = self.quantaGen(self.__facilitytype)
        I = len(self.getInfected())
        t = 1
        print(type(p), type(q), type(Q), type(I), type(t))

        return 1 - math.exp(-(I*q*p*t)/Q)
