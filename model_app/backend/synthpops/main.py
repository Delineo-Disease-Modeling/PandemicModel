import synthpops as sp
import json 

# Meant to intialize a "county" of cities 
class masterController():

  data = [] #list of dictionaries
  cities = {} #dictionary to store initialized city objects
  households = {} #dictionary to store household locations 
  dict = {} #all submodules

  def __init__(self, filename, dictname):
    # Reads in json file and stores the data in the data instance variable
    jsonfile = open(filename, 'r')
    jsondata = jsonfile.read()
    self.data = json.loads(jsondata)
    self.dict = eval(open(dictname).read())

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
    print(self.dict)


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
  mc = masterController("file.json", "dict.txt")
  mc.initializeCities()

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

  pop, homes_dic = sp.generate_synthetic_population(npop,datadir, num_households, num_workplaces, location=location, state_location=state_location,country_location=country_location,
  sheet_name=sheet_name, return_popdict=True)

  #print(pop) #uncomment to print population dictionary
  #print(homes_dic) #uncomment to print households of every size
  num_households = 0
  num_pop = 0
  for i in range(1,len(homes_dic) + 1):
    num_households = num_households + len(homes_dic[i])
    num_pop = num_pop + len(homes_dic[i]) * i
  print("Population Created, total " + str(num_pop) + " people, " + str(num_households) + " households")


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
