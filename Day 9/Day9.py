import os
import numpy as np

def main(part):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		# Part 1 has 2 knots, part 2 has 10 knots
		num_knots = (8 * (part - 1)) + 2

		positions = [[0,0] for _ in range(num_knots)]
		visited = {(0,0)}
		d = {
			'L' : [-1,0],
			'R' : [1,0],
			'U' : [0,1],
			'D' : [0,-1]
		}
		
		while(len(line := f.readline().split()) != 0):
			(positions, visited) = next_instruction(positions, d[line[0]], int(line[1]), visited)
		return(len(visited))

def next_instruction(positions, direction, distance, visited):
	for i in range(distance):
		positions[0] = [positions[0][0] + direction[0], positions[0][1] + direction[1]]
		for knot in range(len(positions[1:])):
			(positions, visited) = next_step(positions, visited, knot + 1)
	
	return((positions, visited))

def next_step(positions, visited, knot): 
	# If knot ahead moves such that it is further than 1 space away from the current knot, the current knot moves 1 space towards it
	if (abs(positions[knot - 1][0] - positions[knot][0]) > 1) or (abs(positions[knot - 1][1] - positions[knot][1]) > 1):
		positions[knot] = [
			positions[knot][0] + np.sign(positions[knot - 1][0] - positions[knot][0]), 
			positions[knot][1] + np.sign(positions[knot - 1][1] - positions[knot][1])
			]
	
	# Record the position of the final knot if it is a new position
	if (positions[-1][0], positions[-1][1]) not in visited:
		visited.add((positions[-1][0], positions[-1][1]))
	
	return (positions, visited)

if __name__ == "__main__":
	part1 = main(1)
	part2 = main(2)
	print(f" Part 1 solution: {part1}, Part 2 solution: {part2}")
