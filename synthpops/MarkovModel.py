import synthpops as sp
import numpy as np
import matplotlib.pyplot as plt
  
def transitionProb(currentState, population, i):
  # currently hard coded but these should be those diff eq / agent specific age + demographics
  b=0.2
  c=0.2
  d=0.3
  e=0.5

  a = 0
  s = {keys: 0 for keys in ['H', 'S', 'W']}
  beta = {'H': 0.1, 'S': 0.01, 'W': 0.02}
  totContactLayer = 0
  for k in ['H', 'S', 'W']:
    contactLayer = population[i]['contacts'][k]
    if len(contactLayer):
      s[k] = sum(currentState[j] == 'Mild' or currentState[j] == 'Severe' or currentState[j] == 'Critical' for j in contactLayer)
      totContactLayer += len(contactLayer)

  # for now no beta bc it decreases the probability by way too much i think
  # also this is totally wrong bc i normalized probabilities with #contacts which for sure is not right
  if (totContactLayer):
    a = sum(s[k] for k in ['H', 'S', 'W'])/totContactLayer#*beta[k]
  
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

def main():
  # synthpops stuff
  sp.validate()

  datadir = sp.datadir # this should be where your demographics data folder resides

  location = 'seattle_metro'
  state_location = 'Washington'
  country_location = 'usa'
  sheet_name = 'United States of America'
  level = 'county'

  npop = 1132 # how many people in your population
  num_households = 459
  num_workplaces = 200
  
  population, homes_dic = sp.generate_synthetic_population(npop, datadir, num_households, num_workplaces, location=location, state_location=state_location, country_location=country_location, sheet_name=sheet_name, plot=False, return_popdict=True)
  print(population)

  # initialize params
  timestep = 100
  states = ['Susceptible', 'Mild', 'Severe', 'Critical', 'Recovered', 'Dead']
  currentState = {key: states[0] for key in range(npop)}
  currentState[0] = 'Mild'
  currentState[1] = 'Severe'
  print(population[0]['contacts'])
  print(population[1]['contacts'])

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
      #print(p)

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

  plt.subplot(2,1,1)
  plt.plot(list(range(timestep)), infected)
  plt.title('infected')

  plt.subplot(2,1,2)
  plt.plot(list(range(timestep)), deaths)
  plt.title('deaths')

  plt.show()

  # pass results to VisualOutput.py
  return [results, infected, deaths]

if __name__== "__main__":
  main()