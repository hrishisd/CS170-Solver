import itertools
import random
import string
import numpy as np

def generateConstraints(num_names, name_len):
	names = [''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(name_len)) for _ in range(num_names)]
	constraints = list()
	#print (" ".join(names))

	ordering = range(50)
	random.shuffle(ordering)

	#first include constraints with at least every wizard
	'''
	for i in ordering:
		constraint = [None]*3
		insert_index = random.randint(1, 3)
		constraint[insert_index] = names[i]


		constraints.append(names[])
	'''

	constraint_samples = []

	for _ in range(500):
		constraint_indices = np.array(np.random.choice(num_names, size=3, replace=False))
		constraint_samples.append(constraint_indices)

	for constraint in constraint_samples:
		#get indices in sorted order
		constraint = sorted(constraint.tolist())

		#which name will be the last one
		outer = random.choice([0, 2]) 
		last_index = constraint[outer]

		#remove the last one from the list
		del constraint[outer]
		first_two = constraint
		random.shuffle(first_two)
		indices = first_two + [last_index]
		constraints.append(' '.join([names[i] for i in indices]))

	print num_names
	print " ".join(names)
	print len(constraints)
	print '\n'.join(constraints)

generateConstraints(35, 10)
