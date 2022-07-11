from module import Module
from person import Person
from population import Population
from master import MasterController

class SeverityRisk:
    '''
    This class represents the addition of the infection to a population in which persons have comorbidities, which impact severity. 
    It creates a population object with comorbidities in a module and adds infection to persons in the population.
    '''
    def main(self):
        mc = MasterController()
        M = mc.createModule()
        Pop = M.createPopulationObj()
        peopleArray = Pop.get_dict()
        Pop.addDisease()
        for person in peopleArray.values():
            person.setInfectionState(True)

