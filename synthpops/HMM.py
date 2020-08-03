import random


def most_likely_states_for_person(timestamps=20, initial_prob={}, transition_matrix={}, likelihood_matrix={}, observations=[]):
    '''
        This function takes in all relavant info of a person (transition matrix, likelihood matrix, observations, etc) 
        and calculates his state in all timestamps from his observable traits (in this case, the tests results / not tested status)

        It will output something like ['Susceptible', 'Susceptible', 'Mild', 'Severe', 'Dead', 'Dead', 'Dead', etc.] to represent how
        the person's disease status progresses (a path)
    '''
    # 2 means not tested, 1 means tested negative, 0 means tested positive
    # observations = [2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2]

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

    # the 3 possible observations are [tested positive, tested negative, untested]
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
        'Dead': [0.01, 0, 0.99]
    }

    # note on dead: Pr 0.1 for positive, 0.9 for untested does not mean 0.01 tested positive people died,
    # but people died on the day has 0.01 prob they tested on the day, and 0.99 prob they died w/out being tested

    # harded coded for now but needs to be replaced, eg by # of each category within the population / population size
    initial_prob = {
        'Susceptible': 0.99,
        'Mild': 0.009,
        'Severe': 0.001,
        'Critical': 0,
        'Recovered': 0,
        'Dead': 0
    }

    # helps to locate prob from one state at time t to another state at time t+1 in later steps
    state_to_index = {
        'Susceptible': 0,
        'Mild': 1,
        'Severe': 2,
        'Critical': 3,
        'Recovered': 4,
        'Dead': 5
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

    # this variable changes to 1 if 'Dead' appears in one timestamp, and sets all next steps to dead
    dead = 0

    # recursive step
    for timestamp in range(1, timestamps + 1):
        observation = observations[timestamp]

        if (dead == 1):
            disease_states[timestamp] = 'Dead'

        else:
            # a dict of all states (key) and the max likelihood of one path from one of the states from the previous timestamp
            max_prob_of_states = {key: 0 for key in likelihood_matrix.keys()}

            for state in max_prob_of_states.keys():
                # all probs from paths of each of the states (key) to state s from the previous timestamp t to t+1,
                # the maximum here would be put into max_prob_of_state as value of state s
                paths_from_previous_states = {
                    key: 0 for key in likelihood_matrix.keys()}

                # if this is 1, each probability will be magnified by 100 times
                # cuz if calc likelihood is too small it will be rounded off to 0
                magnify = 0
                for (curr_state, likelihood) in paths_from_previous_states.items():
                    # aims to guarantee total number does not become 0. need to change
                    if (curr_state == 'Suspicious' and likelihood <= 0.01):
                        magnify = 1
                        likelihood = 1000 * current_states[curr_state] * \
                            transition_matrix[curr_state][state_to_index[state]] * \
                            likelihood_matrix[state][observation]
                    elif (curr_state != 'Suspicious' and magnify == 1):
                        likelihood = 1000 * current_states[curr_state] * \
                            transition_matrix[curr_state][state_to_index[state]] * \
                            likelihood_matrix[state][observation]
                    else:
                        likelihood = current_states[curr_state] * \
                            transition_matrix[curr_state][state_to_index[state]] * \
                            likelihood_matrix[state][observation]
                    paths_from_previous_states[curr_state] = likelihood
                max_prob_of_states[state] = max(
                    paths_from_previous_states.values())

                magnify = 0

            ############## for debugging #################
            if (timestamp == 13):
                print(str(timestamp) + ':')
                print(max_prob_of_states)

            if (timestamp == 14):
                print(str(timestamp) + ':')
                print(max_prob_of_states)

            current_states = max_prob_of_states

            # pick the most likely state at the new timestamp: the one that gives the largest prob in max_prob_of_states
            next_state = 'Susceptible'
            temp_prob = max_prob_of_states['Susceptible']
            for state in max_prob_of_states.keys():
                if max_prob_of_states[state] > temp_prob:  # todo change
                    temp_prob = max_prob_of_states[state]
                    next_state = state
            disease_states[timestamp] = next_state
            if next_state == 'Dead':
                dead = 1

    print(disease_states)


def generate_observations_for_population(npop=2000, records_by_day={}):
    """
        This function takes in total population and a dict of positive and negative tests results over the days, and
        distribute the new diagnosis among people.

        sample input: 
        {
            8/1/2020: {
                positive: 20,
                negative: 80,
                untested: 900,
            },
            8/2/2020:{}
        } // a total of 10 days

        sample output: {
            0: [2 2 2 2 1 2 2 2 2 2],   // array of length 10
            1: [2 2 0 2 2 2 2 2 2 1],...
        }

        *** note on state ***
        0 = tested positive
        1 = tested negative
        2 = untested

        For any day between a person's two consecutive tests, their status is 2. 
    """

    # dummy for now
    records_by_day = {
        0: {
            'positive': 0,
            'negative': 0,
        },
        1: {
            'positive': 1,
            'negative': 2,
        },
        2: {
            'positive': 3,
            'negative': 2,
        },
        3: {
            'positive': 10,
            'negative': 9,
        },
        4: {
            'positive': 19,
            'negative': 21,
        },
        5: {
            'positive': 29,
            'negative': 25,
        },
        6: {
            'positive': 45,
            'negative': 26,
        },
        7: {
            'positive': 50,
            'negative': 30,
        },
        8: {
            'positive': 48,
            'negative': 46,
        },
        9: {
            'positive': 53,
            'negative': 70,
        },
        10: {
            'positive': 61,
            'negative': 82,
        },
    }

    # use sets to track people's last diagnose and days since the diagnose
    tested_positive = set()
    tested_negative = set()
    results = {}

    for i in range(0, npop):
        results[i] = []

    # use a naive algorithm for now, cannot get rid of cases like 01010
    total_days = len(records_by_day)
    for i in range(0, total_days):
        num_positive = records_by_day[i]['positive']
        num_negative = records_by_day[i]['negative']

        # assign to people's indices of who tested positive this day
        for j in range(0, num_positive):
            next_pos = random.randint(0, npop)
            while next_pos in tested_positive:
                next_pos = random.randint(0, npop)
            tested_positive.add(next_pos)

        # assign to people's indices of who tested negative this day
        for k in range(0, num_negative):
            next_pos = random.randint(0, npop)
            while next_pos in tested_negative or next_pos in tested_positive:
                next_pos = random.randint(0, npop)
            tested_negative.add(next_pos)

        for person in results.keys():
            if person in tested_positive:
                results[person].append(0)
            elif person in tested_negative:
                results[person].append(1)
            else:
                results[person].append(2)

        tested_positive.clear()
        tested_negative.clear()

    return results


if __name__ == "__main__":
    # hmm_propogation()
    # most_likely_states_for_person()
    status_for_each_person = generate_observations_for_population()
    for person in status_for_each_person.keys():
        observations = status_for_each_person[person]
        most_likely_states_for_person(timestamps=10, observations=observations)
