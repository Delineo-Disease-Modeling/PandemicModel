import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.simulation.master import MasterController as sim

if __name__ == '__main__':

    mc = sim()  # Instantiate a MasterController

    # mc.sumVisitMatrices()  # Verify correctness of visit matrices
    interventions = {}

    #interventions = {"maskWearing":100,"stayAtHome":True,"contactTracing":100,"dailyTesting":100,"roomCapacity": 100, "vaccinatedPercent": 50}
    mc.runFacilityTests(r'simulation\data\facilites_info.txt')

    mc.Anytown(print_infection_breakdown=False, num_days=2,
              intervention_list=interventions)  # Run entire simulation for 61 days

    mc.excelToJson('simulation\data\OKC Data.xls', 'simulation\data\OKC Data.json')
