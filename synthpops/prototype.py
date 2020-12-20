import json 
from math import sin, cos, sqrt, atan2, radians
import copy
import random
from copy import deepcopy
import numpy as np
import matplotlib as pltb
import synthpops as sp

def dist(loc1, loc2):
  """
  Computes the distance betweens two locations.
  Locations are in latitude and longitude.

  Args: loc1 (tuple): first location, loc2 (tuple): second location

  Return: The distance between loc1 and loc2, in km.
  """
  # approximate radius of earth in km
  rad = 6373.0

  lat1 = radians(loc1[0])
  lon1 = radians(loc1[1])
  lat2 = radians(loc2[0])
  lon2 = radians(loc2[1])

  dlon = lon2 - lon1
  dlat = lat2 - lat1

  a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  c = 2 * atan2(sqrt(a), sqrt(1 - a))

  return rad * c



def find_next_closest_house(neighbour, houses, population):
  far_loc = [1000, -1000]

  reference_house = [population[neighbour]['house']["latitude"], population[neighbour]['house']["longitude"]]
  min_dist = dist(reference_house, far_loc)
  closest_house = 0
  count = 0

  # For each house dictionary in the houses list
  for i in range(len(houses)):
    # If the house is unassigned
    if houses[i]["status"] == "U":

      house_dict = houses[i]
      # Calculate the distance between the neighbour house and the current house
      reference_house = [population[neighbour]['house']["latitude"], population[neighbour]['house']["longitude"]]

      distance = dist(reference_house, [house_dict["latitude"], house_dict["longitude"]])

      # If a smaller distance is found 
      if min_dist > distance:
        # Update the minimum distance variable
        min_dist = distance

        #Update the location of the closest house
        closest_house = count
    count += 1

  return closest_house

def find_next_available_house(houses):
  count = 0
  for house_dict in houses:
    # If the house is unassigned
    if house_dict["status"] == "U":
      return count
    count += 1
  return -1

def distribute_house(population, housedata, num_assigned):

  npop = len(population.keys())

  if num_assigned >= npop:
    return

  for person in population:
    house_dict = population[person]['house']

    # If the person in the population has NOT been assigned a house
    # if house_dict["latitude"] == 0 and house_dict["longitude"] == 0:

    if population[person]['status'] == "U":

      house_location = find_next_available_house(housedata)

      if house_location == -1:
        return

      house = housedata[house_location]

      housedata[house_location]["status"] = "A"

      population[person]['house'] = house
      population[person]['status'] = "A"

      assign_household(person, population, house)
      assign_school_contacts(person, population, housedata)
      assign_workplace_contacts(person, population, housedata)

      household = population[person]["contacts"]["H"]

      for member in household:
        assign_school_contacts(member, population, housedata)
        assign_workplace_contacts(member, population, housedata)

    num_assigned += 1
  distribute_house(population, housedata, num_assigned)



def assign_household(person, population, house):
  #print(population[person]['H'])
  for household_member in population[person]["contacts"]["H"]:
    #print(population[household_member])
    house_dict = population[household_member]['house']
    #print(house_dict)
    if population[household_member]['status'] == "U":
      population[household_member]["house"] = house
      population[household_member]["status"] = "A"

  #return population

def assign_workplace_contacts(person, population, housedata):

  for coworker in population[person]["contacts"]["W"]:
    house_dict = population[coworker]['house']
    if population[coworker]['status'] == "U":
      closest_house = find_next_closest_house(person,housedata, population)
      house = housedata[closest_house]
      housedata[closest_house]["status"] = "A"

      population[coworker]["house"] = house
      population[coworker]["status"] = "A"
      assign_household(coworker, population, house)


def assign_school_contacts(person, population, housedata):
  for classmate in population[person]["contacts"]["S"]:
    house_dict = population[classmate]['house']
    if population[classmate]['status'] == "U":
      closest_house = find_next_closest_house(person,housedata, population)
      house = housedata[closest_house]
      housedata[closest_house]["status"] = "A"

      population[classmate]["house"] = house
      population[classmate]["status"] = "A"
      assign_household(classmate, population, house)


def initializeFacility(facilities, pop):
    for agent in pop:
      facilities[18][5].append(agent)
    return facilities

def randomFacility():
  # probability distribution of facilities
  return random.randint(1, 17)

def updateLocation(agent, facility, DOW, TOD, population):

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

#move the population
def movePopulation(population, facilities, DOW, TOD):
  # We're assuming facilities has a list of people in it, at index j
  C_facilities = copy.deepcopy(facilities)
  for facility in facilities:
      facilities[facility][5].clear()

  #update locations and add agents to facility lists
  for C_facility in C_facilities:
    for agent in C_facilities[C_facility][5]:
      newID = updateLocation(agent, C_facility, DOW, TOD, population)
      facilities[newID][5].append(agent)

def main():

  # Necessary for synthpops
  sp.validate()

  datadir = sp.datadir # this should be where your demographics data folder resides

  # We are currently using distributions from the seattle dataset, since we don't have data for Barnsdall.
  location = 'seattle_metro'
  state_location = 'Washington'
  country_location = 'usa'
  sheet_name = 'United States of America'
  level = 'county'

  # Reflective of Barnsdall census data
  num_households = 459
  npop = 1132
  num_workplaces = 200

  # Create synthetic population
  pop, homes_dic = sp.generate_synthetic_population(npop,datadir, num_households, num_workplaces, location=location, state_location=state_location,country_location=country_location,
  sheet_name=sheet_name, return_popdict=True)

  num_households = 0
  num_pop = 0

  # Print number of houses and people created (testing purposes)
  for i in range(1,len(homes_dic) + 1):
    num_households = num_households + len(homes_dic[i])
    num_pop = num_pop + len(homes_dic[i]) * i
  print("Population Created, total " + str(num_pop) + " people, " + str(num_households) + " households")

  population = pop

  # add house and status parameters to population
  for person in population:
    population[person]['house'] = {"latitude": 0, "longitude": 0}
    population[person]['status'] = "U"

  #open houses.json, which has latitude and longitude locations for each house
  #TODO: replace with actual housing data
  with open("houses.json") as housejsonfile:
    housejsondata = json.load(housejsonfile)

  # Mark each house as initially unassigned
  for i in range(len(housejsondata)):
    housejsondata[i]["status"] = "U"

  #assign each person a house
  distribute_house(population, housejsondata, 0)

  print("\nExample person in population:\n0:" + str(population[0]))


  facilities = {1: ['retail', 'grocery store', 'DollarGeneral1', 36.567709, -96.166342, []], 2: ['retail', 'grocery store', 'DollarGeneral2', 36.567709, -96.166342, []],  3: ['retail', 'lumberstore', 'BLumber', 36.561313, -96.162036, []], 4: ['retail', 'store', 'JimsResale', 36.561705, -96.160739, []], 5: ['retail', 'saddlery', 'JeffWadeSaddlery', 36.561646, -96.165412, []],6: ['retail', 'beautysalon', 'BSquareHair', 36.561672, -96.162653, []], 7: ['retail', 'florist', 'BarnsdallsFlowerShop', 36.559659, -96.162027, []], 8: ['food services', 'restaurant', 'HatfieldsGrill', 36.557376, -96.160812, []], 9: ['retail', 'restaurant', 'JKsTakeout', 36.561002, -96.161577, []], 10: ['retail', 'restaurant', 'unnamed_food', 36.561616, -96.161645, []], 11: ['retail', 'restaurant', 'UptownPizza', 36.561646, -96.165412, []], 12: ['public transit station', 'bus station', 'Sinclair Gas station', 36.557620, -96.161300, []], 13: ['public transit station', 'gas station', 'FASTTRACK', 36.557620, -96.161300, []], 14: ['outdoors', 'gas station', 'Robinowitz Oil Co', 36.561610, -96.160850, []], 15: ['long term facilities', 'jails', 'Barnsdall Police Department', 36.561610, -96.161070, []], 16: ['long term facilities', 'nursing home', 'Barnsdall Nursing Home', 36.662613, -96.200233, []], 17: ['long term facilities', 'hospital/icu', 'Ascension St. John Jane Phillps', 37.904385, -96.283437, []],18: ['home', 'home', 'home', 0,0,[]], 19: ['work', 'work', 'work', 0,0,[]],20: ['school', 'school', 'school', 0,0,[]]}

  facility_Monday = {}
  facility_Tuesday = {}
  facility_Wednesday = {}
  facility_Thursday = {}
  facility_Friday = {}
  facility_Saturday = {}
  facility_Sunday = {}

  initializeFacility(facilities, population)
  #preview facility
  print(facilities[1])

  #facility map keys to facility type
  facilityTypeMap = {1:"retail", 2:'food services', 3:'public transit station', 4:'outdoors', 5:'long term facilities', 6:'home', 7:'work', 8:'school'}
  #keys are facility type, values are facilities belonging to that type
  facilityMap = {1:[1,2,3,4,5,6,7,9,10,11], 2:[8], 3:[12,13],4:[14], 5:[15,16,17], 6:[18], 7:[19],8:[20]}
  #array to store plotted data points. Indices correspond with facilityTypeMap
  facilityVis = [[]for i in range(8)]

  #iterate through days of week
  for i in range(7):
    #iterate through hours of day
    for j in range(24):
      movePopulation(population, facilities, i, j)

      #store in arrays for our facility visualization
      #TODO: inefficient algorithm
      for k in range(0,8):
        #add to corresponding facility
        facilityVis[k].append(len(facilities[k+1][5]))




if __name__== "__main__":
  main()
