import os
import time

def main(part):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	elves = set()
	with open(f"{dir_path}/input.txt", "r") as f:
		y = -1
		while(len(line := f.readline().strip()) != 0):
			y += 1
			for x, val in enumerate(line):
				if val == '#':
					elves.add((x, y))
	
	direction_index = 0
	directions = (((0,-1),(1,-1),(-1,-1)), ((0,1),(1,1),(-1,1)), ((-1,0),(-1,-1),(-1,1)), ((1,0),(1,-1),(1,1)))
	successful_proposal = {0: (0,-1), 1: (0, 1), 2: (-1, 0), 3: (1, 0)}
	moving_elves = 'placeholder'
	i = 0
	while len(moving_elves) > 0:
		i += 1
		unique_proposals = set()
		duplicate_proposals = set()
		moving_elves = {elf for elf in elves if len(elves.intersection({(elf[0] + a[0], elf[1] + a[1]) for a in {(0,-1),(1,-1),(-1,-1),(1,1),(-1,0),(-1,1),(1,0),(0,1)}})) > 0}
		for elf in moving_elves:
			possible_directions = []
			for d in range(len(directions)):
				index = (direction_index + d) % len(directions)
				choices = [choice for choice in [(elf[0] + directions[index][x][0], elf[1] + directions[index][x][1]) for x in range(len(directions[0]))] if choice not in elves]
				if len(choices) == len(directions[index]):
					possible_directions.append(index)
			if len(possible_directions) > 0:
				proposal = ((elf[0] + successful_proposal[possible_directions[0]][0], elf[1] + successful_proposal[possible_directions[0]][1]), elf)
				if proposal[0] not in duplicate_proposals:
					if proposal[0] not in {x[0] for x in unique_proposals}:
						unique_proposals.add(proposal)
					elif proposal[0] in {x[0] for x in unique_proposals}:
						duplicate_proposals.add(proposal[0])
						unique_proposals.difference_update({x for x in unique_proposals if x[0] == proposal[0]})

		for u in unique_proposals:
			elves.add(u[0])
			elves.remove(u[1])
		
		direction_index = (direction_index + 1) % len(directions)

		if part == 1 and i == 10:
			x_dims = (min([elf[0] for elf in elves]), max([elf[0] for elf in elves]))
			y_dims = (min([elf[1] for elf in elves]), max([elf[1] for elf in elves]))
			solution = (abs(x_dims[0] - x_dims[1]) + 1) * (abs(y_dims[0] - y_dims[1]) + 1) - len(elves)
			moving_elves = []

	if part == 2:
		return(i)
	else:
		return(solution)

if __name__ == "__main__":
	
	start_time = time.time()
	part1 = main(1)
	print(f" Part 1 solution: {part1}")
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	mid_time = time.time()
	part2 = main(2)
	print(f" Part 2 solution: {part2}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))
