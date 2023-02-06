import numpy as np
import pandas as pd
import random
import yaml

'''
    GLOBAL VARIABLES
'''

'''
    Classe Definitions to use in pop_mov_sim
'''

class Person:

    '''
    Class for each individual
    '''

    def __init__(self, id, sex, age, cbg, household):
        self.id = id
        self.sex = sex #male 0 female 1
        self.age = age
        self.cbg = cbg
        self.household = household

class Population:

    '''
    Class for storing population
    '''

    def __init__(self):
        #total population
        self.total_count = 0
        #container for persons in the population
        self.population = []
    
    def populate_indiv(self, person):
        '''

        Populates the population with the person object

        @param person = Person class object to be added to population

        '''
        
        #adding population
        self.population = np.append(self.population, person)

class Household(Population):

    ''' 
    Household class, inheriting Population since its a small population
    '''

    def __init__(self, cbg, population=[], total_count=0):
        # super().__init()
        self.cbg = cbg
        self.population = population
        self.total_count = total_count


    def add_member(self, person):
        '''
        Adds member to the household, with sanity rules applied
        @param person = person to be added to household
        '''
        self.population.append(person)

    #TODO: Add more functions for leaving/coming back, etc if needed
    #jiwoo: an idea would be to extend from the population info to create
    #more realistic dataset (combination) of population in a household
    
'''
    if ran(not imported), yields household assignment values
'''
if __name__=="__main__":

    #HELPER FUNCTIONS

    def create_households(pop_data, households, cbg):
        result = []
        '''
            FOR INFORMATION: family_percents = [married, opposite_sex, samesex, female_single, male_single, other]
        '''
        married, opposite_sex, samesex, female_single, male_single, other = 0, 1, 2, 3, 4, 5
        
        for i in range(int(households * pop_data['family_percents'][married] * 0.01)):
            result.append(create_married_hh(pop_data, cbg))

        for i in range(int(households * pop_data['family_percents'][samesex] * 0.01)):
            result.append(create_samesex_hh(pop_data, cbg))

        for i in range(int(households * pop_data['family_percents'][opposite_sex] * 0.01)):
            result.append(create_oppositesex_hh(pop_data, cbg))

        for i in range(int(households * pop_data['family_percents'][female_single] * 0.01)):
            result.append(create_femsingle_hh(pop_data, cbg))

        for i in range(int(households * pop_data['family_percents'][male_single] * 0.01)):
            result.append(create_malesingle_hh(pop_data, cbg))
        
        for i in range(int(households * pop_data['family_percents'][other] * 0.01)):
            result.append(create_other_hh(pop_data, cbg))

        return result     

    def create_married_hh(pop_data, cbg):

        household = Household(cbg)

    
        age_percent = pop_data['age_percent_married']
        age_group = random.choices(pop_data['age_groups_married'], age_percent)[0]
        
        husband_age = random.choice(range(age_group, age_group+10))
        household.add_member(Person(pop_data['count'], 0, husband_age, cbg, household))
        pop_data['count'] += 1
        wife_age = random.choice(range(age_group, age_group+10))
        household.add_member(Person(pop_data['count'], 1, wife_age, cbg, household))
        pop_data['count'] += 1

        # if there will be children. Old couples have less percent TODO get percents
        #jiwoo: are the numbers 0.1 and 0.05 statistically proven, or are these arbitrary numbers so far?
        children_percent = pop_data['children_true_percent']+0.1 if (age_group < 45 and age_group > 15) else 0.05

        child_bool = random.choices([True, False], [children_percent, 100-children_percent])[0]

        if child_bool:
            num_child = random.choices(pop_data['children_groups'], pop_data['children_percent'])[0]
            for i in range(num_child):
                household.add_member(Person(pop_data['count'], random.choices([0, 1], [pop_data['male_percent'], pop_data['female_percent']])[0], random.choice(range(1, 19)), cbg, household))
                pop_data['count'] += 1
        
        return household

    #jiwoo: for functions that create household with diff combinations of sex, consider
    #creating a separate helper function for the overlapping lines of code for increased efficiency
        
    def create_samesex_hh(pop_data, cbg):

        household = Household(cbg)

        age_percent = pop_data['age_percent']
        age_group = random.choices(pop_data['age_groups'], age_percent)[0] #i'm talking about these lines
        
        husband_age = random.choice(range(age_group, age_group+10))
        wife_age = random.choice(range(age_group, age_group+10))

        gender = random.choices([0, 1], [pop_data['male_percent'], pop_data['female_percent']])[0]
        household.add_member(Person(pop_data['count'], gender, husband_age, cbg, household))
        pop_data['count'] += 1
        household.add_member(Person(pop_data['count'], gender, wife_age, cbg, household))
        pop_data['count'] += 1

        return household

    def create_oppositesex_hh(pop_data, cbg):

        household = Household(cbg)

        age_percent = pop_data['age_percent']
        age_group = random.choices(pop_data['age_groups'], age_percent)[0]
        
        husband_age = random.choice(range(age_group, age_group+10))
        wife_age = random.choice(range(age_group, age_group+10))

        household.add_member(Person(pop_data['count'], random.choices([0, 1], [pop_data['male_percent'], pop_data['female_percent']])[0], husband_age, cbg, household))
        pop_data['count'] += 1
        household.add_member(Person(pop_data['count'], random.choices([0, 1], [pop_data['male_percent'], pop_data['female_percent']])[0], wife_age, cbg, household))
        pop_data['count'] += 1

        return household

    def create_femsingle_hh(pop_data, cbg):
        household = Household(cbg)

        age_percent = pop_data['age_percent']
        age_group = random.choices(pop_data['age_groups'], age_percent)[0]
        
        age = random.choice(range(age_group, age_group+10))

        household.add_member(Person(pop_data['count'], 1, age, cbg, household))
        pop_data['count'] += 1

        return household

    def create_malesingle_hh(pop_data, cbg):
        household = Household(cbg)

        age_percent = pop_data['age_percent']
        age_group = random.choices(pop_data['age_groups'], age_percent)[0]
        
        age = random.choice(range(age_group, age_group+10))

        household.add_member(Person(pop_data['count'], 0, age, cbg, household))
        pop_data['count'] += 1

        return household

    def create_other_hh(pop_data, cbg):
        household = Household(cbg)

        age_percent = pop_data['age_percent']
        age_group = random.choices(pop_data['age_groups'], age_percent)[0]
        
        size_percent = pop_data['size_percent']
        size_group = random.choices(pop_data['size_groups'], size_percent)[0]
        
        for i in range(size_group):
            age = random.choice(range(age_group, age_group+10))
            household.add_member(Person(pop_data['count'], random.choices([0, 1], [pop_data['male_percent'], pop_data['female_percent']])[0], age, cbg, household))
            pop_data['count'] += 1
        
        return household

    def visualize_household(household):
        print("ANALYZING HOUSEHOLD " + str(household))
        print("The current household has "+ str(len(household.population)) + " members.")
        for i in range(len(household.population)):
            print("member " + str(i) + ": ")
            print("id: " + str(household.population[i].id))
            print("sex(0 is male): " + str(household.population[i].sex))
            print("age: " + str(household.population[i].age))

    def create_pop_from_cluster(cluster, census_df):
        populations = 0
        households = 0
        for i in cluster:
            i = int(i)
            populations += (int(census_df[census_df.census_block_group == i].values[0][1]))
            households += (int(census_df[census_df.census_block_group == i].values[0][3]))

        return populations, households

    # reading population information from yaml file
    pop_data = {}

    with open('population_info.yaml', mode="r", encoding="utf-8") as file:
        pop_data = yaml.full_load(file)

    print(pop_data) #TODO delete

    # Reading Census Information
    census_info = "safegraph_cbg_population_estimate.csv"
    census_df = pd.read_csv(census_info)

    # HELPER FUNCTIONS

    # read clusters into string array in order to easier census search
    cluster_df = pd.read_csv('clusters.csv')
    clusters = [str(i) for i in list(cluster_df['cbgs'])]

    household_list = []

    # get number of households
    for cbg in clusters:
        _, household = create_pop_from_cluster([cbg], census_df)
        household_list.append(create_households(pop_data, household, cbg))

    # Dump household list data into households.yaml file
    with open('households.yaml', mode="wt", encoding="utf-8") as outstream:
        yaml.dump(household_list, outstream)

    print("Successfully Created Households")
    

    
    



    

    

    

    



    
    


    