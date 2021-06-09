class phasePlan():
    def __init__(self, ageMin=[], ageMax=[], maxPhaseNum=0, daysInPhase=[]):
        self.ageMin = ageMin
        self.ageMax = ageMax
        self.maxPhaseNum = maxPhaseNum
        self.daysInPhase = daysInPhase

    def addPhase(self, ageMin, ageMax, days):
        self.ageMin.append(ageMin)
        self.ageMax.append(ageMax)
        self.daysInPhase.append(days)
        self.maxPhaseNum += 1
