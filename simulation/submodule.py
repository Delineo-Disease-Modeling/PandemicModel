import networkx as nx
import random as rnd

class Submodule:

    def __init__(self, Area, Contact, Mobility, Density, Cleanliness, numGroups, Groups, People):
        # Either initialize parameterized or empty and fill in with methods.
        self.__Area = Area
        self.__Contact = Contact
        self.__Mobility = Mobility
        self.__Density = Density
        self.__Cleanliness = Cleanliness
        self.__numGroups = numGroups
        self.__Groups = Groups
        self.__People = People

    def calcContact(self):
        contact = 0 #placeholder
        return contact

    def calcMobility(self):
        mobility = 0 #placeholder
        return mobility

    def calcDensity(self):
        density = 0 #placeholder
        return density
    def calcNumGroups(self):
        numGroups = 0 #placeholder
        return numGroups

    def createGroups(self):
        groups = {} #placeholder
        return groups

    def calcCleanliness(self):
        cleanliness = 0 #placeholder
        return cleanliness

    def getInfected(self):
        infected = []
        for person in self.__People
            if person.isInfected()
                infected.append(person)
        return infected


    # This is a potential new function to create the graph, which calcInfection will then traverse
    def createGraph(self):
        sizes = [0] * self.__numGroups
        idList = []
        p = []
        for i in self.__numGroups:
            sizes[i] = len(self.__Groups[i])

            for person in self.__Groups[i]:
                idList.append(person.getID())

            tmp_p = [0] * self.__numGroups
            for j in self.__numGroups:
                if j == i:
                    tmp_p[j] = 1 #If you're in the same group as an infected person, this is the likelihood you are in contact
                else:
                    tmp_p[j] = self.__Mobility * self.__Density # Likelihood of connections between groups, arbitrary formula
            p.append(tmp_p)
        return nx.stochastic_block_model(sizes, p, idList)

    # It seems for simplicity, it would make the most sense to calcInfection here
    def calcInfection(self, stochGraph):
        infected = getInfected()
        for person in infected:
            for i in nx.list(stochGraph.adj[person.getID()]):
                #TODO Make this more accurate
                randNum = rnd.randint(1, 101)
                if (randNum < 30):
                    Population.find(i).setInfected(True) # Set's person to be infected
        
        