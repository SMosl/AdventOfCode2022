import os
import time

def main(num_rocks):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		while(len(line := f.readline().strip()) != 0):
			instructions = line
	
	rocks = [
		{(2, 0), (3, 0), (4, 0), (5, 0)}, 
		{(2, 1), (3, 1), (4, 1), (3, 0), (3, 2)}, 
		{(2, 0), (3, 0), (4, 0), (4, 1), (4, 2)}, 
		{(2, 0), (2, 1), (2, 2), (2, 3)}, 
		{(2, 0), (3, 0), (2, 1), (3, 1)}
		]

	gas = {'>' : 1, '<' : -1}
	highest_rock = 0
	floor = {(0, -1), (1, -1), (2, -1), (3, -1), (4, -1), (5, -1), (6, -1)}
	direction_index = -1
	heights = {0}
	
	num_rocks_stopped = 0
	cycle_dict = {}

	for i in range(num_rocks):
		# Find the rock starting position
		rock_position = set((x[0], x[1] + highest_rock + 3) for x in rocks[i % 5])
		moving = True
		while moving:
			direction_index += 1
			# Find the position the rock is after pushed by gas
			after_gas = set((x[0] + gas[instructions[direction_index % len(instructions)]], x[1]) for x in rock_position)
			if valid_position(after_gas, floor):
				rock_position = after_gas
			# Then try to move down 1 unit
			after_fall = set((x[0], x[1] - 1) for x in rock_position)
			if valid_position(after_fall, floor):
				rock_position = after_fall
			else:
				# If the rock cannot fall, it has come to rest
				num_rocks_stopped += 1
				floor = floor.union(rock_position)
				rock_height = max({x[1] + 1 for x in rock_position})
				heights.add(rock_height)
				highest_rock = max(rock_height, highest_rock)
				
				pair = (i % 5, direction_index % len(instructions))

				cycle_dict[pair] = (num_rocks_stopped, highest_rock)
				
				moving = False
	return(highest_rock)

def main2():
	rocks, gas, instructions, heights, floor = parse_input()
	find_start_vals = find_cycle_start(rocks, gas, instructions, heights, floor)
	num_rocks_before_cycle = find_start_vals[0]
	mystery_value = find_start_vals[1]
	cycle_length = find_cycle_length(rocks, gas, instructions, heights, floor, mystery_value)
	tot_cycles = (1000000000000 - num_rocks_before_cycle) // cycle_length
	height_of_cycle = main(num_rocks_before_cycle + cycle_length) - main(num_rocks_before_cycle)
	num_rocks_after_cycles = (1000000000000 - num_rocks_before_cycle - (tot_cycles * cycle_length))
	total_buffer = main(num_rocks_before_cycle + num_rocks_after_cycles)
	return((tot_cycles * height_of_cycle) + total_buffer)

def valid_position(rock_position, floor):
	for x_coord in rock_position:
		if x_coord[0] > 6 or x_coord[0] < 0 or x_coord in floor:
			return False
	return True

def parse_input():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		while(len(line := f.readline().strip()) != 0):
			instructions = line
	
	rocks = [
		{(2, 0), (3, 0), (4, 0), (5, 0)}, 
		{(2, 1), (3, 1), (4, 1), (3, 0), (3, 2)}, 
		{(2, 0), (3, 0), (4, 0), (4, 1), (4, 2)}, 
		{(2, 0), (2, 1), (2, 2), (2, 3)}, 
		{(2, 0), (3, 0), (2, 1), (3, 1)}
		]
	gas = {'>' : 1, '<' : -1}
	floor = {(0, -1), (1, -1), (2, -1), (3, -1), (4, -1), (5, -1), (6, -1)}
	heights = {0}
	return(rocks, gas, instructions, heights, floor)

def find_cycle_start(rocks, gas, instructions, heights, floor):
	highest_rock = 0
	direction_index = -1
	num_rocks_stopped = 0
	cycle_dict = {}
	i = -1
	while i > -2:
		i += 1
		# Find the rock starting position
		rock_position = set((x[0], x[1] + highest_rock + 3) for x in rocks[i % 5])
		moving = True
		while moving:
			direction_index += 1
			# Find the position the rock is after pushed by gas
			after_gas = set((x[0] + gas[instructions[direction_index % len(instructions)]], x[1]) for x in rock_position)
			if valid_position(after_gas, floor):
				rock_position = after_gas
			# Then try to move down 1 unit
			after_fall = set((x[0], x[1] - 1) for x in rock_position)
			if valid_position(after_fall, floor):
				rock_position = after_fall
			else:
				# If the rock cannot fall, it has come to rest
				num_rocks_stopped += 1
				floor = floor.union(rock_position)
				rock_height = max({x[1] + 1 for x in rock_position})
				heights.add(rock_height)
				highest_rock = max(rock_height, highest_rock)
				
				pair = (i % 5, direction_index % len(instructions))
				if pair in cycle_dict.keys():
					return([num_rocks_stopped, num_rocks_stopped - cycle_dict[pair][0]])
				else:
					cycle_dict[pair] = (num_rocks_stopped, highest_rock)
				moving = False

def find_cycle_length(rocks, gas, instructions, heights, floor, mystery_value):
	highest_rock = 0
	direction_index = -1
	num_rocks_stopped = 0
	cycle_dict = {}
	i = -1
	while i > -2:
		i += 1
		# Find the rock starting position
		rock_position = set((x[0], x[1] + highest_rock + 3) for x in rocks[i % 5])
		moving = True
		while moving:
			direction_index += 1
			# Find the position the rock is after pushed by gas
			after_gas = set((x[0] + gas[instructions[direction_index % len(instructions)]], x[1]) for x in rock_position)
			if valid_position(after_gas, floor):
				rock_position = after_gas
			# Then try to move down 1 unit
			after_fall = set((x[0], x[1] - 1) for x in rock_position)
			if valid_position(after_fall, floor):
				rock_position = after_fall
			else:
				# If the rock cannot fall, it has come to rest
				num_rocks_stopped += 1
				floor = floor.union(rock_position)
				rock_height = max({x[1] + 1 for x in rock_position})
				heights.add(rock_height)
				highest_rock = max(rock_height, highest_rock)
				
				pair = (i % 5, direction_index % len(instructions))
				if pair in cycle_dict.keys() and (num_rocks_stopped - cycle_dict[pair][0] != mystery_value):
					return(num_rocks_stopped - cycle_dict[pair][0])
				else:
					cycle_dict[pair] = (num_rocks_stopped, highest_rock)
				moving = False

if __name__ == "__main__":
	
	start_time = time.time()
	part1 = main(2022)
	print(f" Part 1 solution: {part1}")
	mid_time = time.time()
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	
	part2 = main2()
	print(f" Part 2 solution: {part2}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))