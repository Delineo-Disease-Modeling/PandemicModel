import synthpops as sp
import json 

# Meant to intialize a "county" of cities 
class masterController():

  data = [] #list of dictionaries
  cities = {} #dictionary to store initialized city objects

  def __init__(self, filename):
    # Reads in json file and stores the data in the data instance variable
    jsonfile = open(filename, 'r')
    jsondata = jsonfile.read()
    self.data = json.loads(jsondata)

  def initializeCities(self):
    # For each city in the data
    for cityData in self.data:
      # Append the city object and name as a key value pair to the dictionary of cities
      self.cities[cityData["City_Name"]] = city(cityData)
  
    # For each city in the dictionary of cities
    for c in self.cities.values():
      #Initialize submodules and households for thhat city
      c.initializeSubModules()
      c.initializeHouseholds()

  # tester function
  def printData(self):
    print(self.data)
    print(self.cities)


class city(masterController):
  cityData = {} # dictionary containing city data
  submodules = [] # stores several submodule objects
  city_graph = {} # graph that stores city data
  households = [] # stores several household objects
   
  #include percent infected somewhere
  def __init__(self, data):
    self.cityData = data
    self.population = data["Population"]

  # TODO
  def initializeSubModules(self):
    # Initialize submodules

    # For the number 
    for i in range(3):
      self.submodules.append(subModule("submodule data", "filler_type"))
    #print(self.submodules)


  # TODO
  def initializeHouseholds(self):
    #Initialize households
    for i in range(3):
      self.households.append(household("household data"))
    #print(self.households)


# TODO 
class subModule(city):
  subModuleData = {}
  
  # data should have num visitors, average visit length, population density, etc.
  def __init__(self, data, modType):
    self.subModuleData = data
    self.modType = modType

# TODO
class household(city):
  householdData = {}

  def __init__(self, data):
    self.householdData = data

def main():           
  # exercise the class methods
  mc = masterController("file.json")
  mc.initializeCities()

  #mc.printData()
  print("HERE")
  sp.validate()

  datadir = sp.datadir # this should be where your demographics data folder resides

  location = 'seattle_metro'
  state_location = 'Washington'
  country_location = 'usa'
  sheet_name = 'United States of America'
  level = 'county'

  npop = 10000 # how many people in your population
  sp.generate_synthetic_population(npop,datadir,location=location, state_location=state_location,country_location=country_location,
  sheet_name=sheet_name,level=level)
  print("Population Created")


class node():
  def __init__(self, lat, lon, plus):
    self.latitude = lat 
    self.longitude = lon
    self.pluscode = plus

  def populateEdgeList(self):
    #Code to instantiate edgelist
    print()

  def createSubModule(self):
    self.subModule = subModule("submodule data", "filler_type")
  


"""
class graph():
  def __init__(self,gdict=None):
    if gdict is None:
      gdict = []
    self.gdict = gdict

  def getVertices(self):
    return list(self.gdict.keys())
"""

if __name__== "__main__":
  main()