class vaccineDistribution():
    def __init__(self, phaseNum, currPhaseDayNum, ageMin, ageMax):
        self.initializePhaseNum(phaseNum, ageMin, ageMax)

    def initializePhaseNum (self, phaseNumNew, minAge, maxAge):
        self.phaseNum = phaseNumNew
        self.ageMin = minAge
        self.ageMax = maxAge
        self.currPhaseDayNum = 0

    def incrementPhaseDayNum(self):
        self.currPhaseDayNum += 1

    def implementPhase(self):
        # # maxPhaseNum will depend on how many phases there will be
        # while (phaseNum < maxPhaseNum):
        #     # phaseNumber will depend on the phase that it is in
        #     while (currPhaseDayNum < phaseNumber):
        #         # vaccinate function constantly while in the phase
        #         currPhaseDayNum += 1
        #     minAge and maxAge will depend on the phase that it is in
        #     initializePhaseNum(phaseNum++, minAge, maxAge)
