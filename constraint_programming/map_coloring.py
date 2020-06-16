# Implementing MapColoring problem using OOP 
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
from copy import deepcopy
from abc import ABCMeta, abstractmethod

class Given:
	colors = {'gray', 'yellow', 'green', 'brown'}
	countries = {'Belgium', 'Denmark', 'France', 'Germany',
				'Netherlands', 'Luxemborg'}
	neighbors = {
		'Belgium': {'France', 'Germany', 'Netherlands', 'Luxemborg'},
		'Denmark': {'Germany'},
		'France': {'Belgium', 'Germany', 'Luxemborg'},
		'Germany': {'Belgium', 'France', 'Luxemborg', 'Netherlands'},
		'Netherlands': {'Belgium', 'Germany'},
		'Luxemborg': {'Belgium', 'France', 'Germany'}
	}

	def __str__(self):
		return "Possible Countries are: {}\nPossible Colors are: {}".format(Given.countries,Given.colors)


class DomainStore(Given):
	"""Search Space
	for all the possible decision variables
	for all the countries
	"""
	search_space = {}
	for country in Given.countries:
		search_space[country] = deepcopy(Given.colors)


	def showSearchSpace(self):
		for country in Given.countries:
			print(country, DomainStore.search_space[country])



class PropagationEngine(DomainStore):
	def feasibility_check(self,country):
		"""Feasibility Checking
		Check if constraint will find a solution
		"""
		feasible = True
		for c in Given.countries:
			for n in Given.neighbors[c]:
				# print(type(DomainStore.search_space[c]),c)
				# print(type(DomainStore.search_space[n]),n)
				if len(DomainStore.search_space[c] | DomainStore.search_space[n]) == 1:
					feasible = False
					print(DomainStore.search_space[c],c)
					print(DomainStore.search_space[n],n)

		return feasible

	def prune(metaclass=ABCMeta): pass


	def prunability(self):
		"""Check for Prunability
		Checks if we have found a solution
		"""
		solution = True
		for c in Given.countries:
			for n in Given.neighbors[c]:
				if (len(DomainStore.search_space[c] | DomainStore.search_space[n]) != 2) and \
					(len(DomainStore.search_space[c] & DomainStore.search_space[n]) == 0):
					solution = False

		return solution


	def propagate(self,country,color):
		"""Perform Propagation
		"""
		self.prune(country,color)


		if not self.feasibility_check(country):
			raise Exception("Constraint is not feasible!")

		result = self.prunability()
		if result:
			print("Solution")
			self.showSearchSpace()
			return True
		else:
			print("Current Domain Space")
			self.showSearchSpace()
			return False
			


class AssignColor(PropagationEngine):
	def prune(self,country,color):
		"""Prunes the DomainStore
		when a Color is assigned to a Country
		"""

		# Reduce DomainSpace to 1 of the Country
		DomainStore.search_space[country] = {color}

		# Prune the DomainSpace according to the model
		for neighbor in Given.neighbors[country]:
			if color in DomainStore.search_space[neighbor]:
				DomainStore.search_space[neighbor].discard(color)

				# Prune if a country has only one choice left
				if len(DomainStore.search_space[neighbor]) == 1:
					for n in Given.neighbors[neighbor]:
						for neighbor_color in DomainStore.search_space[neighbor]: pass

						if neighbor_color in DomainStore.search_space[n]:
							DomainStore.search_space[n].discard(neighbor_color)



class PreventColor(PropagationEngine):
	def prune(self,country,color):
		"""Prunes the DomainStore
		when a Color is not allowed to be a value for the Country
		"""
		print("PREVENTING:!!")
		print(DomainStore.search_space[country])
		DomainStore.search_space[country].discard(color)
		print(DomainStore.search_space[country])

		
if __name__ == "__main__":
	p = {10,12}
	print(p)

	assign_color = AssignColor()
	prevent_color = PreventColor()
	given = Given()
	while True: 
		print(given)
		country = input("Choose a Country: ")
		color = input("Choose a Color: ")
		mode = input("Choose mode:")
		print("\n\n\n\n\n\n\n\n")
		if mode == 'a':
			result = assign_color.propagate(country,color)
		elif mode == 'p':
			result = prevent_color.propagate(country,color)
		else:
			print("Invalid mode")
			continue

		if result:
			break

	