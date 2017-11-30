import argparse
import random
import numpy as np
from collections import defaultdict
import operator

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
    #construct edges (edge is called w1;w2 iff w1 < w2)
    E = {}
    for i in range(num_wizards):
        for j in range(i + 1, num_wizards):
            w1, w2 = wizards[i], wizards[j]
            if w1 < w2:
                E[(w1, w2)] = 0
            else:
                E[(w2, w1)] = 0
    #increment the counts
    for constraint in constraints:
        w1, w2, w3 = constraint[0], constraint[1], constraint[2]
        #do it for w1 and w3
        if w1 < w3:
            E[(w1, w3)] += 1
        else:
            E[(w3, w1)] += 1
        #do it for w2 and w3
        if w2 < w3:
            E[(w2, w3)] += 1
        else:
            E[(w3, w2)] += 1
    #filter edges based on constraints
    threshold = num_wizards - 2
    filteredE = set()
    for edge in E:
        if E[edge] <= threshold:
            filteredE.add(edge)

    #get the degrees
    degreeDict = {}
    for wiz in wizards:
        degreeDict[wiz] = 0
    for w1, w2 in filteredE:
        degreeDict[w1] += 1
        degreeDict[w2] += 1

    #associate to each edge to number of neighbors (reinitialize E)
    E = {}
    for i in range(num_wizards):
        for j in range(i + 1, num_wizards):
            w1, w2 = wizards[i], wizards[j]
            if w1 < w2:
                E[(w1, w2)] = degreeDict[w1] + degreeDict[w2]
            else:
                E[(w2, w1)] = degreeDict[w1] + degreeDict[w2]

    #get rid of highest element. redo procedure
    sortedE = sorted(E, key=lambda k: E[k])
    sortedE = sortedE[0:len(sortedE)-1]
    while (len(sortedE) > num_wizards - 1):
        degreeDict = {}
        for wiz in wizards:
            degreeDict[wiz] = 0
        for w1, w2 in sortedE:
            degreeDict[w1] += 1
            degreeDict[w2] += 1
        E = {}
        for edge in sortedE:
            E[edge] = degreeDict[edge[0]] + degreeDict[edge[1]]
        sortedE = sorted(E, key=lambda k: E[k])
        sortedE = sortedE[0:len(sortedE)-2]

    #sort edges into path
    ordering = []
    degreeDict = {}
    for wiz in wizards:
        degreeDict[wiz] = 0
    for w1, w2 in sortedE:
        degreeDict[w1] += 1
        degreeDict[w2] += 1
    nextWiz = ""
    for edge in sortedE:
        if degreeDict[edge[0]] == 1:
            ordering.append(edge[0])
            ordering.append(edge[1])
            nextWiz = edge[1]
            sortedE.remove(edge)
            break
        elif degreeDict[edge[1]] == 1:
            ordering.append(edge[1])
            ordering.append(edge[0])
            nextWiz = edge[0]
            sortedE.remove(edge)
            break
    while len(sortedE) > 1:
        print(len(sortedE))
        for edge in sortedE:
            if edge[0] == nextWiz:
                ordering.append(edge[1])
                nextWiz = edge[1]
                sortedE.remove(edge)
                break
            elif edge[1] == nextWiz:
                ordering.append(edge[0])
                nextWiz = edge[0]
                sortedE.remove(edge)
                break
    for e in sortedE:
        if e[0] == nextWiz:
            ordering.append(e[1])
        else:
            ordering.append(e[0])
    print("sorted: ", ordering)
    return ordering



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
