import synthpops as sp
import json 
from math import sin, cos, sqrt, atan2, radians
import json
from copy import deepcopy
import numpy as np

def dist(loc1, loc2):
  #print(loc1)
  #loc1 = [loc1["latitude"], loc1["longitude"]]
  #print(loc1)
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
  #print("HERE")
  #print(neighbour)
  #print(population[neighbour]['house'])
  reference_house = [population[neighbour]['house']["latitude"], population[neighbour]['house']["longitude"]]
  min_dist = dist(reference_house, far_loc)
  closest_house = 0
  count = 0

  # For each house dictionary in the houses list
  #print(type(houses))
  #print()
  #print(houses[0])
  #print()
  for i in range(len(houses)): 
    # If the house is unassigned
    #print(houses)
    #print(houses[i])
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
  

  # Assign the first person in the population to the first house
  #population[0]['house'] = housedata[0]

  # Mark the first house as assigned
  #housedata[0]["status"] = "A"
  #population[0]["status"] = "A"
  #prev_person = 0

  for person in population:
    house_dict = population[person]['house']
    

    # If the person in the population has NOT been assigned a house
    #if house_dict["latitude"] == 0 and house_dict["longitude"] == 0:

    if population[person]['status'] == "U":
      
      #print(person)
      #num_household_members = population[person]['contacts']['H']

      house_location = find_next_available_house(housedata)

      if house_location == -1:
        return

      house = housedata[house_location]

      housedata[house_location]["status"] = "A"
      #print(type(population[person]['house']))
      #print(type(house))
      population[person]['house'] = house
      population[person]['status'] = "A"
      
      #prev = population[prev_person]['house']
      #closest_house = find_next_closest_house(prev, housedata)
      
      #house = housedata[closest_house]

      #housedata[closest_house]["status"] = "A"

      #print(house)

      assign_household(person, population, house)
      assign_school_contacts(person, population, housedata)
      assign_workplace_contacts(person, population, housedata)
      

      household = population[person]["contacts"]["H"]

      for member in household:
        assign_school_contacts(member, population, housedata)
        assign_workplace_contacts(member, population, housedata)
        
      
    
    #if person > 0:
    #prev_person += 1
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

def temp_cn(population, housedata):
  temp_cn = {}
  large = ['hospitals', 'supermarkets', 'community_centres']

  temp_pop = deepcopy(population)

  for submodule in housedata:
    temp_contacts = {}
    for i in housedata[submodule]:
      if submodule in large:
        temp_people = np.random.choice(list(temp_pop.keys()),15).tolist()
        temp_contacts[i] = temp_people
        for i in temp_people:
          temp_pop.pop(i, None)
      else:
        temp_people = np.random.choice(list(temp_pop.keys()),5).tolist()
        temp_contacts[i] = temp_people
        #delete people from population
        for i in temp_people:
          temp_pop.pop(i, None)
    temp_cn[submodule] = temp_contacts
  #TODO: this # isn't constant
  print(str(len(temp_pop.keys())) + " people at either HH or work")

  return temp_cn

def main():           
  # exercise the class methods

  #mc.printData()
  sp.validate()

  datadir = sp.datadir # this should be where your demographics data folder resides

  location = 'seattle_metro'
  state_location = 'Washington'
  country_location = 'usa'
  sheet_name = 'United States of America'
  level = 'county'

  num_households = 459
  npop = 1132
  num_workplaces = 200

  submodule_dict = eval(open("dict.txt").read())
  
  with open("houses.json") as housejsonfile:
    housejsondata = json.load(housejsonfile)

# Mark each house as initially unassigned
  for i in range(len(housejsondata)):
    housejsondata[i]["status"] = "U"

  pop, homes_dic = sp.generate_synthetic_population(npop,datadir, num_households, num_workplaces, location=location, state_location=state_location,country_location=country_location,
  sheet_name=sheet_name, return_popdict=True)

  num_households = 0
  num_pop = 0
  for i in range(1,len(homes_dic) + 1):
    num_households = num_households + len(homes_dic[i])
    num_pop = num_pop + len(homes_dic[i]) * i
  #print("Population Created, total " + str(num_pop) + " people, " + str(num_households) + " households")

  population = pop

  for person in population:
    population[person]['house'] = {"latitude": 0, "longitude": 0}
    population[person]['status'] = "U"

  distribute_house(population, housejsondata, 0)

  print("0:" + str(population[0]))
  print("\n1:" + str(population[1]))

  temp_cn_dict = deepcopy(submodule_dict)

  del temp_cn_dict['households']
  del temp_cn_dict['schools']
  del temp_cn_dict['workplaces']

  #probability of 0.5 if you are in contact with them
  for i in range(24):
    print("\n Hour " + str(i))
    #at home
    if i in range(9) or i in range(22,24):
      #at school or work
      print("Household CN")
    elif i in range(9, 18):
      #at submodules 
      print("Proportion of School/Workplace CN")
    else:
      print(str(temp_cn(population, temp_cn_dict)) + "\n")
  

if __name__== "__main__":
  main()
