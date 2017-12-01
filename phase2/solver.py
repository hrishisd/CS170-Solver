from random import random
import argparse
import random
import numpy as np
from collections import defaultdict
import operator
import math

"""
======================================================================
  Complete the following function.
======================================================================
"""

def solve(num_wizards, num_constraints, wizards, constraints):
    """
    Write your algorithm here.
    Input:
        num_wizards: Number of wizards
        num_constraints: Number of constraints
        wizards: An array of wizard names, in no particular order
        constraints: A 2D-array of constraints, 
                     where constraints[0] may take the form ['A', 'B', 'C']i

    Output:
        An array of wizard names in the ordering your algorithm returns
    """

    def generate_neighbor(ordering):
        i, j = random.sample(range(num_wizards), k=2)
        new_ordering = list(ordering)
        new_ordering[i], new_ordering[j] = new_ordering[j], new_ordering[i]
        return new_ordering
    
    def cost(ordering):
        #TODO: can speed this up
        return count_invalid_constraints(ordering)

    def acceptance_probability(old_cost, new_cost, T):
        exponent = (old_cost - new_cost)/T
        try:
            ans = math.exp(exponent)
        except OverflowError:
            #print "overflow for exponent =", exponent
            if exponent > 0:
                ans = 0
            else:
                ans = 1
        return ans

    def anneal(solution):
        old_cost = cost(solution)
        T = 1.0
        T_min = 0.00001
        alpha = 0.9
        while T > T_min:
            i = 1
            while i <= 100:
                new_solution = generate_neighbor(solution)
                new_cost = cost(new_solution)
                ap = acceptance_probability(old_cost, new_cost, T)
                if ap > random.random():
                    solution = new_solution
                    old_cost = new_cost
                    #print new_cost
                i += 1
            T = T*alpha
        return solution, old_cost

    def map_wiz_to_index(partial_ordering):
        mapping = {}
        for i, wiz in enumerate(partial_ordering):
            mapping[wiz] = i

        return mapping

    def count_invalid_constraints(partial_ordering):
        wiz_to_invalid = map_wiz_to_invalid_constraint(partial_ordering)
        count = sum(wiz_to_invalid.values())
        return count/3

    def map_wiz_to_invalid_constraint(partial_ordering):
        wiz_to_index = map_wiz_to_index(partial_ordering)

        mapping = defaultdict(int)
    
        for constraint in constraints:
            w1, w2, w3 = constraint[0], constraint[1], constraint[2]
            i, j, k = wiz_to_index[w1], wiz_to_index[w2], wiz_to_index[w3]
            if (k > i and k < j) or (k < i and k > j):
                mapping[w1] += 1
                mapping[w2] += 1
                mapping[w3] += 1
        return mapping

    def get_most_invalid_wiz(partial_ordering):
        #get mapping from wiz to num invalid
        wiz_to_invalid = map_wiz_to_invalid_constraint(partial_ordering)

        #get wiz with max invalid count 
        max_wiz = max(wiz_to_invalid.items(), key=operator.itemgetter(1))[0]

        return max_wiz

    def update(partial_ordering):
        """
        returns a better ordering from 1 swap
        """

        #Pick a random wizard
        max_wiz = get_most_invalid_wiz(partial_ordering)

        #rand_wiz = random.choice(partial_ordering)

        bad_wiz_index = partial_ordering.index(max_wiz)

        initial_num_invalid = count_invalid_constraints(partial_ordering)

        curr_num_invalid = initial_num_invalid

        for i in range(num_wizards):
            if i == bad_wiz_index:
                pass
            partial_ordering[i], partial_ordering[bad_wiz_index] = partial_ordering[bad_wiz_index], partial_ordering[i]
            if count_invalid_constraints(partial_ordering) < curr_num_invalid:
                curr_num_invalid = count_invalid_constraints(partial_ordering)
                bad_wiz_index = i
            else:
                partial_ordering[i], partial_ordering[bad_wiz_index] = partial_ordering[bad_wiz_index], partial_ordering[i]

        if (curr_num_invalid == initial_num_invalid):
            rand_wiz = random.choice(partial_ordering)
            rand_wiz_index = partial_ordering.index(rand_wiz)
            for i in range(num_wizards):
                if i == rand_wiz_index:
                    pass
                partial_ordering[i], partial_ordering[rand_wiz_index] = partial_ordering[rand_wiz_index], \
                                                                       partial_ordering[i]
                if count_invalid_constraints(partial_ordering) < curr_num_invalid:
                    curr_num_invalid = count_invalid_constraints(partial_ordering)
                    rand_wiz_index = i
                else:
                    partial_ordering[i], partial_ordering[rand_wiz_index] = partial_ordering[rand_wiz_index], \
                                                                           partial_ordering[i]
        return list(partial_ordering)

    #def random_update(partial_ordering):




    # best = wizards
    # best_invalid = count_invalid_constraints(wizards)
    # print ("num constraints", num_constraints)
    # print("init invalid", best_invalid)
    # while(best_invalid > 100):
    #     temp = np.random.permutation(wizards)
    #     curr_invalid = count_invalid_constraints(temp)
    #     #print(curr_invalid)
    #     if (curr_invalid < best_invalid):
    #         best_invalid = curr_invalid
    #         best = temp
    #         print(best_invalid)
    #         print best

    #     if best_invalid == 0:
    #         break

    # updated_ordering = best.tolist()
    # prev_num_invalid = count_invalid_constraints(updated_ordering)
    # while (best_invalid > 10):
    #     updated_ordering = update(updated_ordering)
    #     curr_num_invalid = count_invalid_constraints(updated_ordering)
    #     print curr_num_invalid
    #     if curr_num_invalid == prev_num_invalid:
    #         pass

    #     prev_num_invalid = curr_num_invalid



    # #print(constraints, constraints)
    # return updated_ordering
    #for _ in range()

    best_solution, best_cost = anneal(wizards)
    print best_cost
    while best_cost > 0:
        random.shuffle(wizards)
        curr_solution, curr_cost = anneal(wizards)
        if curr_cost < best_cost:
            best_solution, best_cost = curr_solution, curr_cost
            print curr_cost
    return best_solution


"""
======================================================================
   No need to change any code below this line
======================================================================
"""

def read_input(filename):
    with open(filename) as f:
        num_wizards = int(f.readline())
        num_constraints = int(f.readline())
        constraints = []
        wizards = set()
        for _ in range(num_constraints):
            c = f.readline().split()
            constraints.append(c)
            for w in c:
                wizards.add(w)
                
    wizards = list(wizards)
    return num_wizards, num_constraints, wizards, constraints

def write_output(filename, solution):
    with open(filename, "w") as f:
        for wizard in solution:
            f.write("{0} ".format(wizard))

if __name__=="__main__":
    parser = argparse.ArgumentParser(description = "Constraint Solver.")
    parser.add_argument("input_file", type=str, help = "___.in")
    parser.add_argument("output_file", type=str, help = "___.out")
    args = parser.parse_args()

    num_wizards, num_constraints, wizards, constraints = read_input(args.input_file)
    solution = solve(num_wizards, num_constraints, wizards, constraints)
    write_output(args.output_file, solution)
