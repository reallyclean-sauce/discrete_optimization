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

class Node:
    def __init__(self,row_queens,N):
        # i-th index represents the i-th Queen
        # value in i-th index represents the chosen row
        self.row_queens =  row_queens

        # Search Space
        # i-th index represents the search space for the i-th Queen
        self.search_space = set(range(N))

        self.children = [None] * N

class Queen_N_Tree:
    def __init__(self,row_queens,N):
        self.N = N
        self.root = Node(row_queens,N)
        self.solutions = []

    def depth_first_search(self,start,level):

        for i in range(self.N):
            if not i in start.search_space:
                # print(start.search_space)
                continue

            next_level = level + 1

            # Branching
            new_row_queens = deepcopy(start.row_queens)
            new_row_queens[level] = i

            # Check if solution
            if next_level == self.N:
                self.solutions.append(deepcopy(new_row_queens))
                return True
            
            child_node = Node(new_row_queens,self.N)

            # Pruning Search Space
            next_level_search = set(range(self.N))

            for j in range(next_level):
                # Prune Same Row
                next_level_search.discard(new_row_queens[j])

                # Prune Lower Diagonal
                next_level_search.discard(new_row_queens[j] + (next_level - j))

                # Prune Upper Diagonal
                next_level_search.discard(new_row_queens[j] - (next_level - j))

            # Feasibility Checking
            if len(next_level_search) == 0:
                continue

            child_node.search_space = next_level_search
            

            start.children[i] = child_node
            self.depth_first_search(start.children[i],level+1)

        
        return self.solutions

if __name__ == '__main__':
    N = 10

    row_queens = [None] * N


    queen_tree = Queen_N_Tree(row_queens,N)

    start_time = time.time()
    solutions = queen_tree.depth_first_search(queen_tree.root,0)
    runtime = time.time() - start_time

    print(solutions)
    print(f"Total time taken: {runtime}s")