import os
import time

def main1():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		paths = []
		while(len(line := f.readline().strip()) != 0):
			paths.append([(int(x.split(',')[0]), int(x.split(',')[1])) for x in line.split(' -> ')])
	rocks = parse_rocks(paths)

	current_state = rocks
	infinite = False
	sand_count = 0
	while not infinite:
		iteration = release_sand(current_state, 1)
		if iteration[1] == False:
			sand_count += 1
			current_state = iteration[0]
		else:
			infinite = True
	return(sand_count)

def main2():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		y_bound = 0
		paths = []
		while(len(line := f.readline().strip()) != 0):
			paths.append([(int(x.split(',')[0]), int(x.split(',')[1])) for x in line.split(' -> ')])
	rocks = parse_rocks(paths)
	
	# Find y value of the floor
	for rock in rocks:
		if rock[1] > y_bound:
			y_bound = rock[1]
	y_bound += 2
	floor = set((x, y_bound) for x in range(500 - (y_bound + 10), 500 + (y_bound + 12)))
	rocks.update(floor)
	
	current_state = rocks
	full = False
	sand_count = 0
	while not full:
		iteration = release_sand(current_state, 2)
		if iteration[1] == False:
			sand_count += 1
			current_state = iteration[0]
		else:
			full = True
	return(sand_count + 1)

def release_sand(current_state, part):
	position = (500, 0)
	end = False
	while not end:
		# Find the next position of the sand
		new_pos = next_sand_pos(current_state, position)
		# Check if the sand moved
		if new_pos[1] == True:
			# For part 1, if the sand is above the abyss, return the state
			if part == 1 and is_doomed(current_state, new_pos[0]):
				return(current_state, True)
			# Otherwise iterate with the sand at the new position
			else:
				position = new_pos[0]
		# If the sand hasn't moved, it is at rest so update and return the current state
		else:
			if (part == 2) and (new_pos[0] == (500, 0)):
				return(current_state, True)
			else:
				sand_resting_pos = tuple(new_pos[0])
				current_state.add(sand_resting_pos)
				return(current_state, False)

def is_doomed(current_state, pos):
	for coord in current_state:
		if (pos[0] == coord[0]) and (pos[1] < coord[1]):
			return False
	return True

def next_sand_pos(current_state, coord):
	# Find next position of the sand
	has_moved = True
	if (coord[0], coord[1] + 1) not in current_state:
		position = (coord[0], coord[1] + 1)
	elif (coord[0] - 1, coord[1] + 1) not in current_state:
		position = (coord[0] - 1, coord[1] + 1)
	elif (coord[0] + 1, coord[1] + 1) not in current_state:
		position = (coord[0] + 1, coord[1] + 1)
	else:
		position = (coord[0], coord[1])
		has_moved = False
	return(position, has_moved)

def parse_rocks(paths):
	# Create set of coords that are rock
	rocks = set()
	for path in paths:
		for i in range(len(path) - 1):
			if path[i][0] == path[i + 1][0]:
				for j in range(abs(path[i][1] - abs(path[i+1][1])) + 1):
					rocks.add((path[i][0], min(path[i][1], path[i+1][1]) + j))
			elif path[i][1] == path[i + 1][1]:
				for j in range(abs(path[i][0] - abs(path[i+1][0])) + 1):
					rocks.add((min(path[i][0], path[i+1][0]) + j, path[i][1]))
	return(rocks)

if __name__ == "__main__":
	start_time = time.time()
	part1 = main1()
	print(f" Part 1 solution: {part1}")
	part2 = main2()
	print(f" Part 2 solution: {part2}")
print("Process finished --- %s seconds ---" % (time.time() - start_time))