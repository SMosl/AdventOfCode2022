import os

def main(part):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	# Read the input data, record the start and end points, and create a map of ints for easier neighbouring height comparisons
	with open(f"{dir_path}/input.txt", "r") as f:
		map = []
		part2_start = []
		for y, line in enumerate(f.read().splitlines()):
			l = []
			for x, point in enumerate(line):
				if point == 'S':
					start = [y,x]
					part2_start.append([y,x])
					l.append(96)	# Want the start position 'S' to have value one less than ord(a) = 97
				elif point == 'E':
					end = [y,x]
					l.append(123)	# Want the end position 'E' to have value one more than ord(z) = 122
				elif point == 'a':
					part2_start.append([y,x])
					l.append(ord(point))
				else:
					l.append(ord(point))
			map.append(l)

	# Create a dict of valid neighbours
	graph = {}
	for y, line in enumerate(map):
		for x, pos in enumerate(line):
			graph[(y,x)] = create_graph((y,x), map[y][x], map)
	
	# For part 1, we only consider a single start point, 'S'
	if part == 1:
		return(len(find_shortest_path(graph, end, start)) - 1)
	else:
		# For part 2, we consider any point of elevation 'a' or 'S' as a starting point and find the overall shortest path
		part2_answers = []
		for start_point in part2_start:
			shortest = len(find_shortest_path(graph, end, start_point)) - 1
			if shortest > 0:
				part2_answers.append(shortest)
		part2_answers.sort()
		return(part2_answers[0])

def find_shortest_path(graph, end, start):
	# Use breadth first search to find the shortest path from the start point to the end point
	paths = [[(start[0],start[1])]]
	visited = {(start[0],start[1])}
	i = 0

	while i < len(paths):
		path = paths[i]
		path_end = path[-1]
		possible_adjacents = graph[path_end]
		if end in possible_adjacents:
			path.append(end)
			return path
		
		for adjacent in possible_adjacents:
			if not (adjacent[0], adjacent[1]) in visited:	
				new_path = path[:]
				new_path.append((adjacent[0], adjacent[1]))
				paths.append(new_path)
				visited.add((adjacent[0], adjacent[1]))
		i += 1
	return []

def create_graph(coord, height, map):
	# For each coordinate, return a list of orthogonally adjacent neighbours with height of at most 1 higher than the input coord
	directions = [[0,-1],[0,1],[-1,0],[1,0]]
	output = []
	for d in directions:
		adj_coord = [coord[0] + d[0], coord[1] + d[1]]
		if (adj_coord[0] in range(len(map))) and (adj_coord[1] in range(len(map[0]))):
			if (map[adj_coord[0]][adj_coord[1]] <= height + 1) or (map[adj_coord[0]][adj_coord[1]] == 123):
				output.append(adj_coord)
	return output

if __name__ == "__main__":
	part1 = main(1)
	part2 = main(2)
	print(f" Part 1 solution: {part1}, Part 2 solution: {part2}")
