"""
Distribute the population among all the houses.

Assign houses to individuals based on distance, starting with one reference person
1. Assign current person the current house
2. Assign household members the same house
3. Look through school contact layer for next person
4. If necessary, look through work layer for next person
5. If necessary, find next person with smallest index to assign house
"""

from math import sin, cos, sqrt, atan2, radians


def dist(loc1, loc2):
	"""
	Computes the distance betweens two locations. 
	Locations are in lattitude and longitude.

	Args:
		loc1 (tuple): first location
		loc2 (tuple): second location

	Return:
		The distance between loc1 and loc2, in km.
	"""
	# approximate radius of earth in km
	rad = 6373.0

	lat1 = radians(loc1[0])
	lon1 = radians(loc1[1])
	lat2 = radians(loc2[0])
	lon2 = radians(loc2[1])

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	return rad * c


def nearest_house(initial_house, houses, houses_used):
	"""
	Finds the nearest house.

	Args:
		initial_house (tuple)	: location of house to find the nearest to
		houses (list)			: list of house locations (tuples)
		houses_used (set)		: indexes of houses already used

	Return:
		The index of the nearest house to the given house.
	"""

	# Compute distances to each house and store by index of house
	distances = {}
	for i in range(len(houses)):
		if i not in houses_used:
			distances[i] = dist(houses[initial_house], houses[i])
		i += 1

	return min(distances)


def distribute_population(population, houses, initial_person=0, initial_house=0):
	"""
	Assigns each member of the population a house number.

	Args:
		population (list)	: list of `Person` objects
		houses (list)		: list of house locations (tuples)
		initial_person (int): index of initial person to start populating
		initial_house (int)	: index of initial house to start populating

	Return:
		N/A
	"""

	# Set of indices of houses already assigned
	houses_used = set()

	# Set of indices of people already assigned
	people_used = set()

	current_person = initial_person
	current_house = initial_house

	while len(population) != len(people_used):

		# Add current person/house to respective sets of used people/houses
		people_used.add(current_person)
		houses_used.add(current_house)

		# Assign each person in the household the same house
		population[current_person].house = current_house
		for person in population[current_person].house_layer:
			population[person].house = current_house
			people_used.add(person)

		# Stop if everyone has been assigned a house
		if len(population) == len(people_used):
			break

		# Find the nearest house to the current one
		current_house = nearest_house(current_house, houses, houses_used)

		new_person_found = False

		# Go through school layer to find next person
		for person in population[current_person].school_layer:
			if person not in people_used:
				current_person = person
				new_person_found = True
				break

		if new_person_found:
			continue

		# If no new classmates found, go through work layer
		for person in population[current_person].work_layer:
			if person not in people_used:
				current_person = person
				new_person_found = True
				break

		if new_person_found:
			continue

		# If still no new person found, start again at the first person
		for i in range(len(population)):
			if i not in people_used:
				current_person = i
				break


class Person:
	"""
	Person class contains H, S, W contact layers and a house number/index.
	House number defaults to -1.
	"""
	def __init__(self, house_layer, school_layer, work_layer, house=-1):
		self.house_layer = house_layer
		self.school_layer = school_layer
		self.work_layer = work_layer
		self.house = house

	def __str__(self):
		return "H: " + str(self.house_layer) + ", S: " + str(self.school_layer)\
		+ ", W: " + str(self.work_layer) + ", house: " + str(self.house)

	# Could add other methods like "add_house_contact", etc.


if __name__ == "__main__":
	"""
	Runs an example simulation.
	"""
	p0 = Person([], [1], [1, 2])
	p1 = Person([2], [0], [0, 2])
	p2 = Person([1], [], [])
	p3 = Person([], [], [])

	population = [p0, p1, p2, p3]
	houses = [(0, 0), (0, 1), (2, 2)]

	print(p0)
	print(p1)
	print(p2)
	print(p3)

	distribute_population(population, houses)

	print("POPULATION DISTRIBUTED")
	print(p0)
	print(p1)
	print(p2)
	print(p3)






