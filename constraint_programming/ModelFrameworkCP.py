"""
Containe the Basic Frameworks for solving
Discrete Optimization Problems
Using Constraint Programming
"""
from CPArchitecture import ConstraintModel,Constraint


class NQueens:
    def __init__(self,N):
        self.N = N
        # Constraint Store Initialization
        self.model = ConstraintModel()

        # Alldifferent
        left = list(range(N))
        constraint_type = 'AllDifferent'
        constraint = Constraint(constraint_type,left,[])
        self.model.add(constraint)

        constraint_type = 'NotEqual'
        for i in range(N):
            for j in range(N):
                if i >= j:
                    continue

                # left_var = [i]
                # left_const = [1]
                # left_val = [0]
                # left = [left_var,left_const,left_val]

                # right_var = [j]
                # right_const = [1]
                # right_val = [0]
                # right = [right_var,right_const,right_val]

                # constraint = Constraint(constraint_type,left,right)
                # self.model.add(constraint)


                left_var = [i]
                left_const = [1]
                left_val = [0]
                left = [left_var,left_const,left_val]

                right_var = [j]
                right_const = [1]
                right_val = [j-i]
                right = [right_var,right_const,right_val]

                constraint = Constraint(constraint_type,left,right)
                self.model.add(constraint)

                
                left_var = [i]
                left_const = [1]
                left_val = [0]
                left = [left_var,left_const,left_val]

                right_var = [j]
                right_const = [1]
                right_val = [i-j]
                right = [right_var,right_const,right_val]

                constraint = Constraint(constraint_type,left,right)
                self.model.add(constraint)
        
        print("NQueens constraint model created.")

    def get_domain_store(self):
        # Domain Store Initialization
        total_vars = [None] * self.N
        domains = [list(range(self.N))]*self.N
        attrs = [[None]]*self.N
        domain_store = {'vars': total_vars,
                        'domains': domains,
                        'var_attrs': attrs}
        return domain_store

    def get_model(self):
        return self.model



class SendMoreMoney:
    def __init__(self,word_addend1,word_addend2,word_sum):
        self.word1 = word_addend1
        self.word2 = word_addend2
        self.word3 = word_sum

        if len(word_addend1) != len(word_addend2):
            raise Exception("NEED TO BE THE SAME LENGTH")
        elif len(word_sum) != len(word_addend1)+1:
            raise Exception("OVERALL WORD MUST BE SIZE OF WORD + 1")

        all_letters = set(word_addend1) | set(word_addend2) | set(word_sum)
        num_carries = len(word_addend1)
        self.identifiers = all_letters

        # Domain Store
        # Decision Variable
        variables = []
        for letter in all_letters:
            variables.append(None)
        # For Carry Decision Variable
        for i in range(num_carries):
            variables.append(None)

        # Domains
        domains = []    
        for letter_idx in range(len(all_letters)):
            domains.append(list(range(10)))
        for i in range(num_carries):
            domains.append(list([0,1]))

        print(len(domains))

        self.DS = {'vars': variables,
                    'var_attrs': [[None]]*len(variables),
                    'domains': domains}
        
        # Model Constraint
        # Equality
        letterlist = list(all_letters)
        self.model = ConstraintModel()
        for i in range(len(word_sum)):
            if i == 0:
                # Lefthand Eqn
                left_vars = [len(letterlist)+i] # C4
                left_const = [1]
                left_val = [0]
                left = [left_vars,left_const,left_val]
                # Righthand Eqn
                right_vars = [letterlist.index(word_sum[i])] # M
                right_const = [1]
                right_val = [0]
                right = [right_vars,right_const,right_val]

                constraint = Constraint("Equality",left,right)
                self.model.add(constraint)

            elif i == len(word_sum)-1:
                # Lefthand Eqn
                left_vars = [letterlist.index(word_addend1[i-1]),letterlist.index(word_addend2[i-1])]  # D + E
                left_const = [1,1]
                left_val = [0]
                left = [left_vars,left_const,left_val]
                # Righthand Eqn
                right_vars = [letterlist.index(word_sum[i]),len(letterlist)+i-1] # Y + C1
                right_const = [1,10]
                right_val = [0]
                right = [right_vars,right_const,right_val]

                constraint = Constraint("Equality",left,right)
                self.model.add(constraint)

            else:
                # Lefthand Eqn
                left_vars = [len(letterlist)+i,letterlist.index(word_addend1[i-1]),letterlist.index(word_addend2[i-1])] # C1 + N + R
                left_const = [1,1,1]
                left_val = [0]
                left = [left_vars,left_const,left_val]
                # Righthand Eqn
                right_vars = [letterlist.index(word_sum[i]),len(letterlist)+i-1] # E + 10*C2
                right_const = [1,10]
                right_val = [0]
                right = [right_vars,right_const,right_val]

                constraint = Constraint("Equality",left,right)
                self.model.add(constraint)

        # Alldifferent: Basic implementation
        constraint_type = 'NotEqual'
        for i in range(len(all_letters)):
            for j in range(len(all_letters)):
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
                self.model.add(constraint)

        left_var = [letterlist.index(word_addend1[0])]
        left_const = [1]
        left_val = [0]
        left = [left_var,left_const,left_val]

        right_var = [0]
        right_const = [0]
        right_val = [0]
        right = [right_var,right_const,right_val]

        constraint = Constraint(constraint_type,left,right)
        self.model.add(constraint)

        left_var = [letterlist.index(word_addend2[0])]
        left_const = [1]
        left_val = [0]
        left = [left_var,left_const,left_val]

        right_var = [0]
        right_const = [0]
        right_val = [0]
        right = [right_var,right_const,right_val]

        constraint = Constraint(constraint_type,left,right)
        self.model.add(constraint)

        left_var = [letterlist.index(word_sum[0])]
        left_const = [1]
        left_val = [0]
        left = [left_var,left_const,left_val]

        right_var = [0]
        right_const = [0]
        right_val = [0]
        right = [right_var,right_const,right_val]

        constraint = Constraint(constraint_type,left,right)
        self.model.add(constraint)

        self.letterlist = letterlist

    def get_domain_store(self):
        return self.DS

    def get_model(self):
        return self.model

    def print_solution(self,solutions):
        send = more = money = 0

        for variables in solutions:
            answer_map = {}
            print(variables)
            for value,identifier in zip(variables,self.identifiers):
                answer_map[identifier] = str(value)

            word1_val = int(''.join([i for i in map(lambda x: answer_map[x], self.word1)]))
            word2_val = int(''.join([i for i in map(lambda x: answer_map[x], self.word2)]))
            word3_val = int(''.join([i for i in map(lambda x: answer_map[x], self.word3)]))
            print(self.word1,":",word1_val)
            print(self.word2,":",word2_val)
            print(self.word3,":",word3_val)
            print(self.word1,"+",self.word2,":",word1_val+word2_val)

        # left_vars = []
        # left_const = []
        # right_vars = []
        # right_const = []
        # for variables in solutions:

        #     for i in range(len(self.word3)):
        #         if i == 0:
        #             # Lefthand Eqn
        #             left_vars = [len(self.letterlist)+i] # C4
        #             left_const = [1]
        #             # Righthand Eqn
        #             right_vars = [self.letterlist.index(self.word3[i])] # M
        #             right_const = [1]

        #             l = 0
        #             for var,mult in zip(left_vars,left_const):
        #                 l += mult*variables[var]

        #             r = 0
        #             for var,mult in zip(right_vars,right_const):
        #                 r += mult*variables[var]

        #             print(l,r)



        #         elif i == len(self.word3)-1:
        #             # Lefthand Eqn
        #             left_vars = [self.letterlist.index(self.word1[i-1]),self.letterlist.index(self.word2[i-1])]  # D + E
        #             left_const = [1,1]
        #             # Righthand Eqn
        #             right_vars = [self.letterlist.index(self.word3[i]),len(self.letterlist)+i-1] # Y + C1
        #             right_const = [1,10]

        #             l = 0
        #             for var,mult in zip(left_vars,left_const):
        #                 l += mult*variables[var]

        #             r = 0
        #             for var,mult in zip(right_vars,right_const):
        #                 r += mult*variables[var]

        #             print(l,r)

        #         else:
        #             # Lefthand Eqn
        #             left_vars = [len(self.letterlist)+i,self.letterlist.index(self.word1[i-1]),self.letterlist.index(self.word2[i-1])] # C1 + N + R
        #             left_const = [1,1,1]
        #             # Righthand Eqn
        #             right_vars = [self.letterlist.index(self.word3[i]),len(self.letterlist)+i-1] # E + 10*C2
        #             right_const = [1,10]

        #             l = 0
        #             for var,mult in zip(left_vars,left_const):
        #                 l += mult*variables[var]

        #             r = 0
        #             for var,mult in zip(right_vars,right_const):
        #                 r += mult*variables[var]

        #             print(l,r)

        #     print("========================")


        

        # if money == send+more:
        #     print(send,more)
        #     print(money)
        #     self.solutions.append(money)
        # else:
        #     print(send,more)
        #     print(money)
        #     raise Exception("Error! Solution is not correct")