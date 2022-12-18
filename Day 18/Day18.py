import os
import time
import numpy as np

def parse_input():
	# Parse the input, returning a set of coordinates that are offset by 1 to remove any possible boundary collision
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		coords = set()
		while(len(line := f.readline().strip()) != 0):
			raw_input = [int(x) for x in line.split(',')]
			input_offset = (raw_input[0] + 1, raw_input[1] + 1, raw_input[2] + 1)
			coords.add(input_offset)
		return(coords)

def main1():
	# Finds the number of faces that are shared between the input set of coordinates
	coords = parse_input()
	shared_faces = find_surface_area(coords, coords)
	return(6 * len(coords) - shared_faces)

def main2():
	coords = parse_input()
	bounds = [max([x[0] for x in coords]) + 2, max([x[1] for x in coords]) + 2, max([x[2] for x in coords]) + 2]
	# Create a matrix of zeroes with a buffer space of 1 around the input shape, set the shape coordinates as having value 2
	matrix = np.zeros((bounds[0], bounds[1], bounds[2]))
	for point in coords:
		matrix[point[0]][point[1]][point[2]] = 2
	# Flood fill the exterior of the shape, any position pathable to from (0, 0, 0) is the exterior, set its value as 1
	queue = [(0,0,0)]
	count = 0
	while len(queue) > 0:
		x, y, z = queue[0][0], queue[0][1], queue[0][2]
		if matrix[x][y][z] == 2:
			count += 1
		elif matrix[x][y][z] == 0:
			matrix[x][y][z] = 1
			if x > 0:
				queue.append((x - 1, y, z))
			if x < bounds[0] - 1:
				queue.append((x + 1, y, z))
			if y > 0:
				queue.append((x, y - 1, z))
			if y < bounds[1] - 1:
				queue.append((x, y + 1, z))
			if z > 0:
				queue.append((x, y, z - 1))
			if z < bounds[2] - 1:
				queue.append((x, y, z + 1))
		queue = queue[1:]
	# Create sets of coordinates of all air positions and lava positions
	air = set()
	lava = set()
	for z, plane in enumerate(matrix):
		for y, line in enumerate(plane):
			for x, point in enumerate(line):
				if point == 1:
					air.add((x, y, z))
				elif point == 2:
					lava.add((x, y, z))
	# Find the number of shared faces between the exterior air and the lava
	shared_faces = find_surface_area(air, lava)
	return(shared_faces)

def find_surface_area(input_set, coords):
	shared_faces = 0
	for point in coords:
		for other in set(x for x in input_set if x != point):
			adjacent_x = {point[0] + 1, point[0] - 1}
			adjacent_y = {point[1] + 1, point[1] - 1}
			adjacent_z = {point[2] + 1, point[2] - 1}
			if other[0] in adjacent_x and other[1] == point[1] and other[2] == point[2]:
				shared_faces += 1
			elif other[1] in adjacent_y and other[0] == point[0] and other[2] == point[2]:
				shared_faces += 1
			elif other[2] in adjacent_z and other[0] == point[0] and other[1] == point[1]:
				shared_faces += 1
	return(shared_faces)

if __name__ == "__main__":
	
	start_time = time.time()
	part1 = main1()
	print(f" Part 1 solution: {part1}")
	mid_time = time.time()
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	part2 = main2()
	print(f" Part 2 solution: {part2}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))