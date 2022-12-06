import os

def main(part):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		# Part 1 has markers of length 4, part 2 has markers of length 14
		num_chars = (10 * (part - 1)) + 4
		
		line = f.readline()
		for position in range(num_chars, len(line)):
			potential_marker = line[position - num_chars : position]
			# Check if the characters in the current potential marker are unique to one another
			if len(set(potential_marker)) == len(potential_marker):
				return(position, potential_marker)

if __name__ == "__main__":
	part1 = main(1)
	part2 = main(2)
	print(f" Part 1 solution: {part1}, Part 2 solution: {part2}")
