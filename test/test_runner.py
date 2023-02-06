import simulation.master

if __name__ == '__main__':

    # mc.sumVisitMatrices()  # Verify correctness of visit matrices
    interventions = {}

    # interventions = {"maskWearing":100,"stayAtHome":True,"contactTracing":100,"dailyTesting":100,"roomCapacity": 100, "vaccinatedPercent": 50}
    mc.runFacilityTests(r'sim\src\simulation\data\facilites_info.txt')

    mc.runTest(2)  # Run entire simulation for 61 days

    mc.excelToJson(r'sim\src\simulation\data\OKC_Data.xls',
                   r'sim\src\simulation\data\OKC_Data.json')