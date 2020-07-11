# Constraint Programming Modules
# These are the required classes to create a Constraint Programming solution
from abc import ABCMeta, abstractmethod
import json
from collections import namedtuple
from ConstraintPropagators import NotEqualPropagator, EqualityPropagator
import SearchUtils
import time
from copy import deepcopy
import sys

def str_to_class(classname):
	return getattr(sys.modules[__name__], classname)

Constraint = namedtuple("Constraint", ['type', 'left', 'right'])

class Reader:
	@abstractmethod
	def format(self,input_data): pass
		

class ConstraintModel:
	"""
	Implementation of the chosen 
	Constraint Programming Model
	as set of constraints
	"""
	def __init__(self):
		self.constraints = []

	def get_constraints(self): 
		return self.constraints

	def add(self, constraint):
		self.constraints.append(constraint)


class Initializer:
	"""
	Initializes constraint Model
	Which also initialzes domain_store
	"""
	def init_constraint_store(self, model):
		constraint_store = []
		for constraint in model.constraints:
			constraint_store.append(constraint)

		return constraint_store

	def init_propagation_engine(self,constraint_store):
		engine = PropagationEngine()
		for constraint in constraint_store:
			service = str_to_class(constraint.type+'Propagator')
			engine.propagators[constraint.type] = service()

		service = str_to_class('EqualityPropagator')
		engine.propagators['Equality'] = service()

		return engine

	def init_propagators(self,constraint_store):
		propagators = {}
		for constraint in constraint_store:
			service = str_to_class(constraint.type+'Propagator')
			propagators[constraint.type] = service()

		service = str_to_class('EqualityPropagator')
		propagators['Equality'] = service()

		return propagators


	def init_domain_store(self,items,model): 
		domain_store = {}

		for item in items:
			domain_store['vars'].append(None)

			temp_dict = {}
			for name,value in item._asdict().iteritems():
				temp_dict[name] = value	
			domain_store['var_attrs'].append(temp_dict)

		domain_store['domains'] = model.initialize_domain()

		return domain_store


	def preliminary_prune(self, domain_store, constraint_store, propagation_engine):	
		domains = domain_store['domains']
		constraitns = constraint_store

		prev_domains = domains
		while True:
			if not propagation_engine.feasibility_checking(domain_store,constraint_store):
				break
			domains = propagation_engine.pruning(domain_store,constraint_store)
			if (domains == prev_domains):
				break

			prev_domains = domains

		return domains



class SearchModule:
	def get_variable_order(self,domain_store):
		# Basic Variable Labeling
		for idx,domain in enumerate(domain_store['domains']):
			if len(domain) > 1:
				return range(idx,len(domain_store['domains']))

		return None

	def get_value_order(self,domain_store,var_idx):
		# Basic Variable->Value Labeling
		return domain_store['domains'][var_idx]


	def get_constraint(self,var,val):
		# Create new constraint
		left_variable = [var]
		left_const = [1]
		left_value = [0]

		right_variable = [0]
		right_const = [0]
		right_value = [val]


		left = [left_variable,
				left_const,
				left_value]

		right = [right_variable,
				right_const,
				right_value]

		constraint = Constraint("Equality",
								left,
								right)

		return constraint


class PropagationEngine:
	def __init__(self):
		self.propagators = {}

	def __str__(self):
		return ''.join([key for key in self.propagators])

	def feasibility_checking(self,domain_store,constraint_store):
		domains = domain_store['domains']
		constraints = constraint_store
		for constraint in constraints:
			# print("HEREV1",constraint.type)
			# print(self)
			if not self.propagators[constraint.type].feasibility_check(domains,constraint):
				return False

		return True

	def pruning(self,domain_store,constraint_store):
		new_domains = domain_store['domains']
		for constraint in constraint_store:
			new_domains = self.propagators[constraint.type].prune(new_domains,constraint)

		return new_domains

class DomainStoreWorker:
	def update(self,domain_store):
		updated_domain_store = domain_store
		for idx in range(len(domain_store['domains'])):
			if len(domain_store['domains'][idx]) == 1:
				updated_domain_store['vars'][idx] = domain_store['domains'][idx][0]
		return updated_domain_store

	def check_solution(self,domain_store):
		for var in domain_store['vars']:
			if var == None:
				return False
		
		return True



class Node:
	def __init__(self,domain_store,constraint_store):
		self.domain_store = domain_store
		self.constraint_store = constraint_store


class TraversalTree:
	def __init__(self,root):
		self.root = root
		self.state_queue = [root]
		self.solutions = []
		self.domain_worker = DomainStoreWorker()

	def init_modules(self,search_module,propagation_engine):
		self.search_module = search_module
		self.propagation_engine = propagation_engine

	
	def constraint_solution(self,current_node): 
		domain_store = deepcopy(current_node.domain_store)
		# print(domain_store)
		constraint_store = deepcopy(current_node.constraint_store)
		# print(constraint_store)

		variable_order = self.search_module.get_variable_order(domain_store)
		if variable_order is None:
			return

		for var_idx in variable_order:

			value_order = self.search_module.get_value_order(domain_store,var_idx)
			for value in value_order:
				# print(var_idx,value)
				constraint = self.search_module.get_constraint(var_idx,value)
				new_constraint_store = deepcopy(constraint_store)
				new_constraint_store.append(constraint)

				# print("HERE")
				if not self.propagation_engine.feasibility_checking(domain_store,new_constraint_store):
					continue
				
				new_domain_store = deepcopy(domain_store)
				prev_domains = domain_store['domains']
				while True:
					new_domains = self.propagation_engine.pruning(new_domain_store,new_constraint_store)
					if prev_domains == new_domains:
						break
					prev_domains = new_domains
					new_domain_store['domains'] = deepcopy(new_domains)

				new_domain_store = self.domain_worker.update(new_domain_store)
				if self.domain_worker.check_solution(new_domain_store):
					print("SOLUTION")
					self.solutions.append(new_domain_store['vars'])

				print(new_domain_store['domains'])
				# print(new_domain_store['vars'])
				# print("Constraint:",constraint)
				time.sleep(1)

				new_node = Node(new_domain_store,new_constraint_store)
				self.constraint_solution(new_node)

			return

# class Action(SearchModule,PropagationEngine,DomainStoreWorker):
# 	def __init__(self):
# 		SearchModule().__init__()
# 		PropagationEngine().__init__()
# 		DomainStoreWorker().__init__()

# 	def create_children(self,state):
# 		ordered_values = self.get_value_order(state)
# 		return ordered_values

# 	def get_next_state(self,value,state):
# 		return next_state

# N-Queens
class TemplateDomainStore:
	def __init__(self):
		N = 4
		self.DS = {}
		self.DS['vars'] = [None] * N
		self.DS['var_attrs'] = [[None]] * N
		self.DS['domains'] = [list(range(N))] * N
		self.var = 0


class State(TemplateDomainStore,):
	def __init__(self,domain_store,constraint_store,var):
		self.DS = domain_store
		self.var = var
		# self.CS = constraint_store


class Action(DomainStoreWorker):
	def __init__(self):
		self.total_action = 0
		N = 4
		self.template_domains = [
					[list(range(N))]*N,
					[[0],[1,2,3],[1,2,3],[1,2,3]],
					[[0],[1],[1,2,3],[1,2,3]],
					[[0],[2],[1,3],[1,3]],
					[[0],[2],[1],[1,3]],
					[[0],[2],[3],[1,3]],
					[[0],[3],[1,2],[1,2]],
					[[0],[3],[1],[1,2]],
					[[0],[3],[1],[1]],
					[[0],[3],[1],[2]],
					[[0],[3],[2],[1,2]],
					[[1],[0,2,3],[0,2,3],[0,2,3]],
					[[1],[0],[0,2,3],[0,2,3]],
					[[1],[2],[0,2,3],[0,2,3]],
					[[1],[3],[0,2],[0,2]],
					[[1],[3],[0],[2]],
					]
		self.template_var = [0,0,0,1,1,2,2,1,2,3,0,1,1,1,2]

		self.init_state = {}



	def create_children(self,state):
		# Template: N-Queens
		for domain in state.DS['domains']:
			# print(domain)
			if len(domain) > 1: 
				return domain

		return None

	def get_next_state(self,state,value):
		# Pruning
		self.total_action += 1
		if self.total_action < len(self.template_domains):
			new_domains = self.template_domains[self.total_action]
		else:
			return None
		new_DS = deepcopy(state.DS)
		new_DS['domains'] = deepcopy(new_domains)
		new_DS = self.update(new_DS)

		# Feasibility Checking
		for i,var_i in enumerate(new_DS['vars']):
			if var_i is None:
				continue

			for j,var_j in enumerate(new_DS['vars']):
				if var_j is None:
					continue

				if i >= j:
					continue

				if var_i == var_j: 
					print("Not Feasible1")
					print(state.var,new_DS)
					print("=====================")
					return None
				elif var_i == var_j + (j-i): 
					print("Not Feasible2")
					print(state.var,new_DS)
					print("=====================")
					return None
				elif var_i == var_j - (j-i):
					print("Not Feasible3")
					print(state.var,new_DS)
					print("=====================")
					return None

		
		next_state = deepcopy(state)
		next_state.DS = new_DS
		next_state.var = deepcopy(state.var + 1)

		print(state.var,state.DS)
		print(next_state.var,next_state.DS)
		print("------------------")

		return next_state



class Tree(Action):
	def __init__(self):
		super().__init__()
		self.root = TemplateDomainStore()

	def traverse(self,state):
		if state is None:
			return

		values = self.create_children(state)
		if values is None:
			return

		for value in values:
			next_state = self.get_next_state(state,value)
			time.sleep(5)
			self.traverse(next_state)


		print("Finished!", state.var)
		print(state.DS)
		print("++++++++++++++++++++++")
		time.sleep(5)

		return None






if __name__ == '__main__':
	# Prototyping the Tree
	tree = Tree()

	tree.traverse(tree.root)

