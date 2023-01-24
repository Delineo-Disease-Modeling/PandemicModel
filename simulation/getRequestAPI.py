import requests
import pandas as pd

import json
from ValueController import ValueController
from phasePlan import PhasePlan
# response = requests.get("http:") #change


data = json.load(open('testAPI.json'))  # change to response
phase_plan = PhasePlan()  # TODO: initialize phaseplan!!

# call ValueController
valController = ValueController(data['state'], data['country'], data['population'],
                                data['interventions'], data['dayOfWeek'], data['timeOfDay'],
                                phase_plan, data['currDay'], data['phaseNum'], data['phaseDay'],
                                data['infecFacilitiesTot'], data['infecHousesTot'],
                                data['visitMatricies'], data['averageHouseholdInfectionRate'])
