# Constraint Programming
# Implementing Different types of Search algorithms using OOP 
import ConstraintPropagators
from abc import ABCMeta, abstractmethod

class BasicSearch:
	"""
	Returns the index of the first decision variable whose domain length is not 1
	: Indicates nothing has been decided on this variable yet
	"""

	def search(self, domains):
		for idx,domain in enumerate(domains):
			if len(domain) != 1:
				return idx