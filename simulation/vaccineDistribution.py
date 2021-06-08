class vaccineDistribution():
    def __init__(self, phaseNum, currPhaseDayNum, ageMin, ageMax, maxPhaseNum):
        self.initializePhaseNum(phaseNum, ageMin, ageMax)
        self.maxPhaseNum = maxPhaseNum  # The number of phases that there will be

    def initializePhaseNum(self, phaseNumNew, ageMin, ageMax):
        self.phaseNum = phaseNumNew  # The number of the phase of the vaccine distribution
        self.currPhaseDayNum = 0     # The number of days spent in the current phase
        self.ageMin = ageMin         # The minimum age of people who are eligible for the vaccine
        self.ageMax = ageMax         # The maximum age of people who are eligible for the vaccine

    def incrementPhaseDayNum(self):
        self.currPhaseDayNum += 1

    def implementPhase(self):
        # maxPhaseNum will depend on how many phases there will be
        while self.phaseNum < self.maxPhaseNum:
            # phaseNumber will depend on the phase that it is in
            while self.currPhaseDayNum < self.phaseNum:
                # vaccinate function constantly while in the phase
                self.incrementPhaseDayNum()

            # ageMin and ageMax will depend on the phase that it is in
            self.initializePhaseNum(self.phaseNum + 1, self.ageMin, self.ageMax)
            self.phaseNum += 1
