import os
import time
import re
import operator
import sympy

def main():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		vals = {}
		operations = {}
		while(len(line := f.readline().strip()) != 0):
			val = re.findall(r'\d+', line)
			line = line.split(': ')
			if len(val) > 0:
				vals[line[0]] = int(val[0])
			else:
				operations[line[0]] = [line[1][:4], line[1][5], line[1][7:]]
	
	ops = { '+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv }
	# We have a dictionary of names with their defined value, 'vals', and another of names with their operation, 'operations'
	# Iterate over the operations, substituting known values and evaluating if simplified
	solution = False
	while solution == False:
		for unsolved in operations:
			for i, value in enumerate(operations[unsolved]):
				if value in vals:
					operations[unsolved][i] = vals[value]
		vals, operations = evaluate(vals, operations, ops)
		if 'root' in vals:
			solution = vals['root']

	return(solution)

def main2():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		vals = {}
		operations = {}
		while(len(line := f.readline().strip()) != 0):
			val = re.findall(r'\d+', line)
			line = line.split(': ')
			if len(val) > 0:
				vals[line[0]] = int(val[0])
			else:
				operations[line[0]] = [line[1][:4], line[1][5], line[1][7:]]

	ops = { '+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv }
	LHS = [operations['root'][0]]
	RHS = [operations['root'][2]]
	# goal is to solve (root: LHS = RHS) where LHS and RHS are expressions in terms of humn
	del vals['humn']
	del operations['root']
	solution = False

	# Reduce the set of operations to only be those that depend on the value of humn
	while solution == False:
		num_unsolved = len(operations)
		for unsolved in operations:
			for i, value in enumerate(operations[unsolved]):
				if value in vals:
					operations[unsolved][i] = vals[value]
		vals, operations = evaluate(vals, operations, ops)
		if len(operations) == num_unsolved:
			solution = True
	# Repeatedly replace any instances of an operation with its expanded version (eg 'sllz + lgvd' becomes '(4 - (ljgn * ptdq))' in the example)
	# It happens that RHS is an integer and does not depend on the value of humn
	continuing = True
	while continuing:
		matches = 0
		for i, x in enumerate(LHS):
			if x in vals:
				matches += 1
				for y in [z for z in range(len(LHS)) if LHS[z] == x]:
					LHS[y] = vals[x]
			elif x in operations:
				matches += 1
				del LHS[i]
				LHS = LHS[:i] + ['(', operations[x][0], operations[x][1], operations[x][2], ')'] + LHS[i:]
		if matches == 0:
			continuing = False
	# Convert LHS from list form to string, eg from [4, '-', '(', 'ljgn', '*', 'ptdq', ')'] to '4-(ljgn*ptdq)'
	LHS = ''.join([str(s) for s in LHS])
	RHS = vals[RHS[0]]
	# Define 'humn' as a symbol and pass the expression into sympy
	expression = sympy.parse_expr(LHS)
	humn = sympy.Symbol('humn')
	eqa = sympy.Eq(expression, RHS)
	solution = sympy.solve(eqa)

	return(solution[0])

def evaluate(vals, operations, ops):
	# If both sides of an operation have a value, evaluate the operation, remove from the dict of operations and add to vals
	removed_keys = set()
	for o in operations:
		if type(operations[o][0]) == int and type(operations[o][2]) == int and operations[o][1] != '=':
			vals[o] = int(ops[operations[o][1]](operations[o][0],operations[o][2]))
			removed_keys.add(o)
	for o in removed_keys:
		del operations[o]
	return(vals, operations)

if __name__ == "__main__":
	
	start_time = time.time()
	part1 = main()
	print(f" Part 1 solution: {part1}")
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	mid_time = time.time()
	part2 = main2()
	print(f" Part 2 solution: {part2}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))