from module import Module
from person import Person
from population import Population
from master import MasterController

class SeverityRisk:
    def main(self):
        mc = MasterController()
        M = mc.createModule()
        Pop = M.createPopulationObj()
        peopleArray = Pop.get_dict()
        Pop.addDisease()
        for person in peopleArray.values():
            person.setInfectionState(True)

