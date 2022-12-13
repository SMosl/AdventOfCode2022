import os
import ast

def main1():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		pairs = [(ast.literal_eval(x.split('\n')[0]), ast.literal_eval(x.split('\n')[1])) for x in f.read().split('\n\n')]
		indices = []
		for i in range(len(pairs)):
			indices.append(compare(pairs[i][0], pairs[i][1]))
		return(sum([i + 1 for  i, x in enumerate(indices) if (x == True)]))

def main2():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		input = f.read().split('\n\n')
		pairs = []
		for pair in input:
			lines = pair.split('\n')
			pairs = pairs + [ast.literal_eval(lines[0]), ast.literal_eval(lines[1])]
		pairs = pairs + [[[2]], [[6]]]

		num_true = 0
		while num_true < len(pairs) - 1:
			num_true = 0
			for i in range(len(pairs) - 1):
				if compare(pairs[i], pairs[i + 1]) == False:
					pairs[i], pairs[i + 1] = pairs[i + 1], pairs[i]
				else:
					num_true += 1

		return((pairs.index([[2]]) + 1) * (pairs.index([[6]]) + 1))

def compare(left, right):
	index = 0
	for index in range(len(left)):	
		try:
			if type(left[index]) == type(right[index]) == int:
				if left[index] > right[index]:
					return(False)
				elif left[index] < right[index]:
					return(True)
				else:
					index += 1
			elif type(left[index]) == list and type(right[index]) == int:
				comparison = compare(left[index], [right[index]])
				if type(comparison) == bool:
					return(comparison)
				else:
					index += 1
			elif type(left[index]) == int and type(right[index]) == list:
				comparison = compare([left[index]], right[index])
				if type(comparison) == bool:
					return(comparison)
				else:
					index += 1
			else:
				comparison = compare(left[index], right[index])
				if type(comparison) == bool:
					return(comparison)
				else:
					index += 1
		except IndexError:
			return(False)

	if len(left) < len(right):
		return(True)

if __name__ == "__main__":
	part1 = main1()
	part2 = main2()
	print(f" Part 1 solution: {part1}, Part 2 solution: {part2}")
