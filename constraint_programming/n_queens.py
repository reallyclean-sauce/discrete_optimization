"""
Problem: 8 Queens in 8x8 chessboard

Problem Definition: 
You are given N queens. You must place each queen in the chessboard
in such a way that none of the queens can attack each other.

Goal: Assign a row for each queen

Model: Each queen has a column assigned: i
Decision Variable: Which row to place the queen: row[i]

Lecture:
Based on the lecture, this problem can be solve using Branch and Prune
"""

# Knapsack
# Find the items that will maximize the value
# Given a constraint on weight
# Branch on the decision variables (taken)
# Bound using the estimated values

# Constraint Programming:
# Find any solution
# That satisfies the constraint
# Branch on the decision variables (chosen value within the search space)
# Prune based on the decision variables


from copy import deepcopy
import time

from CPArchitecture import Initializer
# from CPArchitecture import PropagationEngine, SearchModule
from CPArchitecture import ConstraintModel, Constraint


class Propagators:
    def __init__(self):
        self._propagators = {}

    def add(self,propagator):
        self._propagator[propagator.constraint_type] = propagator

class DomainStore:
    def __init__(self):
        self.vars = []
        self.var_attrs = []
        self.domains = []

class DomainStoreWorker:
    def get_updated_vars(self,state):
        decision_vars = deepcopy(state.vars)
        for idx in range(len(state.domains)):
            if len(state.domains[idx]) == 1:
                decision_vars[idx] = state.domains[idx][0]
        return decision_vars


    def check_solution(self,state):
        for var in state.vars:
            if var == None:
                return False        
        return True


class PropagationEngine:
    def feasibility_checking(self,propagators,state):
        domains = state.domains
        constraints = state.CS
        for constraint in constraints:
            if not propagators[constraint.type].feasibility_check(domains,constraint):
                return False
        return True

    def pruning(self,propagators,state):
        new_domains = deepcopy(state.domains)
        for constraint in state.CS:
            new_domains = propagators[constraint.type].prune(new_domains,constraint)

        return new_domains


class ConstraintStoreWorker:
    def add_constraint(self,state,constraint):
        state.CS.append(constraint)

    def equality_constraint(self,var,val):
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

    

class SearchModule:
    def value_ordering(self,state):
        if not state.state_var in range(len(state.domains)):
            print(state.domains)
            print(state.vars)
            print(len(state.domains),state.state_var)
        return state.domains[state.state_var]
    def get_next_variable(self,state):
        return state.state_var + 1
    



class State:
    def __init__(self,level,DS,CS):     
        self.state_var = level

        attrs = [[None]]*N
        self.vars = DS['vars']
        self.var_attrs = DS['var_attrs']
        self.domains = DS['domains']

        self.CS = CS

class Solver:
    def __init__(self,propagators):
        global N
        self.N = N
        self.propagators = propagators
        self.solutions = []

    def solve(self,state):
        if state is None:
            return

        # Get value range for a variable
        # Sort the values accordingly
        value_range = SearchModule().value_ordering(state)

        # Generate child nodes
        # Sets which value the variable has to take
        for i in value_range:
            next_state = deepcopy(state)

            # ConstraintStoreWorker
            # Add EqualityConstraint to constraint Store
            constraint = ConstraintStoreWorker().equality_constraint(next_state.state_var,i)
            next_state.CS.append(constraint)

            # Propagation Engine
            # Feasibility Checking
            if not PropagationEngine().feasibility_checking(self.propagators,next_state): 
                return None
            # Pruning Search Space
            prev_domains = next_state.domains
            while True:
                new_domains = PropagationEngine().pruning(self.propagators,next_state)
                next_state.domains = new_domains
                if prev_domains == new_domains:
                    break
                prev_domains = new_domains

            # DomainStoreWorker
            # Update the Domain Store
            next_state.vars = DomainStoreWorker().get_updated_vars(next_state)

            # SearchModule
            # Determines which Decision Variable to process
            next_state.state_var = SearchModule().get_next_variable(next_state)

            if DomainStoreWorker().check_solution(state):
                self.solutions.append(state.vars)
                return None

            self.solve(next_state)

        
        return self.solutions


# Global Var
N = 8

# V2
# Domain Store Initialization
total_vars = [None] * N
domains = [set(range(N))]*N
attrs = [[None]]*N

domain_store = {'vars': total_vars,
                'domains': domains,
                'var_attrs': attrs}

# Constraint Store Initialization
model = ConstraintModel()
constraint_type = 'NotEqual'
for i in range(N):
    for j in range(N):
        if i >= j:
            continue

        left_var = [i]
        left_const = [1]
        left_val = [0]
        left = [left_var,left_const,left_val]

        right_var = [j]
        right_const = [1]
        right_val = [0]
        right = [right_var,right_const,right_val]

        constraint = Constraint(constraint_type,left,right)
        model.add(constraint)


        left_var = [i]
        left_const = [1]
        left_val = [0]
        left = [left_var,left_const,left_val]

        right_var = [j]
        right_const = [1]
        right_val = [j-i]
        right = [right_var,right_const,right_val]

        constraint = Constraint(constraint_type,left,right)
        model.add(constraint)

        
        left_var = [i]
        left_const = [1]
        left_val = [0]
        left = [left_var,left_const,left_val]

        right_var = [j]
        right_const = [1]
        right_val = [i-j]
        right = [right_var,right_const,right_val]

        constraint = Constraint(constraint_type,left,right)
        model.add(constraint)

# constraint = ConstraintStoreWorker().equality_constraint(8,1)
# model.add(constraint)
# constraint = ConstraintStoreWorker().equality_constraint(0,5)
# model.add(constraint)

initializer = Initializer()
constraint_store = model.get_constraints()
propagators = initializer.init_propagators(constraint_store)

#V2
queen_tree = Solver(propagators)

root = State(0,domain_store,constraint_store)
state_time = time.time()
solutions = queen_tree.solve(root)
runtime = time.time() - state_time

if solutions != []:
    print(solutions)
else:
    print("No solution found")
print(f"Total time taken: {runtime}s")