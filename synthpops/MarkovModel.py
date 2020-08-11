import synthpops as sp
import numpy as np
import matplotlib.pyplot as plt
import random
import pandas as pd

def transitionProb(currentState, population, i):
    # currently hard coded but these should be those diff eq / agent specific age + demographics
    b = 0.2
    c = 0.2
    d = 0.3
    e = 0.5

    a = 0
    s = {keys: 0 for keys in ['H', 'S', 'W']}
    beta = {'H': 0.1, 'S': 0.01, 'W': 0.02}
    for k in ['H', 'S', 'W']:
        contactLayer = population[i]['contacts'][k]
        if len(contactLayer):
            s[k] = sum(currentState[j] == 1 or currentState[j] ==
                       2 or currentState[j] == 3 for j in contactLayer)

    # normalize probability with total #infected in all contact networks
    if (sum(s.values())):
        a = sum(s[k]*beta[k] for k in ['H', 'S', 'W'])/sum(s.values())

    if (a > 1):
        raise Exception('probability>1')

    switch = {
        0: [1-a, a, 0, 0, 0, 0],
        1: [0, (1-c)/2, c, 0, (1-c)/2, 0],
        2: [0, 0, (1-d)/2, d, (1-d)/2, 0],
        3: [0, 0, 0, (1-e)/2, (1-e)/2, e],
        4: [1-b, 0, 0, 0, b, 0],
        5: [0, 0, 0, 0, 0, 1]
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

    # takes in custom param
    initial_list = get_user_input(npop)

    # initialize params
    timestep = 30
    #states = ['Susceptible', 'Mild', 'Severe', 'Critical', 'Recovered', 'Dead']
    states = np.arange(6) # this is for the heatmap visualization
    currentState = np.arange(npop)

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

    # initialize results list
    df = pd.DataFrame(columns=np.arange(timestep))
    df[0] = currentState
    nextState = np.empty((npop,), dtype=np.int32)
    infected = [0 for t in range(timestep)]
    newInfected = [0 for t in range(timestep)]
    deaths = [0 for t in range(timestep)]
    infected[0] = sum(currentState[j] == states[1] or currentState[j] ==
                    states[2] or currentState[j] == states[3] for j in population)
    deaths[0] = sum(currentState[j] == states[5] for j in population)

    # run simulation
    for t in range(timestep-1):
        for i in range(len(population)):
            # create transition probabilities for current state of ith agent
            p = transitionProb(df[t], population, i)

            # get next state with probability distribution p
            try:
                nextState[i] = np.random.choice(states, p=p)
            except:
                raise Exception('bad probability')

            # add to results
            if (nextState[i] == states[1] or nextState[i] == states[2] or nextState[i] == states[3]):
                infected[t+1] += 1
                # count Susceptible -> Mild
                if (df.at[i,t] == states[0]):
                    newInfected[t+1] += 1
            elif (nextState[i] == states[5]):
                deaths[t+1] += 1
        df[t+1] = nextState

    print("infected")
    print(infected)
    print("newly infected")
    print(newInfected)
    print("deaths")
    print(deaths)

    plt.figure()
    plt.plot(list(range(timestep)), infected, label='infected')
    plt.plot(list(range(timestep)), deaths, c='green', label='deaths')
    plt.plot(list(range(timestep)), newInfected, c='red', label='newly infected')
    plt.title('infected and deaths')
    plt.legend(loc=2)

    plt.figure()
    plt.pcolormesh(df, cmap='inferno_r')
    cbar = plt.colorbar(ticks=np.arange(6))
    cbar.ax.set_yticklabels(['Susceptible', 'Mild', 'Severe', 'Critical', 'Recovered', 'Dead'])
    plt.title('heatmap')
    state_list = df[timestep-1].tolist()
    su = 0
    m = 0
    se = 0
    c = 0
    r = 0
    d = 0
    for i in state_list:
        if (i == 0):
            su += 1
        if (i == 1):
            m += 1
        if (i == 2):
            se += 1
        if (i == 3):
            c += 1
        if (i == 4):
            r += 1;
        if (i == 5):
            d +=1
    plt.figure()
    objects = ('Susceptible', 'Mild', 'Severe', 'Critical', 'Recovered', 'Dead')
    y_pos = np.arange(len(objects))
    performance = [su,m,se,c,r,d]
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Number of people in state')
    plt.title('Infection states at end of time period')

    plt.figure()
    plt.pie(performance, labels=objects)
    plt.title('Percentage of people in infection state at end of time period')
    
    
    plt.show()

    # pass results to VisualOutput.py
    return [df, infected, deaths]


if __name__ == "__main__":
    main()
