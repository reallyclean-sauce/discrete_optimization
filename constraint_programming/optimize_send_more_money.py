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

from copy import deepcopy
from collections import namedtuple
import time

Item = namedtuple("Item", ['index', 'letter', 'value', 'search_space'])

class SendMoreMoney:
    def __init__(self,word1,word2,optimize_word):
        if len(word1) != len(word2):
            raise Exception("NEED TO BE THE SAME LENGTH")
        elif len(optimize_word) != len(word2)+1:
            raise Exception("OVERALL WORD MUST BE SIZE OF WORD + 1")

        self.word1 = word1
        self.word2 = word2
        self.optimize_word = optimize_word
        num_carries = len(word2)



        self.first_letters = set([word1[0],word2[0],optimize_word[0]])

        word1 = set(word1)
        word2 = set(word2)
        optimize_word = set(optimize_word)

        self.all_letters = word1 | word2 | optimize_word

        self.items = []
        iterator = 0
        for letter in self.all_letters:
            letter = letter
            value = None
            search_space = set(range(10)) 
            self.items.append(Item(iterator,letter,value,search_space))

            iterator += 1

        for i in range(num_carries):
            letter = f'{i+1}'
            value = None
            search_space = set(range(2))
            self.items.append(Item(iterator,letter,value,search_space))            

            iterator += 1


    def displaySearchSpace(self):
        print("Printing the Search space")
        print("==========================")
        for item in self.items:
            print(f"{item.letter}: {item.search_space}")


    def prune_inequality(self):
        for item in self.items:
            if item.value is None:
                continue 

            # Skip if Carry
            if item.letter in [str(x+1) for x in range(4)]:
                continue

            # Remove from search space if value for letter is assigned
            for search_item in self.items:
                if search_item.letter == item.letter:
                    continue

                if search_item.letter in [str(x+1) for x in range(4)]:
                    continue

                search_item.search_space.discard(item.value)
                new_space = search_item.search_space

                self.items[search_item.index]._replace(search_space=new_space)

        for item in self.items:
            if item.letter in self.first_letters:
                item.search_space.discard(0)
                new_space = item.search_space
                self.items[item.index]._replace(search_space=new_space)

    def get_range(self,letters,right):
        minimum = 0
        maximum = 0

        for item in self.items:
            if not item.letter in letters:
                continue

            if right and (ord(item.letter) in range(ord('0'),ord('9')+1)):
                minimum = minimum + min(item.search_space) * 10
                maximum = maximum + max(item.search_space) * 10
            else:
                # print(self.search_space[variable],variable)
                minimum = minimum + min(item.search_space)
                maximum = maximum + max(item.search_space)



        return set(range(minimum,maximum+1))

    def update_assign(self):
        for item in self.items:
            if len(item.search_space) != 1:
                continue

            value =  [x for x in item.search_space][0]

            self.items[item.index] = self.items[item.index]._replace(value=value)

            self.prune_inequality()

    def prune_equation(self,left_vars,right_vars):
        left_range = self.get_range(left_vars,0)
        right_range = self.get_range(right_vars,1)
        intersection = left_range & right_range


        total_sum = 0
        prune_left = []
        prune_right = []
        for item in self.items:
            if not item.letter in left_vars:
                continue

            if item.value is None:
                prune_left.append(item.letter)
            else:
                total_sum += item.value

        # Prune the left side of the equation
        new_intersection = [x-total_sum for x in intersection]

        for prune_var in prune_left:
            dummy_vars = deepcopy(prune_left)
            dummy_vars.remove(prune_var)
            val_range = self.get_range(dummy_vars,0)

            minimum = min(new_intersection) - max(val_range)
            maximum = max(new_intersection) - min(val_range)
            dummy_intersection = set(range(minimum,maximum+1))
            new_item = [item for item in send_more_money.items if item.letter == prune_var][0]
            new_search_space = new_item.search_space & dummy_intersection

            self.items[new_item.index] = self.items[new_item.index]._replace(search_space=new_search_space)

        self.update_assign()

        # Prune the right side of the equation
        total_sum = 0
        for item in self.items:
            if not item.letter in right_vars:
                continue

            if item.value is None:
                prune_right.append(item.letter)
            else:
                if item.letter in [str(x+1) for x in range(4)]:
                    total_sum += item.value * 10
                else:
                    total_sum += item.value

        

        new_intersection = [x-total_sum for x in intersection]

        for prune_var in prune_right:
            dummy_vars = deepcopy(prune_right)
            dummy_vars.remove(prune_var)
            val_range = self.get_range(dummy_vars,1)

            minimum = min(new_intersection) - max(val_range)
            maximum = max(new_intersection) - min(val_range)
            if prune_var in [str(x+1) for x in range(4)]:
                dummy_intersection = set(range(minimum//10,(maximum)//10+1))
            else:
                dummy_intersection = set(range(minimum,maximum+1))
            new_item = [item for item in send_more_money.items if item.letter == prune_var][0]
            new_search_space = new_item.search_space & dummy_intersection
            self.items[new_item.index] = self.items[new_item.index]._replace(search_space=new_search_space)

    def get_total_search_space(self):
        count = 0
        for item in self.items:
            count += len(item.search_space)

        return count

    def prune(self,items):
        delayed_count = 0
        self.items = items
        while True:
            total_count = 0
            
            self.prune_inequality()

            for i in range(len(self.optimize_word)):
                if i == 0:
                    left_vars = [f'{len(self.optimize_word)-1}']
                    right_vars = [f'{self.optimize_word[i]}']

                elif i == len(self.optimize_word)-1:
                    left_vars = [f'{self.word1[i-1]}',f'{self.word2[i-1]}']
                    right_vars = [f'{self.optimize_word[i]}',f'{len(self.optimize_word)-i}']

                else:
                    left_vars = [f'{len(self.optimize_word)-i-1}',f'{self.word1[i-1]}',f'{self.word2[i-1]}']
                    right_vars = [f'{self.optimize_word[i]}',f'{len(self.optimize_word)-i}']

                # print("LEFTVARS:",left_vars)
                # print("RIGHTVARS:",right_vars)
                self.prune_equation(left_vars,right_vars)
                total_count += self.get_total_search_space()

                self.update_assign()

            if total_count == delayed_count:
                break

            delayed_count = total_count

        return self.items




class Node:
    def __init__(self,items,level):
        # i-th index represents the index for the i-th item
        # Each item has ['index', 'letter', 'value', 'search_space'])
        self.items = deepcopy(items)
        self.level = level
        self.children = [None] * len(items[level].search_space)

class MoneyTree:
    def __init__(self,items,propagation_engine):
        self.items = deepcopy(items)
        self.root = Node(items,0)
        self.engine = propagation_engine
        self.solutions = []

    def check_and_get_money(self,items):
        send = more = money = 0
        for i in range(len(self.engine.optimize_word)):
            print(i,len(self.engine.optimize_word)-i-1)
            if i == 0:
                money += [item.value for item in items if item.letter == self.engine.optimize_word[i]][0] * 10**(len(self.engine.optimize_word)-1-i)

            else:
                money += [item.value for item in items if item.letter == self.engine.optimize_word[i]][0] * 10**(len(self.engine.optimize_word)-1-i)
                send += [item.value for item in items if item.letter == self.engine.word1[i-1]][0] * 10**(len(self.engine.optimize_word)-1-i)
                more += [item.value for item in items if item.letter == self.engine.word2[i-1]][0] * 10**(len(self.engine.optimize_word)-1-i)

        if money == send+more:
            print(send,more)
            print(money)
            self.solutions.append(money)
        else:
            print(send,more)
            print(money)
            raise Exception("Error! Solution is not correct")

    def feasibility_check(self,items):
        search_space = set([])
        for item in items:
            if not item.letter in [str(x+1) for x in range(4)]:
                search_space = search_space | item.search_space

            elif item.letter in [str(x+1) for x in range(4)] and len(item.search_space) == 0:
                print("NONFEASIBLE_V1")
                print(len(item.search_space))
                print(item.letter)
                return False

        if len(search_space) < len(self.engine.all_letters):
            print("NONFEASIBLE_V2")
            print(search_space)
            for item in items:
                print(item.letter,item.search_space)
            return False

        return True


    def depth_first_search(self,start):
        for i in range(len(start.items[start.level].search_space)):
            next_level = start.level + 1

            # Branching
            new_value = [val for val in start.items[start.level].search_space][i]
            new_item = deepcopy(start.items[start.level])
            new_item = new_item._replace(value=new_value)
            new_item = new_item._replace(search_space=set([new_value]))

            new_items = deepcopy(start.items)
            new_items[start.level] = new_item

            # Pruning Search Space
            try:
                new_items = self.engine.prune(new_items)
            except:
                continue

            if not self.feasibility_check(new_items):
                continue

            if next_level == len(new_items):
                self.check_and_get_money(new_items)
                return
            
            child_node = Node(new_items,next_level)

            start.children[i] = child_node
            self.depth_first_search(start.children[i])

        
        return self.solutions

if __name__ == '__main__':
    word1 = "SEND"
    word2 = "MORE"
    optimize_word = "MONEY"

    send_more_money = SendMoreMoney(word1,word2,optimize_word)

    items = send_more_money.prune(send_more_money.items)

    money_tree = MoneyTree(send_more_money.items, send_more_money)

    start_time = time.time()
    solutions = money_tree.depth_first_search(money_tree.root)
    runtime = time.time() - start_time
    print(f"Total runtime: {runtime}")