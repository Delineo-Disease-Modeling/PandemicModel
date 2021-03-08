from module import Module
from person import Person
from population import Population
from master import MasterController

class SeverityRisk:
    def main(self):
        mc = MasterController()
        M = mc.createModule()
        Pop = M.createPopulationObj()
        Pop.get_dict()
        Pop.addDisease()
