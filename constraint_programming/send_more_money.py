"""
Problem: Send More Money

Objective: Find the Maximum value for Money

Constraint: SEND + MORE = MONEY (Model Used)
"""

from copy import deepcopy
import time

# class Node:
#     def __init__(self,word1,word2,optimize_word):
#         all_letters = word1 | word2 | optimize_word

#         # Decision Variable
#         self.val_assign = {}
#         for letter in all_letters:
#           self.val_assign[letter] = None

#       # For Carry Decision Variable
#       for i in range(4):
#           self.val_assign[i+1] = None

#         # Search Space
#         self.search_space = {}
#         for letter in all_letters:
#           self.search_space[letter] = set(range(10))
#       for i in range(4):
#           self.val_assign[i+1] = set([0,1])

#         self.children = [None] * N

class SendMoreMoney:
    def __init__(self,word1,word2,optimize_word):
        all_letters = word1 | word2 | optimize_word

        # Decision Variable
        self.val_assign = {}
        for letter in all_letters:
            self.val_assign[letter] = None

        # For Carry Decision Variable
        for i in range(4):
            self.val_assign[str(i+1)] = None

        # Search Space
        self.search_space = {}
        for letter in all_letters:
            self.search_space[letter] = set(range(10))
        for i in range(4):
            self.search_space[str(i+1)] = set([0,1])


    def displaySearchSpace(self):
        print("Printing the Search space")
        print("==========================")
        for var in self.search_space:
            print(f"{var}: {self.search_space[var]}")


    def prune_inequality(self):
        for letter in self.val_assign:
            assigned_val = self.val_assign[letter]
            if self.val_assign[letter] is None:
                continue 

            # Skip if Carry
            if letter in [str(x+1) for x in range(4)]:
                continue

            # Remove from search space if value for letter is assigned
            for search_letter in self.search_space:
                if search_letter == letter:
                    continue

                if search_letter in [str(x+1) for x in range(4)]:
                    continue

                self.search_space[search_letter].discard(assigned_val)

        self.search_space['M'].discard(0)
        self.search_space['S'].discard(0)

    def get_range(self,args,right):
        minimum = 0
        maximum = 0
        for variable in args:
            if right and (ord(variable) in range(ord('0'),ord('9')+1)):
                minimum = minimum + min(self.search_space[variable]) * 10
                maximum = maximum + max(self.search_space[variable]) * 10
            else:
                # print(self.search_space[variable],variable)
                minimum = minimum + min(self.search_space[variable])
                maximum = maximum + max(self.search_space[variable])



        return set(range(minimum,maximum+1))

    def update_assign(self):
        for var in self.val_assign:
            if len(self.search_space[var]) != 1:
                continue

            self.val_assign[var] =  [x for x in self.search_space[var]][0]

            self.prune_inequality()

    def prune_equation(self,left_vars,right_vars):
        left_range = self.get_range(left_vars,0)
        right_range = self.get_range(right_vars,1)
        intersection = left_range & right_range


        total_sum = 0
        prune_left = []
        prune_right = []
        for var in left_vars:
            if self.val_assign[var] is None:
                prune_left.append(var)
            else:
                total_sum += self.val_assign[var]

        # Prune the left side of the equation
        new_intersection = [x-total_sum for x in intersection]

        for prune_var in prune_left:
            dummy_vars = deepcopy(prune_left)
            dummy_vars.remove(prune_var)
            val_range = self.get_range(dummy_vars,0)
            # print("========================")
            # print("DUMMY VARS:",dummy_vars)
            # print("RANGE:",val_range)
            # print("VAR", prune_var, total_sum)
            # print("OLD_INTERSECTION:",new_intersection)

            minimum = min(new_intersection) - max(val_range)
            maximum = max(new_intersection) - min(val_range)
            dummy_intersection = set(range(minimum,maximum+1))
            # print("INTERSECTION:",dummy_intersection)
            self.search_space[prune_var] = self.search_space[prune_var] & dummy_intersection
            # print(f"PRUNING {prune_var}: {self.search_space[prune_var]}")
            # input("NEW INTERSECTION")


        self.update_assign()
        # self.displaySearchSpace()
        # input("Within prune_eqn, Waiting...")

        # Prune the left side of the equation
        total_sum = 0
        for var in right_vars:
            if self.val_assign[var] is None:
                prune_right.append(var)
            else:
                if var in [str(x+1) for x in range(4)]:
                    total_sum += self.val_assign[var] * 10
                else:
                    total_sum += self.val_assign[var]

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
            self.search_space[prune_var] = self.search_space[prune_var] & dummy_intersection

    def get_total_search_space(self):
        count = 0
        for var in self.search_space:
            # print(count)
            count += len(self.search_space[var])

        return count

    def prune(self):
        delayed_count = 0
        while True:
            total_count = 0
            
            self.prune_inequality()

            # C4 = Val[M]
            left_vars = ['4']
            right_vars = ['M']
            self.prune_equation(left_vars,right_vars)
            total_count += self.get_total_search_space()

            self.update_assign()

            # C3 + val[S] + val[M] = val[O] + 10*C4
            left_vars = ['3','S','M']
            right_vars = ['O','4']
            self.prune_equation(left_vars,right_vars)
            total_count += self.get_total_search_space()

            self.update_assign()

            # C2 + val[E] + val[O] = val[N] + 10*C3
            left_vars = ['2','E','O']
            right_vars = ['N','3']
            self.prune_equation(left_vars,right_vars)
            total_count += self.get_total_search_space()

            self.update_assign()

            # C1 + val[N] + val[R] = val[E] + 10*C2
            left_vars = ['1','N','R']
            right_vars = ['E','2']
            self.prune_equation(left_vars,right_vars)
            total_count += self.get_total_search_space()

            self.update_assign()

            # C1 + val[N] + val[R] = val[E] + 10*C2
            left_vars = ['D','E']
            right_vars = ['Y','1']
            self.prune_equation(left_vars,right_vars)

            self.update_assign()

            self.displaySearchSpace()
            total_count += self.get_total_search_space()
            print(total_count,delayed_count)
            input("Waiting...")

            if total_count == delayed_count:
                break

            delayed_count = total_count


    def propagate(self,start,level):
        self.prune()


                






if __name__ == '__main__':
    word1 = set("SEND")
    word2 = set("MORE")
    optimize_word = set("MONEY")

    send_more_money = SendMoreMoney(word1,word2,optimize_word)

    send_more_money.prune()

    send_more_money.displaySearchSpace()
