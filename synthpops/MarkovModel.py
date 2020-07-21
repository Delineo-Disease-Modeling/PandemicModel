import synthpops as sp
import numpy as np
import matplotlib.pyplot as plt
import random


def transitionProb(currentState, population, i):
    # currently hard coded but these should be those diff eq / agent specific age + demographics
    b = 0.2
    c = 0.2
    d = 0.3
    e = 0.5

    a = 0
    s = {keys: 0 for keys in ['H', 'S', 'W']}
    beta = {'H': 0.1, 'S': 0.01, 'W': 0.02}
    totContactLayer = 0
    for k in ['H', 'S', 'W']:
        contactLayer = population[i]['contacts'][k]
        if len(contactLayer):
            s[k] = sum(currentState[j] == 'Mild' or currentState[j] ==
                       'Severe' or currentState[j] == 'Critical' for j in contactLayer)
            totContactLayer += len(contactLayer)

    # for now no beta bc it decreases the probability by way too much i think
    # also this is totally wrong bc i normalized probabilities with #contacts which for sure is not right
    if (totContactLayer):
        a = sum(s[k] for k in ['H', 'S', 'W'])/totContactLayer  # *beta[k]

    if (a > 1):
        raise Exception('probability>1')

    switch = {
        'Susceptible': [1-a, a, 0, 0, 0, 0],
        'Mild': [0, (1-c)/2, c, 0, (1-c)/2, 0],
        'Severe': [0, 0, (1-d)/2, d, (1-d)/2, 0],
        'Critical': [0, 0, 0, (1-e)/2, (1-e)/2, e],
        'Recovered': [1-b, 0, 0, 0, b, 0],
        'Dead': [0, 0, 0, 0, 0, 1]
    }
    return switch[currentState[i]]


def get_user_input(npop):
    valid_single_input = False
    valid_total = False

    while not valid_total:
        print("Input the integer of initial patients with mild symptoms:")
        # check input is int and range
        while not valid_single_input:
            try:
                mild = int(input())
                if mild > npop:
                    print("Input exceeds population total " +
                          npop + ". Please input again:")
                elif mild < 0:
                    print("Input is negative. Please input again:")
                else:
                    valid_single_input = True
            except:
                print("Input is not an integer. Please input again:")
        valid_single_input = False

        print("Input the integer of initial patients with severe symptoms:")
        # check input is int and range
        while not valid_single_input:
            try:
                severe = int(input())
                if severe > npop:
                    print("Input exceeds population total " +
                          npop + ". Please input again:")
                elif severe < 0:
                    print("Input is negative. Please input again:")
                else:
                    valid_single_input = True
            except:
                print("Input is not an integer. Please input again:")
        valid_single_input = False

        print("Input the integer of initial patients with critical symptoms:")
        # check input is int and range
        while not valid_single_input:
            try:
                critical = int(input())
                if critical > npop:
                    print("Input exceeds population total " +
                          npop + ". Please input again:")
                elif critical < 0:
                    print("Input is negative. Please input again:")
                else:
                    valid_single_input = True
            except:
                print("Input is not an integer. Please input again:")
        valid_single_input = False

        print("Input the integer of initial patients who have been recovered with antibodies, if any (*Note: recover ≠ susceptible*):")
        while not valid_single_input:
            try:
                recovered = int(input())
                if recovered > npop:
                    print("Input exceeds population total " +
                          npop + ". Please input again:")
                elif recovered < 0:
                    print("Input is negative. Please input again:")
                else:
                    valid_single_input = True
            except:
                print("Input is not an integer. Please input again:")
        valid_single_input = False

        total_ever_sick = mild + severe + critical + recovered
        if (total_ever_sick <= npop):
            susceptible = npop - mild - severe - critical - recovered
            initial_dict = [susceptible, mild, severe, critical, recovered]
            print("You have input that, in the population of size " + str(npop) + ", there are " + str(mild) + " number of patients with mild symptoms, " + str(severe) + " number of patients with severe symptoms, " +
                  str(critical) + " number of patients with critical symptoms, " + str(recovered) + " recovered patients, and " + str(susceptible) + " susceptible people. Press y to confirm.")
            confirm = input()
            if confirm == "y" or confirm == "Y":
                valid_total = True
                return initial_dict
            else:
                print("Please start from beginning.\n")
        else:
            print("The total number of mild, severe, critical and recovered patients exceeds population, please start from beginning.\n")


def main():
    # synthpops stuff
    sp.validate()

    datadir = sp.datadir  # this should be where your demographics data folder resides

    location = 'seattle_metro'
    state_location = 'Washington'
    country_location = 'usa'
    sheet_name = 'United States of America'
    level = 'county'

    npop = 1132  # how many people in your population
    num_households = 459
    num_workplaces = 200

    population, homes_dic = sp.generate_synthetic_population(npop, datadir, num_households, num_workplaces, location=location,
                                                             state_location=state_location, country_location=country_location, sheet_name=sheet_name, plot=False, return_popdict=True)
    #print(population)

    # takes in custom param
    initial_list = get_user_input(npop)

    # initialize params
    timestep = 100
    states = ['Susceptible', 'Mild', 'Severe', 'Critical', 'Recovered', 'Dead']
    currentState = {key: states[0] for key in range(npop)}
    currentState[0] = 'Mild'
    currentState[1] = 'Severe'  # todo
    print(population[0]['contacts'])
    print(population[1]['contacts'])


    # set initial state params from initial_list
    populationKeys = list(population.keys()); 
    random.shuffle(populationKeys) 

    start = 0
    for num in range(len(initial_list)): 
        end = start + initial_list[num]
        for z in range (start, end): 
            index = populationKeys[z]
            currentState[index] = states[num] 
        start = end

    # intialize results list
    results = {}
    nextState = {key: states[0] for key in range(npop)}
    infected = [0 for t in range(timestep)]
    deaths = [0 for t in range(timestep)]

    # run simulation
    for t in range(timestep):
        results[t] = currentState
        for i in range(len(population)):
            # create transition probabilities for current state of ith agent
            p = transitionProb(currentState, population, i)
            # print(p)

            # get next state with probability distribution p
            try:
                nextState[i] = np.random.choice(states, p=p)
            except:
                print(i)
                print(p)
                print(currentState[i])
                raise Exception('bad probability')

            # add to results
            if (nextState[i] == 'Mild' or nextState[i] == 'Severe' or nextState[i] == 'Critical'):
                infected[t] += 1
            elif (nextState[i] == 'Dead'):
                deaths[t] += 1

            currentState = nextState

    print("infected")
    print(infected)
    print("deaths")
    print(deaths)

    plt.subplot(2, 1, 1)
    plt.plot(list(range(timestep)), infected)
    plt.title('infected')

    plt.subplot(2, 1, 2)
    plt.plot(list(range(timestep)), deaths)
    plt.title('deaths')

    plt.show()

    # pass results to VisualOutput.py
    return [results, infected, deaths]


if __name__ == "__main__":
    main()
