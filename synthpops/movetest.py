import json 
from math import sin, cos, sqrt, atan2, radians
import copy
import random
from copy import deepcopy
import numpy as np




def initializeFacility(facilities, pop):
  # place everyone in the population at home to start the simulation
  for agent in pop:
    facilties[18][5].append(agent)
  return facilities


def randomFacility():
  # probability distribution of facilities
  return random.randint(1, 17)

def updateLocation(agent, facility, DOW, TOD):

  home = 18
  work = 19
  school = 20
  
  #age: baby (0-4), child(4-18), Adult (18+), Senior?
  #current location: school, work, home, other for facility type (breaks for lunch?)
  #TOD: 9pm-8am, 8am-5pm, 5pm-9pm
  #DOW: Mon-Fri , Sat-Sun
  #example schedules for people
  # baby = [home all day]
  # child = mon - fri[12am-8am 100% @home, 8-3pm 100% @school, 3-8pm every hour 20% chance of being at a facility (function to find which)
       # - other 80@ home, 8-11 5% chance of @ a facility]
       # = sat - sun[12am-8am 100% @home, 8am-7pm: 40% at home, 8-12pm 10% chance @facility]
  # Adult = mon - fri[12am-8am 98% @home, 8-5pm 60% @work/30%home/10%facility*, 5-8pm every hour 20% @facility
  #          - other 80@ home, 8-12 5% chance of @ a facility]
  #       = sat - sun[12am-8am 96% @home, 8am-7pm: 40% at home, 8-12pm 15% chance @facility]
# * for work @8am decide wether they will stay at work for the day, or be in the home/facility group
  if population[agent]['age'] < 4:
    return facility
  elif population[agent]['age'] < 19:
   p = random.randint(1, 100)
   if DOW < 6:   # mon-fri
     if TOD < 8:
       return home
     elif TOD < 15:
       return school
     elif TOD < 20:
       if p < 20:
         return randomFacility()
       else:
         return home
   elif DOW >=6:
      if TOD < 8:
        return home
      elif TOD < 19:
        if p < 40:
          return home
        else:
          return randomFacility()
      else:
        if p < 90:
          return home
        else:
          return randomFacility()
  else:
    p = random.randint(1, 100)
    if DOW < 6: # Weekday
      if TOD < 8:
        if p < 98:
          return home
        else:
          return randomFacility()
      elif TOD < 17:
        if p < 60:
          return work
        elif p < 90:
          return home
        else:
          return randomFacility()
      else:
        if p < 80:
          return home
        else:
          return randomFacility()
    elif DOW >= 6:
      if TOD < 8:
        if p < 96:
          return home
        else:
          return randomFacility()
      elif TOD < 19:
        if p < 40:
          return home
        else:
          return randomFacility()
      else:
        if p < 85:
          return home
        else: 
          return randomFacility()



def movePopulation(population, facilities, DOW, TOD):
  # We're assuming facilities has a list of people in it, at index j
  C_facilities = copy.deepcopy(facilities)
  for facility in facilities:
      facility[5].clear()
  for C_facility, facility in C_facilities, facilities:
    for agent in C_facility[5]:
      newID = updateLocation(agent, facility, DOW, TOD)
      facilities[newID][5].append(agent)



  # copy facility
  # iterate over Cfacilities
    # iterate over each person in the Cfacility
      # update = apply our movement algo on each person (seperate func) : add into facility




def main():           

  with open('sampledict.json') as f:
      population = json.load(f)

  print("\nExample person in population:\n0:" + str(population[0]))

  facilities = {1: ['retail', 'grocery store', 'DollarGeneral1', 36.567709, -96.166342, []], 
  2: ['retail', 'grocery store', 'DollarGeneral2', 36.567709, -96.166342, []], 
  3: ['retail', 'lumberstore', 'BLumber', 36.561313, -96.162036, []], 
  4: ['retail', 'store', 'JimsResale', 36.561705, -96.160739, []], 
  5: ['retail', 'saddlery', 'JeffWadeSaddlery', 36.561646, -96.165412, []], 
  6: ['retail', 'beautysalon', 36.561672, -96.162653, []], 
  7: ['retail', 'florist', 'BarnsdallsFlowerShop', 36.559659, -96.162027],
  8: ['food services', 'restaurant', 'HatfieldsGrill', 36.557376, -96.160812, []], 
  9: ['retail', 'restaurant', 'JKsTakeout', 36.561002, -96.161577, []], 
  10: ['retail', 'restaurant', 36.561616, -96.161645, []], 
  11: ['retail', 'restaurant', 'UptownPizza', 36.561646, -96.165412, []], 
  12: ['public transit station', 'bus station', 'Sinclair Gas station', 36.557620, -96.161300, []], 
  13: ['public transit station', 'gas station', 'FASTTRACK', 36.557620, -96.161300, []], 
  14: ['outdoors', 'gas station', 'Robinowitz Oil Co', 36.561610, -96.160850, []], 
  15: ['long term facilities', 'jails', 'Barnsdall Police Department', 36.561610, -96.161070, []], 
  16: ['long term facilities', 'nursing home', 'Barnsdall Nursing Home', 36.662613, -96.200233, []], 
  17: ['long term facilities', 'hospital/icu', 'Ascension St. John Jane Phillps', 37.904385, -96.283437, []],
  18: ['home', 'home', 'home', 0,0,[]],
  19: ['work', 'work', 'work', 0,0,[]],
  20: ['school', 'school', 'school', 0,0,[]]}

  initializeFacility(facilities, population)

  movePopulation(population, facilities, 1, 0)



  

if __name__== "__main__":
  main()