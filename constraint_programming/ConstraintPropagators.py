# Constraint Programming
# Implementing Different types of Constraints using OOP 
from abc import ABCMeta, abstractmethod
import time
from utils import domain_printer
from copy import deepcopy

class Propagator:
    @property
    def constraint_type(self):
        raise NotImplementedError

    @abstractmethod
    def feasibility_check(self): pass

    @abstractmethod
    def prune(self): pass


class NotEqualPropagator(Propagator):
    constraint_type = 'NotEqual'
        

    def feasibility_check(self,domains,constraint):

        left_var = constraint.left[0]
        left_const_mult = constraint.left[1]
        left_val = constraint.left[2]

        right_var = constraint.right[0]
        right_const_mult = constraint.right[1]
        right_val = constraint.right[2]


        maximum = 0
        minimum = 0
        for var,mult in zip(left_var,left_const_mult):
            maximum += mult*max(domains[var])
            minimum += mult*min(domains[var])
        for const in left_val:
            maximum += const
            minimum += const

        leftside = set(range(minimum,maximum+1))

        maximum = 0
        minimum = 0
        for var,mult in zip(right_var,right_const_mult):
            maximum += mult*max(domains[var])
            minimum += mult*min(domains[var])
        for const in right_val:
            maximum += const
            minimum += const

        rightside = set(range(minimum,maximum+1))


        if len(leftside | rightside) >= 2:
            return True
        else:
            return False

    def prune(self,domains,constraint):
        left_var = constraint.left[0]
        left_const_mult = constraint.left[1]
        left_val = constraint.left[2]

        right_var = constraint.right[0]
        right_const_mult = constraint.right[1]
        right_val = constraint.right[2]

        # We can only prune if only one var has a range
        count = 0
        new_domains = domains
        total_vars = []
        for i,var in enumerate(left_var):
            if left_const_mult[i] != 0:
                total_vars.append(var)
        for i,var in enumerate(right_var):
            if right_const_mult[i] != 0:
                total_vars.append(var)

        for idx,var in enumerate(total_vars):
            if len(domains[var]) > 1:
                count += 1
                prune_var = var
                prune_idx = idx


        if count != 1:
            return domains
        
        right_value = 0
        for var,mult in zip(right_var,right_const_mult):
            if var == prune_var: continue
            if len(domains[var]) == 0:
                domain_printer(domains)
            right_value += mult*domains[var][0]
        for const in right_val:
            right_value += const

        left_value = 0
        for var,mult in zip(left_var,left_const_mult):
            if var == prune_var: continue
            if len(domains[var]) == 0:
                domain_printer(domains)
            left_value += mult*domains[var][0]
        for const in left_val:
            left_value += const

        for val in domains[prune_var]:
            if (prune_var in left_var) and (right_value == left_value + val):
                new_domain = set(new_domains[prune_var])
                new_domain.discard(val)
                new_domains[prune_var] = list(new_domain)

            elif (prune_var in right_var) and (left_value == right_value  + val):
                new_domain = set(new_domains[prune_var])
                new_domain.discard(val)
                new_domains[prune_var] = list(new_domain)


        return new_domains 


class EqualityPropagator(Propagator):
    constraint_type = 'Equality'

    def feasibility_check(self,domains,constraint):
        """Run Feasibility Checking 
        for Equality Type of Constraint
        """
        # print("HEEEREEE")
        left_var = constraint.left[0]
        left_const_mult = constraint.left[1]
        left_val = constraint.left[2]

        right_var = constraint.right[0]
        right_const_mult = constraint.right[1]
        right_val = constraint.right[2]


        # Simple Variable-Value Labeling
        if (left_val == [0] and left_const_mult == [1]) and (right_const_mult == [0]):
            if (right_val[0] in domains[left_var[0]]):
                return True
            else:
                return False

        # Simple Variable-Variable Labeling
        elif (left_val == [0] and left_const_mult == [1]) and (right_val == [0] and right_const_mult == [1]):
            if len(set(domains[left_var[0]]) | set(domains[right_var[0]])) > 0:
                return True
            else:
                return False
        
        # Equation
        else:
            l = 0
            for var,mult in zip(left_var,left_const_mult):
                l += mult*max(domains[var])
            for const in left_val:
                l += const

            r = 0
            for var,mult in zip(right_var,right_const_mult):
                r += mult*min(domains[var])
            for const in right_val:
                r += const

            # For Equations (Equal sign)
            total_vars = left_var+right_var
            total_count = len(left_var+right_var)
            count = 0
            for var in total_vars:
                if len(domains[var]) == 1:
                    count += 1

            # For Equations (Equal sign)
            if (count == total_count):
                if l == r:
                    return True
                else:
                    return False

            if l >= r:
                # print(l,r)
                return True
            else:
                return False

    
    def prune(self,domains,constraint):
        """Run Pruning 
        for Equality Type of Constraint
        """
        left_var = constraint.left[0]
        left_const_mult = constraint.left[1]
        left_val = constraint.left[2]

        right_var = constraint.right[0]
        right_const_mult = constraint.right[1]
        right_val = constraint.right[2]

        new_domains = deepcopy(domains)


        # Simple Variable-Value Labeling
        if (left_val == [0] and left_const_mult == [1]) and (right_const_mult == [0]):
            new_domains[left_var[0]] = [right_val[0]]
        
        # Simple Variable-Variable Labeling
        elif (left_val == [0] and left_const_mult == [1]) and (right_val == [0] and right_const_mult == [1]):
            new_set = set(new_domains[left_var[0]]) & set(new_domains[right_var[0]])
            new_domains[left_var[0]] = list(new_set)
            new_domains[right_var[0]] = list(new_set)

        else:
            l = 0
            for var,mult in zip(left_var,left_const_mult):
                l += mult*max(domains[var])
            for const in left_val:
                l += const

            r = 0
            for var,mult in zip(right_var,right_const_mult):
                r += mult*min(domains[var])
            for const in right_val:
                r += const

            # print(l,r)
            # print(new_domains)
            # print(constraint)

            for var,mult in zip(left_var,left_const_mult):
                max_var = max(domains[var])
                comp = (r-(l-mult*max_var)) / mult
                for elem in domains[var]:
                    if elem < comp:
                        new_domains[var].remove(elem)

            for var,mult in zip(right_var,right_const_mult):
                min_var = min(domains[var])
                comp = (l-(r-mult*min_var)) / mult
                for elem in domains[var]:
                    if elem > comp:
                        new_domains[var].remove(elem)

            # for i,domain in enumerate(new_domains):
            #     if len(domain) == 0:
            #         print(i,l,r)
            #         print("Old:",domains)
            #         print("New:",new_domains)
            #         print(domains)
            #         print(constraint)
            #         print("------------------------")
            #         raise SystemError("Domain is Empty!!")

        return new_domains