import argparse
import random
import numpy as np


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
    def count_invalid_constraints(partial_ordering):
        mapping = {}
        count = 0
        for i, wiz in zip(range(num_wizards), partial_ordering):
            mapping[wiz] = i
        for constraint in constraints:
            w1, w2, w3 = constraint[0], constraint[1], constraint[2]
            i, j, k = mapping[w1], mapping[w2], mapping[w3]
            if (k > i and k < j) or (k < i and k > j):
                count += 1

        return count

    best = wizards
    best_invalid = count_invalid_constraints(wizards)
    print ("num constraints", num_constraints)
    print("init invalid", best_invalid)
    while(best_invalid > 10):
        temp = np.random.permutation(wizards)
        curr_invalid = count_invalid_constraints(temp)
        #print(curr_invalid)
        if (curr_invalid < best_invalid):
            best_invalid = curr_invalid
            best = temp
            print(best_invalid)
            print(best)

        if best_invalid == 0:
            break



    #print(constraints, constraints)
    return best

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
