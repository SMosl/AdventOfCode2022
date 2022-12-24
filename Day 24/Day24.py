import os
import time
import numpy as np

def main(part):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		map = f.read().splitlines()	
		start = (1,0)
		end = (len(map[-1]) - 2, len(map)-1)
		open_points = {start, end}
		for y in range(len(map)-2):
			for x in range(len(map[0])-2):
				open_points.add((x+1, y+1))

		dims = (len(map[0])-2, len(map)-2)
		r_blizzard = set()
		d_blizzard = set()
		l_blizzard = set()
		u_blizzard = set()
		for y, line in enumerate(map):
			for x, pos in enumerate(line):
				if pos == '>':
					r_blizzard.add((x,y))
				elif pos == 'v':
					d_blizzard.add((x,y))
				elif pos == '<':
					l_blizzard.add((x,y))
				elif pos == '^':
					u_blizzard.add((x,y))

	minute = 0
	if part == 1:
		return(len(find_shortest_path(end, start, open_points, r_blizzard, d_blizzard, l_blizzard, u_blizzard, minute, dims))-1)
	else:
		there = len(find_shortest_path(end, start, open_points, r_blizzard, d_blizzard, l_blizzard, u_blizzard, minute, dims))-1
		print(there)
		back_again = len(find_shortest_path(start, end, open_points, r_blizzard, d_blizzard, l_blizzard, u_blizzard, there, dims))-1
		print(back_again)
		a_hobbits_tale = len(find_shortest_path(end, start, open_points, r_blizzard, d_blizzard, l_blizzard, u_blizzard, there + back_again, dims))-1
		print(a_hobbits_tale)
		return(there + back_again + a_hobbits_tale)

def find_shortest_path(end, start, open_points, r_blizzard, d_blizzard, l_blizzard, u_blizzard, minute, dims):
	paths = [[(start[0],start[1])]]
	visited = {(start[0],start[1], 0)}
	i = 0

	while i < len(paths):
		path = paths[i]
		path_end = path[-1]
		possible_adjacents = find_neighbours(path_end, open_points, r_blizzard, d_blizzard, l_blizzard, u_blizzard, len(path) + minute, dims)
		if end in possible_adjacents:
			path.append(end)
			return path
		
		for adjacent in possible_adjacents:
			if not (adjacent[0], adjacent[1], (len(path)) % np.lcm(dims[0], dims[1])) in visited:
				new_path = path[:]
				new_path.append((adjacent[0], adjacent[1]))
				paths.append(new_path)
				visited.add((adjacent[0], adjacent[1], (len(new_path) - 1) % np.lcm(dims[0], dims[1])))
		i += 1
	return []

def find_neighbours(point, open_points, r_blizzard, d_blizzard, l_blizzard, u_blizzard, minute, dims):
	blizzard = set()
	for b in r_blizzard:
		blizzard.add((1 + ((b[0] + minute - 1) % dims[0]), b[1]))
	for b in d_blizzard:
		blizzard.add((b[0], 1 + ((b[1] + minute - 1) % dims[1])))
	for b in l_blizzard:
		blizzard.add((1 + ((b[0] - minute - 1) % dims[0]), b[1]))
	for b in u_blizzard:
		blizzard.add((b[0], 1 + ((b[1] - minute - 1) % dims[1])))

	directions = [[0,-1],[0,1],[-1,0],[1,0],[0,0]]		# Note that standing still, direction [0,0], is an option
	output = []
	for d in directions:
		adj_coord = (point[0] + d[0], point[1] + d[1])
		if (adj_coord in open_points):
			if (adj_coord not in blizzard):
				output.append(adj_coord)
	return output

if __name__ == "__main__":
	start_time = time.time()
	part1 = main(1)
	print(f" Part 1 solution: {part1}")
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	mid_time = time.time()
	part2 = main(2)
	print(f" Part 2 solution: {part2}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))