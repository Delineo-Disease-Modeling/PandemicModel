

def hmm_propogation(npop=10, population_dict={}, observables={}, states=[], total_timestamps=10):
    """
        This function creates a graph coupled hidden Markov Model and update disease state from each day.

        ## missing: param explanations for now
    """

    # too few people, keep it low
    total_timestamps = 3

    population_dict = {}
    # initialize
    for i in range(0, npop):
        population_dict[i] = {'state': -1, 'observable': 0}

    # we decided to go with num of positive tests, num of negative tests, num of untested as three observables
    observables = {}
    for i in range(0, total_timestamps):
        observables[i] = {'positive': i, 'negative': i, 'untested': npop - 2*i}

    # dummy graph: unchanging network for all timestamps, will supply an actual network
    # use adjencency list since graph likely to be sparse, this will be quicker
    network_permanent = {  # we can assume this is all household network only for now
        0: [1, 2, 3],
        1: [0, 2, 3],
        2: [0, 1, 3],
        3: [0, 1, 2],
        4: [5],
        5: [4],
        6: [],
        7: [8, 9],
        8: [7, 9],
        9: [7, 8],
    }

    # dictionary of timestamp:graph_of_networks
    network_dict = {}
    # i put 100 timestamps of unchanging networks here
    for i in range(0, total_timestamps):
        network_dict[i] = network_permanent

    states_at_timestamps = {}
    for i in range(0, total_timestamps):
        states_at_timestamps[i] = {'susceptible': 0, 'mild': 0,
                                   'severe': 0, 'Critical': 0, 'Recovered': 0, 'Dead': 0}

    # the transition matrix from previous state qi to current state qj: currently also dummy values only
    b = 0.2
    c = 0.2
    d = 0.3
    e = 0.5

    transition_matrix = {
        'Susceptible': [1-a, a, 0, 0, 0, 0],
        'Mild': [0, (1-c)/2, c, 0, (1-c)/2, 0],
        'Severe': [0, 0, (1-d)/2, d, (1-d)/2, 0],
        'Critical': [0, 0, 0, (1-e)/2, (1-e)/2, e],
        'Recovered': [1-b, 0, 0, 0, b, 0],
        'Dead': [0, 0, 0, 0, 0, 1]
    }

    # observation_likelihood: the state observation likelihood of the observation symbol o_t given
    # the current state j
    error = 0.0001  # tested, actually sick but results coming negative
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

    # calculation of disease spreading


if __name__ == "__main__":
    hmm_propogation()
