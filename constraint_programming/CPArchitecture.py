# Constraint Programming Modules
# These are the required classes to create a Constraint Programming solution
from abc import ABCMeta, abstractmethod
import json
from collections import namedtuple
from ConstraintPropagators import NotEqualPropagator, EqualityPropagator
import SearchUtils
import time
from copy import deepcopy
from utils import domain_printer
import sys
import numpy as np

def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)

Constraint = namedtuple("Constraint", ['type', 'left', 'right'])

class Reader:
    @abstractmethod
    def format(self,input_data): pass


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
    def propagate_constraints(self,propagators,state):
        # Output:
        validity = True
        new_domains = deepcopy(state.domains)
        constraints = state.CS
        for constraint in constraints:
            if not propagators[constraint.type].feasibility_check(new_domains,constraint):
                validity = False
                break
            new_domains = propagators[constraint.type].prune(new_domains,constraint)

        return validity,new_domains

    # def feasibility_checking(self,propagators,state):

    # def pruning(self,propagators,state):
    #     new_domains = deepcopy(state.domains)
    #     for constraint in state.CS:
            

    #     return new_domains

class DomainStoreWorker:
    def get_updated_vars(self,state):
        decision_vars = deepcopy(state.vars)
        for idx in range(len(state.domains)):
            if len(state.domains[idx]) == 1:
                decision_vars[idx] = state.domains[idx][0]
        return decision_vars


    def check_solution(self,state):
        for domain in state.domains:
            if len(domain) > 1:
                return False

        # if state.state_var == len(state.vars)-1:
        #     print(state.domains)
        #     return True     
        return True



class ConstraintStoreWorker:
    def add_constraint(self,state,constraint):
        state.CS.append(constraint)
    def equality_constraint(self,var,val):
        constraint_type = "Equality"
        # Lefthand Eqn
        left_variable = [var]
        left_const = [1]
        left_value = [0]
        left = [left_variable,
                left_const,
                left_value]
        # Righthand Eqn
        right_variable = [0]
        right_const = [0]
        right_value = [val]
        right = [right_variable,
                right_const,
                right_value]

        constraint = Constraint(constraint_type,
                                left,
                                right)

        return constraint

    

class SearchModule:
    def value_ordering(self,state):
        state.domains[state.state_var].sort(reverse=True)
        return state.domains[state.state_var]
    def get_next_variable(self,state):
        minimum_size = 1000
        min_idx = state.state_var + 1
        for idx,domain in enumerate(state.domains):
            if (len(domain) < minimum_size) and (len(domain) != 1):
                minimum_size = len(domain)
                min_idx = idx

        return min_idx

class State:
    def __init__(self,level,DS,CS):     
        self.state_var = level

        self.vars = DS['vars']
        self.var_attrs = DS['var_attrs']
        self.domains = DS['domains']

        self.CS = CS


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
        
class Propagators:
    def __init__(self):
        self._propagators = {}

    def add_propagator(self,propagator):
        self._propagator[propagator.constraint_type] = propagator

class Solver:
    def __init__(self,propagators):
        self.propagators = propagators
        self.solutions = []
        self.variables_search = []

    def preliminary_prune(self, root):
        new_state = deepcopy(root)
        new_domains = new_state.domains
        prev_domains = new_domains
        domain_printer(new_state.domains)
        print("--------------------------")
        i = 0
        while True:
            # print(i)
            if not i % 100:
                print("Pruning still on process...")
            elif i == 5001:
                i = 0

            valid,new_domains = PropagationEngine().propagate_constraints(self.propagators,new_state)
            if not valid:
                return self.solutions

            domain_printer(new_domains)
            print("--------------------------")
            new_state.domains = new_domains
            if (new_domains == prev_domains):
                break   

            i += 1
            prev_domains = new_domains

        return new_state

    def solve(self,state):
        if state is None:
            return self.solutions
        elif state.state_var == len(state.vars):
            return self.solutions

        # if not state.state_var in self.variables_search:
        #     self.variables_search.append(state.state_var)

        # Get value range for a variable
        # Sort the values accordingly
        value_range = SearchModule().value_ordering(state)
        # print("Value_range",state.state_var,value_range)

        # Generate child nodes
        # Sets which value the variable has to take
        for i in value_range:
            # if len(self.solutions) > 10:
            #     return self.solutions


            next_state = deepcopy(state)

            # ConstraintStoreWorker
            # Add EqualityConstraint to constraint Store
            constraint = ConstraintStoreWorker().equality_constraint(next_state.state_var,i)
            next_state.CS.append(constraint)

            # Propagation Engine
            prev_domains = deepcopy(next_state.domains)
            new_domains = prev_domains
            while True:
                # Propagate constraints
                valid,new_domains = PropagationEngine().propagate_constraints(self.propagators,next_state)
                if not valid:
                    return None

                next_state.domains = new_domains
                if prev_domains == new_domains:
                    break
                prev_domains = new_domains
            
            # print(next_state.domains)
            # print(constraint)
            # print("------------------------")

            # DomainStoreWorker
            # Update the Domain Store
            next_state.vars = DomainStoreWorker().get_updated_vars(next_state)

            # SearchModule
            # Determines which Decision Variable to process
            next_state.state_var = SearchModule().get_next_variable(next_state)

            if DomainStoreWorker().check_solution(state):
                print("SOLUTION!!",state.vars)
                # print(self.variables_search)
                self.solutions.append(state.vars)
                return self.solutions

            self.solve(next_state)

        
        return self.solutions






if __name__ == '__main__':
    # Prototyping the Tree
    tree = Tree()

    tree.traverse(tree.root)

