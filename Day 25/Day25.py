import os
import time
import numpy as np

def main():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		conversions = {
			'2' : 2,
			'1' : 1,
			'0' : 0,
			'-' : -1,
			'=' : -2
		}
		solution = 0
		while(len(line := f.readline().strip()) != 0):
			line = line[::-1]
			decimal = 0
			for i, char in enumerate(line):
				decimal += pow(5, i) * conversions[char]
			solution += decimal
	return(dec_to_snafu(solution))

def dec_to_snafu(value):
	solution = ''
	while value != 0:
		value, remainder = divmod(value, 5)
		if remainder < 3:
			solution += str(remainder)
			alex = 0
		elif remainder == 3:
			solution += '='
			alex = 1
		else:
			solution += '-'
			alex = 1
		value += alex
	return(solution[::-1])

if __name__ == "__main__":
	start_time = time.time()
	part1 = main()
	print(f" Part 1 solution: {part1}")
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	#mid_time = time.time()
	#part2 = main()
	#print(f" Part 2 solution: {part2}")
	#print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))