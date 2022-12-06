import os
import re

def main(part):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		# Part 1 has markers of length 4, part 2 has markers of length 14
		if part == 1:
			num_chars = 4
		else:
			num_chars = 14
		
		line = f.readline()
		position = num_chars
		while(position < len(line)):
			potential_marker = line[position - num_chars :position]
			# Check if the characters in the current potential marker are unique to one another
			if len(set(potential_marker)) == len(potential_marker):
				return(position, potential_marker)
			else:
				position += 1

if __name__ == "__main__":
	part1 = main(1)
	part2 = main(2)
	print(f" Part 1 solution: {part1}, Part 2 solution: {part2}")
