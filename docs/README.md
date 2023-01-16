# Overview
The Delineo Simulator attempts to realistically capture the mechanisms of disease spread within a diverse range of geographies, ranging from small rural communities to large cities. The simulator works in two parts. Fundamentally, the question of disease movement is a question of population movement. Using geolocation mobility data from SafeGraph, realistic population movement dynamics are created. Then, a statistical disease driver uses the population movement information to predict disease spread. 

# Methods
run_test(): Uses default settings to quickly run the simulation. Requires no data.

run_simulation(): Uses generic settings, location, numDays, interventions. 
Information in Input. 

run_simulation_full(): TODO, Uses Input Format

# Input

Format for Input.
 {
    "state": "Oklahoma",
    "county": "Barnsdall",
    "population": 650000,
    "interventions": {"MaskWearing": false,"roomCapacity": 100, "StayAtHome": false},
    "dayOfWeek": 1,
    "timeOfDay": 0,
    "phasePlan": "PhasePlan(3, [60, 40, 16], [99, 99, 99], [60, 45, 60])",
    "currDay": 0,
    "phaseNum": 0,
    "phaseDay": 0,
    "infecFacilitiesTot":[],
    "infecHousesTot": [],
    "visitMatricies": "None",
    "averageHouseholdInfectionRate": 0.2 
  }

state - State where the location data will be pulled.
county - County of State.
population - Sample population.
interventions - Interventions applied to that population. {MaskWearing: bool, roomCapacity: int, StayAtHome: bool}
dayOfWeek - First day to test on (1 = Sunday, 7 = Monday)
timeOfDay - First hour to run on (0 - 12 AM, 1 - 1 AM)
phasePlan: - TO BE UPDATED
currDay: - TODO

# OUTPUT

TOOO