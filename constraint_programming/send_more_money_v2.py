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

import time
from CPArchitecture import Initializer
from CPArchitecture import Solver, State
from ModelFrameworkCP import SendMoreMoney

# Global Var
word1 = "SEND"
word2 = "MORE"
word3 = "MONEY"

# Get Problem Framework
framework = SendMoreMoney(word1,word2,word3)

# Domain Store Initialization
domain_store = framework.get_domain_store()

# Constraint Store Initialization
model = framework.get_model()
constraint_store = model.get_constraints() 
# for constraint in constraint_store:
#   print(constraint)

# Initialize propagators
initializer = Initializer()
propagators = initializer.init_propagators(constraint_store) 

# Initialize solvers
root = State(0,domain_store,constraint_store)
ssm_solver = Solver(propagators)
new_root = ssm_solver.preliminary_prune(root)

# Start solving
state_time = time.time()
solutions = ssm_solver.solve(new_root)
runtime = time.time() - state_time

# Identify Solutions
if solutions != []:
    print("SOLUTION HERE")
    framework.print_solution(solutions)
else:
    print("No solution found")
print(f"Total time taken: {runtime}s")