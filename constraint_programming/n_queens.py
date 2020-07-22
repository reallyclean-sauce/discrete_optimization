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
from ModelFrameworkCP import NQueens

# Global Var
N = 4

# Get Problem Framework
n_queens_framework = NQueens(N)

# Domain Store Initialization
domain_store = n_queens_framework.get_domain_store()

# Constraint Store Initialization
n_queens_model = n_queens_framework.get_model()
constraint_store = n_queens_model.get_constraints() 

# Initialize propagators
initializer = Initializer()
propagators = initializer.init_propagators(constraint_store) 

# Initialize solvers
root = State(0,domain_store,constraint_store)
queen_tree = Solver(propagators)

# Start solving
state_time = time.time()
queen_tree.solve(root)
solutions = queen_tree.solutions
runtime = time.time() - state_time

# Identify Solutions
if solutions != []:
    print("SOLUTIONSS!!")
    print(solutions)
else:
    print("No solution found")
print(f"Total time taken: {runtime}s")