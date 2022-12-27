import os
import time
import numpy as np
import re

def main(part):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		raw_input = f.read().split('\n\n')
		map = raw_input[0].split('\n')
		instructions = raw_input[1]

	matrix = np.zeros((len(map), max(len(line) for line in map)), str)

	for y, line in enumerate(map):
		for x, value in enumerate(line):
			if value in {'.', '#'}:
				matrix[y][x] = value
	
	directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
	visual = {(1, 0):'>', (0, 1):'v', (-1, 0):'<', (0, -1):'^'}

	instructions = re.findall(r'\d+|\D+',instructions)
	position = ((min(np.min(np.where(matrix[0] == '.')), np.min(np.where(matrix[0] == '#'))),0),(1,0))
	path = [[position[0][0], position[0][1], visual[position[1]]]]

	p = position[0]
	d = position[1]
	for instruction in instructions:
		if instruction == 'R':
			d = directions[(directions.index(d) + 1) % len(directions)]
			path[-1] = [path[-1][0], path[-1][1], visual[d]]
		elif instruction == 'L':
			d = directions[(directions.index(d) - 1) % len(directions)]
			path[-1] = [path[-1][0], path[-1][1], visual[d]]
		else:
			p, path, d = travel(matrix, instruction, path, d, p, visual, part)

	for point in path:
		matrix[point[1]][point[0]] = point[2]

	return(1000*(p[1]+1) + 4*(p[0]+1) + directions.index(d))

def travel(matrix, instruction, path, d, p, visual, part):
	blocked = False
	for i in range(int(instruction)):
		if blocked == False:
			next_space = (p[0] + d[0], p[1] + d[1])
			if (next_space[1] > len(matrix) - 1) or (next_space[1] < 0) or (next_space[0] > len(matrix[0]) - 1) or (next_space[0] < 0):
				if part == 2:
					p, d, path, blocked = we_wrap2(matrix, p, d, path, visual)
				else:
					p, d, path, blocked = we_wrap(matrix, p, d, path, visual)
			elif matrix[next_space[1]][next_space[0]] == '':
				if part == 2:
					p, d, path, blocked = we_wrap2(matrix, p, d, path, visual)
				else:
					p, d, path, blocked = we_wrap(matrix, p, d, path, visual)
			elif matrix[next_space[1]][next_space[0]] == '.':
				p = next_space
				path.append(list(p) + [visual[d]])
			elif matrix[next_space[1]][next_space[0]] == '#':
				blocked = True
	return(p, path, d)

def we_wrap(matrix, p, d, path, visual):
	blocked = False
	if d == (1, 0):
		x_val = next(x for x in range(len(matrix[p[1]])) if matrix[p[1]][x] == '.' or matrix[p[1]][x] == '#')
		if matrix[p[1]][x_val] == '#':
			blocked = True
		else:
			p = (x_val, p[1])
			path.append(list(p) + [visual[d]])
	elif d == (0, 1):
		y_val = next(y for y in range(len(matrix)) if matrix[y][p[0]] == '.' or matrix[y][p[0]] == '#')
		if matrix[y_val][p[0]] == '#':
			blocked = True
		else:
			p = (p[0], y_val)
			path.append(list(p) + [visual[d]])
	elif d == (-1, 0):
		x_val = max([x for x in range(len(matrix[p[1]])) if matrix[p[1]][x] == '.' or matrix[p[1]][x] == '#'])
		if matrix[p[1]][x_val] == '#':
			blocked = True
		else:
			p = (x_val, p[1])
			path.append(list(p) + [visual[d]])
	elif d == (0, -1):
		y_val = max([y for y in range(len(matrix)) if matrix[y][p[0]] == '.' or matrix[y][p[0]] == '#'])
		if matrix[y_val][p[0]] == '#':
			blocked = True
		else:
			p = (p[0], y_val)
			path.append(list(p) + [visual[d]])

	return(p, d, path, blocked)

def we_wrap2(matrix, p, d, path, visual):
	blocked = False
	if d == (1, 0):
		if 0 <= p[1] < 50:
			y_val = 149 - p[1]
			x_val = 99
			if matrix[y_val][x_val] == '#':
				blocked = True
			else:
				p = (x_val, y_val)
				d = (-1, 0)
				path.append(list(p) + [visual[d]])
		elif 50 <= p[1] < 100:
			y_val = 49
			x_val = p[1] + 50
			if matrix[y_val][x_val] == '#':
				blocked = True
			else:
				p = (x_val, y_val)
				d = (0, -1)
				path.append(list(p) + [visual[d]])
		elif 100 <= p[1] < 150:
			y_val = 149 - p[1]
			x_val = 149
			if matrix[y_val][x_val] == '#':
				blocked = True
			else:
				p = (x_val, y_val)
				d = (-1, 0)
				path.append(list(p) + [visual[d]])
		elif 150 <= p[1] < 200:
			y_val = 149
			x_val = p[1] - 100
			if matrix[y_val][x_val] == '#':
				blocked = True
			else:
				p = (x_val, y_val)
				d = (0, -1)
				path.append(list(p) + [visual[d]])
	elif d == (0, 1):
		if 0 <= p[0] < 50:
			y_val = 0
			x_val = p[0] + 100
			if matrix[y_val][x_val] == '#':
				blocked = True
			else:
				p = (x_val, y_val)
				d = (0, 1)
				path.append(list(p) + [visual[d]])
		elif 50 <= p[0] < 100:
			y_val = 100 + p[0]
			x_val = 49
			if matrix[y_val][x_val] == '#':
				blocked = True
			else:
				p = (x_val, y_val)
				d = (-1, 0)
				path.append(list(p) + [visual[d]])
		elif 100 <= p[0] < 150:
			y_val = p[0] - 50
			x_val = 99
			if matrix[y_val][x_val] == '#':
				blocked = True
			else:
				p = (x_val, y_val)
				d = (-1, 0)
				path.append(list(p) + [visual[d]])
	elif d == (0, -1):
		if 0 <= p[0] < 50:
			y_val = 50 + p[0]
			x_val = 50
			if matrix[y_val][x_val] == '#':
				blocked = True
			else:
				p = (x_val, y_val)
				d = (1, 0)
				path.append(list(p) + [visual[d]])
		elif 50 <= p[0] < 100:
			y_val = p[0] + 100
			x_val = 0
			if matrix[y_val][x_val] == '#':
				blocked = True
			else:
				p = (x_val, y_val)
				d = (1, 0)
				path.append(list(p) + [visual[d]])
		elif 100 <= p[0] < 150:
			y_val = 199
			x_val = p[0] - 100
			if matrix[y_val][x_val] == '#':
				blocked = True
			else:
				p = (x_val, y_val)
				d = (0, -1)
				path.append(list(p) + [visual[d]])
	elif d == (-1, 0):
		if 0 <= p[1] < 50:
			y_val = 149 - p[1]
			x_val = 0
			if matrix[y_val][x_val] == '#':
				blocked = True
			else:
				p = (x_val, y_val)
				d = (1, 0)
				path.append(list(p) + [visual[d]])
		elif 50 <= p[1] < 100:
			y_val = 100
			x_val = p[1] - 50
			if matrix[y_val][x_val] == '#':
				blocked = True
			else:
				p = (x_val, y_val)
				d = (0, 1)
				path.append(list(p) + [visual[d]])
		elif 100 <= p[1] < 150:
			y_val = 149 - p[1]
			x_val = 50
			if matrix[y_val][x_val] == '#':
				blocked = True
			else:
				p = (x_val, y_val)
				d = (1, 0)
				path.append(list(p) + [visual[d]])
		elif 150 <= p[1] < 200:
			y_val = 0
			x_val = p[1] - 100
			if matrix[y_val][x_val] == '#':
				blocked = True
			else:
				p = (x_val, y_val)
				d = (0, 1)
				path.append(list(p) + [visual[d]])

	return(p, d, path, blocked)

if __name__ == "__main__":

	start_time = time.time()
	part1 = main(1)
	print(f" Part 1 solution: {part1}")
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	mid_time = time.time()
	part2 = main(2)
	print(f" Part 2 solution: {part2}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))
