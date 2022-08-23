#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 09:29:33 2020

@author: jamiehuang
"""

from random import random
import numpy as np
import math
import matplotlib.pyplot as plt

#User inputs facility
facility = input("Enter the facility you are entering: ")
        
#Checks if it is a "valid" facility, will add more facilities onto the list
while (facility != 'Train station' and facility != 'Airport' and 
       facility != 'Hospital' and facility != 'ICU' and 
       facility != 'Nursing home' and facility != 'Prison' and
       facility != 'Pharmacy' and facility != 'Bar' and
       facility != 'Restaurant' and facility != 'Gas station' and 
       facility != 'Park' and facility != 'Supermarket' and 
       facility != 'School' and facility !='Train' and
       facility != 'Airplane' and facility != 'Bus' and
       facility != 'Shopping center'):
    print('Invalid facility, please try again')
    facility = input("Enter the facility you are entering: ")

def facilityType():
    if (facility == 'Train station' or facility == 'Airport'):
        return 'Public transit station'
    elif (facility == 'Grocery store' or facility == 'Pharmacy' or facility == 'Shopping center'):
        return 'Retail'
    elif (facility == 'Restaurant' or facility == 'Bar'):
        return 'Food service'
    elif (facility == 'Train' or facility == 'Airplane' or facility == 'Bus'):
        return 'Public transportation'
    elif (facility == 'Park' or facility == 'Gas station'):
        return 'Outdoors'
    else:
        return facility
    
hours = int(input("Enter number of hours: "))

#User # of susceptible/exposed/infected/recovered agents
arr = []
s0 = int(input("Enter number of susceptible individuals: "))
arr.append(s0)
e0 = int(input("Enter number of exposed individuals: "))
arr.append(e0)
i0 = int(input("Enter number of infected individuals: "))
arr.append(i0)
r0 = int(input("Enter number of recovered individuals: "))
arr.append(r0)
arr.append(0) #in the case of deaths
total = s0 + e0 + i0 + r0
print(arr)

incubation = int(input("Enter average number of days of incubation (from 3 - 14): "))
while (incubation < 3 or incubation > 14):
    print("Incubation out of range, please try again.")
    incubation = int(input("Enter average number of days of incubation (from 3 - 14): "))
        
alpha = 1/(incubation*24) #average incubation time is 6 days * 24 hours/day
    
infection = int(input("Enter average number of days of infection (from 14 - 28): "))
while (infection < 14 or infection > 28):
    print("Infection out of range, please try again.")
    infection = int(input("Enter average number of days of infection (from 14 - 28): "))
    
timeInfectious = infection*24 #time infectious is the average time it takes for exposed->infectious (15 days * 24 hours/day)

alpha = 1/(incubation*24)

area = int(input("Enter the area of your facility (from 50 - 150): "))
while (area < 50 or area > 150):
    print("Area out of range, please try again.")
    area = int(input("Enter the area of your facility (from 50 - 150): "))

densityMult = float(input("Enter density multiplier (from 0.1 - 0.2): "))
while (densityMult < 0.1 or densityMult > 0.2):
    print("Density multiplier out of range, please try again.")
    densityMult = float(input("Enter density multiplier (from 0.1 - 0.2): "))

mobilityMult = float(input("Enter mobility multiplier (from 0.4 - 0.6): "))
while (mobilityMult < 0.4 or mobilityMult > 0.6):
    print("Mobility multiplier out of range, please try again.")
    mobilityMult = float(input("Enter mobility multiplier (from 0.4 - 0.6): "))
    
contactMult = float(input("Enter contact multiplier (from 0.6 - 0.8): "))
while (contactMult < 0.6 or contactMult > 0.8):
    print("Contact multiplier out of range, please try again.")
    contactMult = float(input("Enter contact multiplier (from 0.6 - 0.8): "))

cleanlinessMult = float(input("Enter cleanliness multiplier (from 0.05 - 0.15): "))
while (cleanlinessMult < 0.05 or cleanlinessMult > 0.15):
    print("Cleanliness multiplier out of range, please try again.")
    cleanlinessMult = float(input("Enter cleanliness multiplier (from 0.05 - 0.15): "))
    

if (facility == "ICU"):
    icuDeathRate = float(input("Enter ICU death rate (0.25 - 0.35): "))
    while (icuDeathRate < 0.25 or icuDeathRate > 0.35):
        print("ICU death rate out of range, please try again.")
        icuDeathRate = float(input("Enter ICU death rate (0.25 - 0.35): "))

if (facility == "Hospital"):
    hospitalDeathRate = float(input("Enter hospital death rate (0.01 - 0.02): "))
    while (hospitalDeathRate < 0.01 or hospitalDeathRate > 0.02):
        print("Hospital death rate out of range, please try again.")
        hospitalDeathRate = float(input("Enter hospital death rate (from 0.01 - 0.02): "))
        
if (facility == "Nursing home"):
    nursingDeathRate = float(input("Enter nursing home death rate (0.05 - 0.1): "))
    while (nursingDeathRate < 0.05 or nursingDeathRate > 0.1):
        print("Nursing home death rate out of range, please try again.")
        nursingDeathRate = float(input("Enter nursing home death rate (0.05 - 0.1): "))
      
if (facility == "Prison"):
    prisonDeathRate = float(input("Enter prison death rate (0.05 - 0.2): "))
    while (prisonDeathRate < 0.05 or prisonDeathRate > 0.2):
        print("Prison death rate out of range, please try again.")
        prisonDeathRate = float(input("Enter prison death rate (0.05 - 0.2): "))

def main():
    
    print("Average change in susceptible individuals: " + str(hours*changeSusceptible(s0, e0, i0, r0)))
    print("Average change in exposed individuals: " + str(hours*changeExposed(s0, e0, i0, r0)))
    
    if (facility == "ICU" or facility == "Hospital" or facility == "Nursing home" or facility == "Prison"):
       print("Average change in infected individuals: " + str(hours*changeInfected(s0, e0, i0, r0)))
       print("Average change in recovered individuals: " + str(hours*changeRecovered(s0, e0, i0, r0)))
       print("Average change in dead individuals: " + str(hours*changeDead(s0, e0, i0, r0)))
    
    randS = random()
    if (randS < ((hours*changeSusceptible(s0, e0, i0, r0))%1)):
        changeS = math.floor(hours*changeSusceptible(s0, e0, i0, r0)) + 1
    else:
        changeS = math.floor(hours*changeSusceptible(s0, e0, i0, r0))
    
    randE = random()
    if (randE < ((hours*changeExposed(s0, e0, i0, r0))%1)):
        changeE = math.floor(hours*changeExposed(s0, e0, i0, r0)) + 1
    else:
        changeE = math.floor(hours*changeExposed(s0, e0, i0, r0))
    
    randI = random()
    if (randI < ((hours*changeInfected(s0, e0, i0, r0))%1)):
        changeI = math.floor(hours*changeInfected(s0, e0, i0, r0)) + 1
    else:
        changeI = math.floor(hours*changeInfected(s0, e0, i0, r0))
    
    randR = random()
    if (randR < ((hours*changeRecovered(s0, e0, i0, r0))%1)):
        changeR = math.floor(hours*changeRecovered(s0, e0, i0, r0)) + 1
    else:
        changeR = math.floor(hours*changeRecovered(s0, e0, i0, r0))
    
    randD = random()
    if (randD < ((hours*changeDead(s0, e0, i0, r0))%1)):
        changeD = math.floor(hours*changeDead(s0, e0, i0, r0)) + 1
    else:
        changeD = math.floor(hours*changeDead(s0, e0, i0, r0))
        
    print("Change in susceptible individuals: " + str(changeS))
    print("Change in exposed individuals: " + str(changeE))
    
    
    if (facility == "ICU" or facility == "Hospital" or facility == "Nursing home" or facility == "Prison"):
        print("Change in infected individuals: " + str(changeI))
        print("Change in recovered individuals: " + str(changeR))
        print("Change in dead individuals: " + str(changeD))
    print("Transmission Rate: " + str(transmissionRate(s0, e0, i0, r0)))
    
    
    #Shows the bar graph of s, e, i, r, d (orange represents change)
    arr1 = [hours*changeSusceptible(s0, e0, i0, r0), 
            hours*changeExposed(s0, e0, i0, r0),
            hours*changeInfected(s0, e0, i0, r0),
            hours*changeRecovered(s0, e0, i0, r0),
            hours*changeDead(s0, e0, i0, r0)]
    width = 0.35 
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('State of individuals')
    x = np.arange(5)
    plt.xticks(x, ('Susceptible', 'Exposed', 'Infected', 'Recovered', 'Dead'))
    p1 = plt.bar(x, arr, width)
    p2 = plt.bar(x, arr1, width, bottom=arr)
    plt.ylabel('Number of individuals')
    plt.title(facility)
    plt.text(23, 45, r'$\mu=15, b=3$')
    maxfreq = total
    # Set a clean upper y-axis limit.
    plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq)


def areaFactor():
    return area

#Broken up into 3 types of facility
#1. individuals fixed location separated
#2. individuals fixed location, shared room
#3. individuals free to move around, shared room
def mobilityFactor():
    multiplier = 0
    if (facilityType() == 'Hospital' or facilityType() == 'ICU' or facilityType() == 'Prison' or facilityType() == 'Nursing home'):
        multiplier = 0
    elif (facilityType() == 'Food service' or facilityType() == 'Public transportation'):
        multiplier = 0.5
    elif (facilityType() == 'Outdoors' or facilityType() == 'Retail' or facilityType() == 'Public transit station'):
        multiplier = 1
    return multiplier

#Needs work
def contactFactor():
    multiplier = 0
    if (facilityType() == 'Public transportation' or facilityType == 'Food service' or facilityType() == 'ICU' or facilityType() == 'Nursing home' or facilityType() == 'Prison'):
        multiplier = 0.2
    elif (facilityType() == 'Retail'):
        multiplier = 0.15
    elif (facilityType() == 'Outdoors'):
        multiplier = 0.1
    return multiplier

#Facilities that are outdoor
def isOutdoors(facility):
    return (facilityType() == 'Outdoors')

#Facilities that have food
def hasFood(facility):
    return (facilityType == 'Food service')

#Facilities that are outdoors = cleaner, have food = not as clean
def cleanlinessFactor():
    multiplier = 0
    if (isOutdoors(facility)):
        multiplier -= 0.05
    elif (hasFood(facility)):
        multiplier += 0.1
    else:
        multiplier += 0.075
    return multiplier

#Transmission rate equations, combine different factors
def transmissionRate(s0, e0, i0, r0):
    n = s0 + e0 + i0 + r0
    density = n / areaFactor()
    mobility = mobilityFactor()
    contact = contactFactor()
    cleanliness = cleanlinessFactor()
    #beta = .15 * density + .7 * contact + .1 * cleanliness + .5 * mobility
    beta = densityMult * density + contactMult * contact + cleanlinessMult * cleanliness + mobilityMult * mobility
    return beta

#Represents average contagious level among infected agents
def overallContagiousness(): 
    multiplier = 0.0
    averageContagiousLevel = random() * 4
    if averageContagiousLevel >= 0 and averageContagiousLevel <= 1:
        multiplier = 0.95
    elif averageContagiousLevel >= 1 and averageContagiousLevel <= 2:
        multiplier = 1.0
    elif (averageContagiousLevel >= 2 and averageContagiousLevel <= 3):
        multiplier = 1.05
    elif (averageContagiousLevel >= 3 and averageContagiousLevel <= 4):
        multiplier = 1.1
    #print("Overall contagiousness: " + str(averageContagiousLevel))
    return multiplier

#Represents average severity risk among infected agents (how likely they are to die/recover)
def overallSeverityRisk():
    multiplier = 0.0
    averageSeverityRisk = random()*4
    if averageSeverityRisk >= 0 and averageSeverityRisk <= 1:
        multiplier = 0.95
    elif averageSeverityRisk >= 1 and averageSeverityRisk <= 2:
        multiplier = 1.0
    elif (averageSeverityRisk >= 2 and averageSeverityRisk <= 3):
        multiplier = 1.05
    elif (averageSeverityRisk >= 3 and averageSeverityRisk <= 4):
        multiplier = 1.1
    #print("Overall severity risk: " + str(averageSeverityRisk))
    return multiplier
    
#Represents change in susceptible individuals
def changeSusceptible(s0, e0, i0, r0):
    #ds_dt = -1 * transmissionRate(facility, s0, e0, i0, r0) + s0
    ds_dt = -1*(overallContagiousness()*transmissionRate(s0, e0, i0, r0)*s0*i0)/total
    return ds_dt

#Represents change in exposed individuals
def changeExposed(s0, e0, i0, r0):
    #de_dt = transmissionRate(facility, s0, e0, i0, r0) * s0 * i0 - infectedRate * e0
    de_dt = overallContagiousness()*((transmissionRate(s0, e0, i0, r0)*s0*i0)/total) - alpha*e0
    return de_dt
   
#Represents change in infected individuals  
def changeInfected(s0, e0, i0, r0):
    #dr_dt = recoveryRate() * i0
    #dd_dt = deathRate() * i0
    #di_dt = r0 * 0.05 + overallContagiousness()*alpha * e0 - (dr_dt + dd_dt)*e0
    #di_dt = infectedRate*e0 - (recoveryRate() + deathRate())*i0
    di_dt = alpha*e0 - i0/(timeInfectious)
    return di_dt
    
#Represents change in recovered individuals
def changeRecovered(s0, e0, i0, r0):
    #dr_dt = recoveryRate() * i0
    if (facilityType == 'Hospital'):
        dr_dt = i0*(1-overallSeverityRisk()*hospitalDeathRate)/timeInfectious
    elif (facilityType == 'ICU'):
        dr_dt = i0*(1-overallSeverityRisk()*icuDeathRate)/timeInfectious
    elif (facilityType == 'Nursing home'):
        dr_dt = i0*(1-overallSeverityRisk()*nursingDeathRate)/timeInfectious
    elif (facilityType == 'Prison'):
        dr_dt = i0*(1-overallSeverityRisk()*prisonDeathRate)/timeInfectious
    else:
       dr_dt = i0/timeInfectious
    return dr_dt

#Represents change in dead individuals
def changeDead(s0, e0, i0, r0):
    #dd_dt = deathRate() * i0
    if (facilityType == 'Hospital'):
        dd_dt = i0*(overallSeverityRisk()*hospitalDeathRate)/timeInfectious
    elif (facilityType == 'ICU'):
        dd_dt = i0*(overallSeverityRisk()*icuDeathRate)/timeInfectious
    elif (facilityType == 'Nursing home'):
        dd_dt = i0*(overallSeverityRisk()*nursingDeathRate)/timeInfectious
    elif (facilityType == 'Prison'):
        dd_dt = dd_dt = i0*(overallSeverityRisk()*prisonDeathRate)/timeInfectious
    else:
        dd_dt = dd_dt = 0
    return dd_dt

    
if __name__ == "__main__": main()
