def most_likely_states_for_person(timestamps=20, initial_prob={}, transition_matrix={}, likelihood_matrix={}, o_next=[]):
    '''
        This function takes in all relavant info of a person and calculates his state in all timestamps from his
        observable traits (in this case, the tests results / not tested status)
        It will output something like [0,0,0,0,1,2,3,...] as how the person's disease status progresses
    '''
    # 2 means not tested, 1 means tested negative, 0 means tested positive
    observations = [2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2,
                    2, 2, 2, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2]

    # the transition matrix from previous state qi to current state qj: currently also dummy values only
    a = 0
    b = 0.2
    c = 0.2
    d = 0.3
    e = 0.5

    # hard-coded for now but need to be replaced to take contacts into consideration
    # may vary from person to person, based on contacts and also socio-econ class, race, etc.
    transition_matrix = {
        'Susceptible': [1-a, a, 0, 0, 0, 0],                # state 0
        'Mild': [0, (1-c)/2, c, 0, (1-c)/2, 0],  # 1
        'Severe': [0, 0, (1-d)/2, d, (1-d)/2, 0],  # 2
        'Critical': [0, 0, 0, (1-e)/2, (1-e)/2, e],  # 3
        'Recovered': [1-b, 0, 0, 0, b, 0],  # 4
        'Dead': [0, 0, 0, 0, 0, 1]  # 5
    }

    error = 0.0001
    likelihood_matrix = {
        'Susceptible': [0, 0, 1],
        # a susceptible person has 0 prob of testing positive, 0 prob of testing negative,
        # 100% change of being untested since in the US only those showing symptoms would be tested
        'Mild': [0.1, error, 0.9-error],  # mild have 0.0001
        'Severe': [0.2, error, 0.8-error],
        'Critical': [0.4, error, 0.6-error],
        # no rationale, just making things up here. few recovered will be tested
        'Recovered': [error, 0.1-error, 0.9],
        # say if symptoms gets this bad they will definitely be tested positive. id Pr(pos | dead) = 1
        'Dead': [1, 0, 0]
    }

    # harded coded for now but needs to be replaced, eg by # of each category within the population / population size
    initial_prob = {
        'Susceptible': 0.99,
        'Mild': 0.009,
        'Severe': 0.001,
        'Critical': 0,
        'Recovered': 0,
        'Dead': 0
    }

    # initialize the disease states dictionary of one person's status at different times
    disease_states = {}
    for timestamp in range(0, timestamps+1):
        disease_states[timestamp] = 0

    # initialize for time zero
    for state in initial_prob.keys():
        observation = observations[0]
        initial_prob[state] = initial_prob[state] * \
            likelihood_matrix[state][observation]
    current_states = {}
    current_states = initial_prob
    next_state = 'Susceptible'
    state_prob = initial_prob['Susceptible']
    for state in initial_prob.keys():
        if initial_prob[state] > state_prob:
            next_state = state
            state_prob = initial_prob[state]
    disease_states[0] = next_state

    if timestamps == 1:
        return disease_states

    state_to_index = {
        'Susceptible': 0,
        'Mild': 1,
        'Severe': 2,
        'Critical': 3,
        'Recovered': 4,
        'Dead': 5
    }

    # recursive step
    for timestamp in range(1, timestamps + 1):
        observation = observations[timestamp]
        # a dict of all states (key) and the max likelihood of one path from one of the states from the previous timestamp
        max_prob_of_states = {key: 0 for key in likelihood_matrix.keys()}
        for state, max_likelihood in max_prob_of_states.items():
            # all probs from paths of each of the states (key) to state s from the previous timestamp t to t+1,
            # the maximum here would be put into max_prob_of_state as value of state s
            paths_from_previous_states = {
                key: 0 for key in likelihood_matrix.keys()}
            for (curr_state, likelihood) in paths_from_previous_states.items():
                likelihood = current_states[curr_state] * \
                    transition_matrix[curr_state][state_to_index[state]] * \
                    likelihood_matrix[state][observation]

            # manually magnify prob by x1000 times, otherwise too small, will print 0
            magnified_states_prob = {}
            for (curr_state, likelihood) in paths_from_previous_states.items():
                magnified_states_prob[curr_state] = 1000 * likelihood
            max_likelihood = max(magnified_states_prob.values())

        current_states = max_prob_of_states

        # pick the most likely state at the new timestamp: the one that gives the largest prob in max_prob_of_states
        next_state = 'Susceptible'
        temp_prob = max_prob_of_states['Susceptible']
        for state in max_prob_of_states.keys():
            if max_prob_of_states[state] > temp_prob:  # todo change
                temp_prob = max_prob_of_states[state]
                next_states = state
        disease_states[timestamp] = next_state

    print(disease_states)


if __name__ == "__main__":
    # hmm_propogation()
    most_likely_states_for_person()
