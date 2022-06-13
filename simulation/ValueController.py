from phasePlan import PhasePlan


class ValueController:
    def __init__(self, state: str, county: str, population: int, interventions: set, dayOfWeek: int, timeOfDay: int, 
                    phasePlan: PhasePlan, currDay: int, phaseNum: int, phaseDay: int, infecFacilitiesTot: list, infecHousesTot: list,
                    visitMatrices, averageHouseholdInfectionRate: float) -> None:
        """Initializer for ValueController

        Args:
            state (str): state
            county (str): county
            population (int): population size
            interventions (set): set format should be as follows{"MaskWearing": bool,"roomCapacity": int, "StayAtHome": bool}
            dayOfWeek (int): values 1-7 representing Mon-Sun 
            timeOfDay (int): 0-23 representing the hour (rounded down)
            phasePlan (PhasePlan): phase plan of the simulation
            currDay (int): day of the simulation
            phaseNum (int): phase number
            phaseDay (int): phase day
            infecFacilitiesTot (list): 
            infecHousesTot (list): 
            visitMatrices (_type_): 
            averageHouseholdInfectionRate (float): total odds of infecting someone whom they are connected to in a household
        """

        self.__state = state
        self.__county = county
        self.__population = population

        self.__interventions = interventions

        self.__dayOfWeek = dayOfWeek
        self.__timeOfDay = timeOfDay

        self.__phasePlan = phasePlan
        self.__currDay = currDay
        self.__phaseNum = phaseNum
        self.__phaseDay = phaseDay

        self.__infecFacilitiesTot = infecFacilitiesTot
        self.__infecHousesTot = infecHousesTot

        self.__visitMatrices = visitMatrices # Save matrices

        self.__averageHouseholdInfectionRate = averageHouseholdInfectionRate
        return

    def getState(self):
        return self.__state

    def getCounty(self):
        return self.__county

    def getPopulation(self):
        return self.__population

    def getInterventions(self):
        return self.__interventions

    def getDayOfWeek(self):
        return self.__dayOfWeek
    
    def getTimeOfDay(self):
        return self.__timeOfDay

    def getPhasePlan(self):
        return self.__phasePlan

    def getCurrDay(self):
        return self.__currDay

    def getPhaseNum(self):
        return self.__phaseNum

    def getPhaseDay(self):
        return self.__phaseDay

    def getInfecFacilitiesTot(self):
        return self.__infecFacilitiesTot

    def getInfecHousesTot(self):
        return self.__infecHousesTot

    def getVisitMatrices(self):
        return self.__visitMatrices

    def getAverageHouseholdInfectionRate(self):
        return self.__averageHouseholdInfectionRate

