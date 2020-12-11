#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 14:30:07 2020
"""

from random import random
import numpy as np
import math

facilities = {1: ['retail', 'grocery store', 'DollarGeneral1', 36.567709, -96.166342, [0, 1]], 2: ['retail', 'grocery store', 'DollarGeneral2', 36.567709, -96.166342, [0,1]], 3: ['retail', 'lumberstore', 'BLumber', 36.561313, -96.162036, [0,1]], 3: ['retail', 'store', 'JimsResale', 36.561705, -96.160739, [0,1]], 4: ['retail', 'saddlery', 'JeffWadeSaddlery', 36.561646, -96.165412, [0,1]], 4: ['retail', 'beautysalon', 36.561672, -96.162653, [0,1]], 5: ['retail', 'florist', 'BarnsdallsFlowerShop', 36.559659, -96.162027, [0,1]], 6: ['food services', 'restaurant', 'HatfieldsGrill', 36.557376, -96.160812, [0,1]], 7: ['retail', 'restaurant', 'JKsTakeout', 36.561002, -96.161577, [0,1]], 8: ['retail', 'restaurant', 36.561616, -96.161645, [0,1]], 9: ['retail', 'restaurant', 'UptownPizza', 36.561646, -96.165412, [0,1]], 10: ['public transit station', 'bus station', 'Sinclair Gas station', 36.557620, -96.161300, [0,1]], 11: ['public transit station', 'gas station', 'FASTTRACK', 36.557620, -96.161300, [0,1]], 12: ['outdoors', 'gas station', 'Robinowitz Oil Co', 36.561610, -96.160850, [0,1]], 13: ['long term facilities', 'jails', 'Barnsdall Police Department', 36.561610, -96.161070, [0,1]], 14: ['long term facilities', 'nursing home', 'Barnsdall Nursing Home', 36.662613, -96.200233, [0,1]], 15: ['long term facilities', 'hospital/icu', 'Ascension St. John Jane Phillps', 37.904385, -96.283437, [0,1]]}
population = {0:{'age': 42, 'sex': 1, 'loc': None, 'contacts': {'H': set(), 'S': set(), 'W': {868, 548, 388, 776, 408, 1019, 190, 255}, 'C': set()}, 'hhid': 0, 'scid': -1, 'wpid': 0, 'wpindcode': -1, 'socio-econ': -1, 'house': {'latitude': 36.28, 'longitude': -96.17, 'status': 'A'}, 'status': 'susceptible'},
              1:{'age': 42, 'sex': 1, 'loc': None, 'contacts': {'H': set(), 'S': set(), 'W': {868, 548, 388, 776, 408, 1019, 190, 255}, 'C': set()}, 'hhid': 0, 'scid': -1, 'wpid': 0, 'wpindcode': -1, 'socio-econ': -1, 'house': {'latitude': 36.28, 'longitude': -96.17, 'status': 'A'}, 'status': 'infected'}}

def infectPopulation(facilities, population):
  for facility in facilities:
    valueList = facilities[facility]
    persons = valueList[len(valueList) - 1] # list of people in the facility is the last entry in each value list
    
    transmissions(valueList, persons, population)
    
    
    SEIR = {'susceptible': 0, 'exposed': 0, 'infected': 0, 'recovered': 0}

    #for person in persons:
      # Based on state, increment the appropriate variable
     # state = population[person]['state'] # Assume the state of the person is going to be associated with a 'state' key in the person's dictionary -- assume states are the same as the keys in the SEIR dictionary

      # Increment the appropriate state
      #SEIR[state] += 1

      # Once you've obtained the number of people in each state for this particular facility, using an incubation of 1 hour, obtain the new distribution for SEIR and apply it to the people in the facility --> MAKE SURE TO UPDATE THE SYNTHPOPS DICTIONARY BECAUSE THIS IS WHERE YOU SHOULD ORIGINALLY BE DRAWING STATES FROM 
   
def simulateDay(facilities, population):
  
  # Update the facilities dictionary, no change to the population
  #movePopulation(facilities, population)

  # Update the population dictionary, no change to the facilities 
  infectPopulation(facilities, population)

  # Store some information or visualize something???

def transmissions(facility, persons, population):
    SEIR = {'susceptible': [], 'exposed': [], 'infected': [], 'recovered': []}
    for person in persons:
        state = population[person]['status']
        SEIR[state].append(person)
    s0 = len(SEIR['susceptible'])
    e0 = len(SEIR['exposed'])
    i0 = len(SEIR['infected'])
    r0 = len(SEIR['recovered'])
    total = s0 + e0 + i0 + r0
    incubation = int(random()*11+3)
    alpha = 1/(incubation*24) #average incubation time is 6 days * 24 hours/day
         
    #infection = int(input("Enter average number of days of infection (from 14 - 28): "))
    #while (infection < 14 or infection > 28):
    #    print("Infection out of range, please try again.")
    #    infection = int(input("Enter average number of days of infection (from 14 - 28): "))
     
    #random int from 14 to 28
    infection = int(random()*14 + 14)
    timeInfectious = infection*24 #time infectious is the average time it takes for exposed->infectious (15 days * 24 hours/day)
     
    alpha = 1/(incubation*24)
    area = int(random()*100 + 50)
    densityMult = random()*0.1 + 0.1
    mobilityMult = random()*0.2 + 0.4
    contactMult = random()*0.2 + 0.6
    cleanlinessMult = random()*0.1 + 0.05
    icuDeathRate = random()*0.1 + 0.25
    hospitalDeathRate = random()*0.01 + 0.01
    nursingDeathRate = random()*0.05 + 0.05
    prisonDeathRate = random()*0.15 + 0.05

    mobility = 0
    if (facility[0] == 'long term facilities'):
        mobility = 0
    elif (facility[0] == 'food services' or facility[0] == 'public transportation'):
        mobility = 0.5
    elif (facility[0] == 'outdoors' or facility[0] == 'retail' or facility[0] == 'public transit station'):
        mobility = 1
        
    contact = 0
    if (facility[0] == 'long term facilities' or facility[0] == 'food services' or facility[0] == 'public transportation'):
        contact = 0.2
    elif (facility[0] == 'retail' or facility[0] == 'public transit station'):
        contact = 0.15
    elif (facility[0] == 'outdoors'):
        contact = 0.1
        
    cleanliness = 0
    if (facility[0] == 'outdoors'):
        cleanliness -= 0.05
    elif (facility[0] == 'food services'):
        cleanliness += 0.1
    else:
        cleanliness += 0.075
        
    density = 75 / area
    #beta = .15 * density + .7 * contact + .1 * cleanliness + .5 * mobility
    beta = densityMult * density + contactMult * contact + cleanlinessMult * cleanliness + mobilityMult * mobility
    
    overallContagiousness = 0.0
    averageContagiousLevel = random()*4
    if averageContagiousLevel >= 0 and averageContagiousLevel <= 1:
        overallContagiousness = 0.95
    elif averageContagiousLevel >= 1 and averageContagiousLevel <= 2:
        overallContagiousness = 1.0
    elif (averageContagiousLevel >= 2 and averageContagiousLevel <= 3):
        overallContagiousness = 1.05
    elif (averageContagiousLevel >= 3 and averageContagiousLevel <= 4):
        overallContagiousness = 1.1

    overallSeverity = 0.0
    averageSeverityRisk = random()*4
    if averageSeverityRisk >= 0 and averageSeverityRisk <= 1:
        overallSeverity = 0.95
    elif averageSeverityRisk >= 1 and averageSeverityRisk <= 2:
        overallSeverity = 1.0
    elif (averageSeverityRisk >= 2 and averageSeverityRisk <= 3):
        overallSeverity = 1.05
    elif (averageSeverityRisk >= 3 and averageSeverityRisk <= 4):
        overallSeverity = 1.1
    
    #probability than a susceptible will become exposed, so on so forth for the rest
    prob = {'susceptible': 1*(overallContagiousness * beta * s0 * i0)/(total), 'exposed': alpha*e0, 'infected': i0/(timeInfectious), 'recovered': -1}
    #will have to decide something for infected to recovered or death. later problem though
    newSEIR = {'susceptible': [], 'exposed': [], 'infected': [], 'recovered': []}
    for i in SEIR:
        for agent in SEIR[i]:
            rand = random()
            if rand < (prob[i]/len(SEIR[i])):
                newSEIR[map(map(i) + 1)].append(agent)
                population[agent]['status'] = map(map(i)+1);
            else:
                newSEIR[i].append(agent)
                population[agent]['status'] = i;
    array = [len(newSEIR[map(0)]), len(newSEIR[map(1)]), len(newSEIR[map(2)]), len(newSEIR[map(3)])]
    print(array)
            
def map(var):
    if(var == 0):
        return 'susceptible' 
    elif(var == 1):
        return 'exposed' 
    elif(var == 2):
        return 'infected' 
    elif(var == 3):
        return 'recovered' 
    elif(var == 'susceptible'):
        return 0
    elif(var == 'exposed'):
        return 1 
    elif(var == 'infected'):
        return 2 
    elif(var == 'recovered'):
        return 3 
    
simulateDay(facilities, population)
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       