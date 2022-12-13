import os
import ast

def main1():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		# Separate the input into a list of pairs of lists
		pairs = [(ast.literal_eval(x.split('\n')[0]), ast.literal_eval(x.split('\n')[1])) for x in f.read().split('\n\n')]
		
		# indices will list whether a pair is in the correct order, 'True', or not, 'False' 
		indices = []
		for i in range(len(pairs)):
			indices.append(compare(pairs[i][0], pairs[i][1]))
		
		# Part 1 asks for the sum of the indices of the matching pairs
		return(sum([i + 1 for  i, x in enumerate(indices) if (x == True)]))

def main2():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		packets = [ast.literal_eval(x) for x in f.read().splitlines() if (x != '')] + [[[2]], [[6]]]
		
		# Repeat the following until every pairwise comparison returns True
		num_true = 0
		while num_true < len(packets) - 1:
			num_true = 0
			# Compare each element in the list of packets with the next, swapping their positions if left > right
			for i in range(len(packets) - 1):
				if compare(packets[i], packets[i + 1]) == False:
					packets[i], packets[i + 1] = packets[i + 1], packets[i]
				else:
					num_true += 1

		# Part 2 asks for the product of the indices of the two divider packets, [[2]] and [[6]]
		return((packets.index([[2]]) + 1) * (packets.index([[6]]) + 1))

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
			# In the case that right runs out of items before left
			return(False)

	# In the case that left runs out of items before right
	if len(left) < len(right):
		return(True)

if __name__ == "__main__":
	part1 = main1()
	part2 = main2()
	print(f" Part 1 solution: {part1}, Part 2 solution: {part2}")
