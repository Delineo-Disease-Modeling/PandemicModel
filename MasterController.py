#use pymongo to query from database
#import pymongo
#from Town import Town;
#from Agent import Agent;

class MasterController: 
    #initialize fields based on user input
    def __init__(self, county, state, time): #possible parameters: lockdown date, establishment
        self.county = county
        self.state = state
        self.town = makeTown()
        self.agent = makeAgent()
        self.countyData = getData()
        self.time = time #represents time point simulation is taking place 
        print("Hello")

    #query data from MongoDB
    def getData(self): 
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["Demographics"] 

        locQuery = { "Area_Name": self.county , "State": self.state}
        #query for population density, people per household, number of buildings, sub-modules, schools
        #get population density, people per household, number of buildings, sub-modules
        return countyData

    def makeTown(self):
        self.town = Town(countyData, time)
    
    def makeAgent(self):
        self.agent = Agent(countyData, time)
    
    def main():
        getData()
        makeTown()
        makeAgent()

    if __name__ == "__main__":
        main()

    #record return values from simulation based on time points and people infected 



        
