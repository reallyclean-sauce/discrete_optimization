"""
Problem: Map Coloring

Problem Definition:
You have a whole map which is composed of different countries. 
Each country has its own neighboring couuntries. For each country, a color should be assigned. However, no neighboring country should have the same color.

Goal:
Assign colors to each country while ensuring that no neighboring country has the same color.

Model:
Neighbors and Country and Color
"""

# Optimization Problem
# Decision Variable: Color
# Constraint: country_color[country] != country_color[neighbors[country]]  for all neighbors
# Find country color combination when given a single country color

from copy import deepcopy

#Given:
colors = ['gray', 'yellow', 'green', 'brown']
countries = ['Belgium', 'Denmark', 'France', 'Germany',
			'Netherlands', 'Luxemborg']
neighbors = {
	'Belgium': ['France', 'Germany', 'Netherlands', 'Luxemborg'],
	'Denmark': ['Germany'],
	'France': ['Belgium', 'Germany', 'Luxemborg'],
	'Germany': ['Belgium', 'France', 'Luxemborg', 'Netherlands'],
	'Netherlands': ['Belgium', 'Germany'],
	'Luxemborg': ['Belgium', 'France', 'Germany']				
}


# Constraint Programming
# DS: Search Space / Domain Store for Each Country
# Constraints: Setting a color for a country
# Propagation_Engine: Feasibility Checking, Pruning

DS = {}
for country in countries:
	DS[country] = deepcopy(colors)


# Assigning color -> Assigning constraint
country_color = {}
for country in countries:
	country_color[country] = None

# Basic Propagation engine
while True:
	# Search Store
	# Sending constraints to Constraint Store
	chosen_country = input("Choose country: ")
	if chosen_country not in countries:
		print("Invalid country")
		continue

	mode = input("Choose Mode: ")
	
	country_color[chosen_country] = input("Choose color: ")
	if country_color[chosen_country] not in colors:
		print("Invalid color")
		country_color[chosen_country] = None
		continue



	# Constraint Store
	
	# Feasibility Checking
	# Check if constraint will find a solution
	feasible = True
	for country in countries:

		if country_color[country] is None:
			continue

		for neighbor in neighbors[country]:
			if country_color[country] == country_color[neighbor]:
				feasible = False

	if not feasible:
		print("Constraint is not feasible!")
		print("Choose another constraint")
		country_color[chosen_country] = None
		break


	# Pruning Algorithm
	# Two types of Pruning Algorithm:
	# # Assigning a color for a country
	# # Preventing a color to be assigned to a country
	if mode == 'a':
		DS[chosen_country] = [country_color[chosen_country]]
		for neighbor in neighbors[chosen_country]:
			if country_color[chosen_country] in DS[neighbor]:
				DS[neighbor].remove(country_color[chosen_country])
	elif mode == 'p':
		DS[chosen_country].remove(country_color[chosen_country])
	else:
		print("Chosen mode is not available")

	for country in countries:
		if len(DS[country]) == 1:
			country_color[country] = DS[country][0]
			for neighbor in neighbors[country]:
				if country_color[country] in DS[neighbor]:
					DS[neighbor].remove(country_color[country])


	# Check if there are any values left to be pruned
	count = 0
	for country in DS:
		if len(DS[country]) == 1:
			count += 1

	if count == len(DS.keys()):
		print("Color Combination chosen:")
		for country in countries:
			print(country, country_color[country])
		break


	print("New Domain Store after setting France to Gray")
	for country in DS:
		print(country)
		print(DS[country])