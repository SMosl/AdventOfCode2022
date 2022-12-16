import os
import time
import re
from itertools import combinations

def following_a_hunch():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		graph = {}
		rates = {}
		valves_closed = set()
		while(len(line := f.readline().strip()) != 0):
			valves = re.findall(r'[A-Z]{2}',line)
			graph[valves[0]] = set(valves[1:])
			rates[valves[0]] = int(re.findall(r'\d+',line)[0])
			valves_closed.add(valves[0])
	
	path_graph = {}
	for i in graph.keys():
		path_graph[i] = {}
		for j in graph.keys():
			if j != i:
				shortest = find_shortest_path(graph, j, i)
				path_graph[i][j] = len(shortest) - 1

	non_zero_valves = set(x for x in graph.keys() if rates[x] != 0)
	return(non_zero_valves, path_graph, graph, rates)

def find_solution(non_zero_valves, path_graph, graph, rates, part):
	paths30 = []
	total_time = abs((part - 2)*4) + 26
	time_left = total_time

	iterating_paths = [['AA', total_time]]
	while len(iterating_paths):
		current_path = iterating_paths[0]
		time_left = current_path[-1]
		current_valve = current_path[-2]
		if current_valve in non_zero_valves:
			values_to_check = set(x for x in non_zero_valves if x != current_valve)
		else:
			values_to_check = non_zero_valves
		possible_additions = set(x for x in values_to_check if path_graph[current_valve][x] < time_left and x not in set(current_path[:-2]))
		if len(possible_additions) > 0:
			for y in possible_additions:
				new_path = current_path[:-1] + [y]
				new_path.append(time_left - path_graph[current_valve][y] - 1)
				iterating_paths.append(new_path)
			iterating_paths.pop(0)
		else:
			paths30.append(current_path)
			iterating_paths.pop(0)
	

	paths30 = [x[:-1] for x in paths30]
	best_result = 0
	for perm in paths30:
		current_time_passed = 0
		total_pressure_released = 0
		pps = 0
		visited = []
		for i in range(len(perm) - 1):
			# Find path to next valve
			s = find_shortest_path(graph, perm[i+1], perm[i])
			# If you can't travel to the next valve (and turn it on) in time, don't bother and just calculate end total pressure
			if current_time_passed + len(s) > total_time:
				total_pressure_released += (total_time - current_time_passed) * pps
			# If you do have time to visit the valve and turn it on
			else:
				# Update the current time and total pressure
				current_time_passed += len(s)
				total_pressure_released += len(s) * pps
				# Turn on the valve
				pps += rates[perm[i+1]]
				visited.append(perm[i+1])

		while current_time_passed < total_time:
			current_time_passed += 1
			total_pressure_released += pps
							
		if total_pressure_released > best_result:
			best_result = total_pressure_released

	return(best_result)

def main1():
	(non_zero_valves, path_graph, graph, rates) = following_a_hunch()
	answer = find_solution(non_zero_valves, path_graph, graph, rates, 1)
	return(answer)

def main2():
	(non_zero_valves, path_graph, graph, rates) = following_a_hunch()
	all_combs = [x for x in combinations(non_zero_valves, 7)]

	best_answer = 0

	for comb in all_combs:
		comb_input = list(comb)
		complement = [x for x in non_zero_valves if x not in comb_input]
		comb_answer = find_solution(comb_input, path_graph, graph, rates, 2)
		complement_answer = find_solution(complement, path_graph, graph, rates, 2)
		if comb_answer + complement_answer > best_answer:
			best_answer = comb_answer + complement_answer

	return(best_answer)

def find_shortest_path(graph, end, start):
	# Use breadth first search to find the shortest path from the start point to the end point
	paths = [[start]]
	visited = {start}
	i = 0

	while i < len(paths):
		path = paths[i]
		path_end = path[-1]
		possible_adjacents = graph[path_end]
		if end in possible_adjacents:
			path.append(end)
			return path
		
		for adjacent in possible_adjacents:
			if not adjacent in visited:	
				new_path = path[:]
				new_path.append(adjacent)
				paths.append(new_path)
				visited.add(adjacent)
		i += 1
	return []

if __name__ == "__main__":
	
	start_time = time.time()
	part1 = main1()
	print(f" Part 1 solution: {part1}")
	mid_time = time.time()
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	
	part2 = main2()
	print(f" Part 2 solution: {part2}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))