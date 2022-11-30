import os
import sys
from Delineo_Simulation import MasterController

if __name__ == '__main__':
    
    mc = MasterController()  # Instantiate a MasterController

    # mc.sumVisitMatrices()  # Verify correctness of visit matrices
    interventions = {}

    #interventions = {"maskWearing":100,"stayAtHome":True,"contactTracing":100,"dailyTesting":100,"roomCapacity": 100, "vaccinatedPercent": 50}
    # mc.runFacilityTests('facilities_info.txt')

    mc.Anytown(print_infection_breakdown=False, num_days=2,
               intervention_list=interventions)  # Run entire simulation for 61 days

    mc.excelToJson('OKC Data.xls', 'OKC Data.json')