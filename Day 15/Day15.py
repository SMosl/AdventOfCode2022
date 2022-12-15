import os
import time
import re

def main1():
	input_vals = parse_input()
	part1 = search_row(2000000, input_vals[0], input_vals[1], input_vals[2], input_vals[3])
	return(part1)

def main2():
	x = (0, 4000000)
	y = (0, 4000000)
	min_x, max_x, sensors, beacons = parse_input()
	possibilities = set()
	overlaps = set()
	checked_sensors = set()
	
	# find the set of all points 1 away from each sensors reach
	for sensor in sensors:
		s_poss = set()
		if (x[0] <= sensor[0] - sensor[2] <= x[1]) and (y[0] <= sensor[1] <= y[1]):
			s_poss.add((sensor[0] - sensor[2] - 1, sensor[1]))
		if (x[0] <= sensor[0] + sensor[2] <= x[1]) and (y[0] <= sensor[1] <= y[1]):
			s_poss.add((sensor[0] + sensor[2] + 1, sensor[1]))
		for x_range in range(max(sensor[0] - sensor[2], x[0]), min(sensor[0] + sensor[2] + 1, x[1])):
			manhattan_left = sensor[2] - abs(sensor[0] - x_range)
			if y[0] <= sensor[1] + manhattan_left + 1 <= y[1]:
				s_poss.add((x_range, sensor[1] + manhattan_left + 1))
			if y[0] <= sensor[1] - manhattan_left - 1 <= y[1]:
				s_poss.add((x_range, sensor[1] - manhattan_left - 1))
		# Want to reduce the number of points that are necessary to check
		for pos in s_poss:
			# The beacon position will be an overlap between 2 or more possible points
			if pos in possibilities:
				overlaps.add(pos)
			# If a point is on the boundary but is within reach of another sensor, there's no need to check it
			elif not visible(pos[0], pos[1], checked_sensors):
				checked_sensors.add(sensor)
				possibilities.add(pos)

	print('HOLD......')
	for point in overlaps:
		if not visible(point[0], point[1], sensors):
			return((point[0] * 4000000) + point[1])


def parse_input():
	# Reads the input file and outputs the smallest and largest possible x values (for part 1),
	# a set of sensor positions with their corresponding manhattan distances, and a set of beacon positions
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		pairs = []
		x = set()
		while(len(line := f.readline().strip()) != 0):
			parsed_line = []
			for i in [re.findall('\-?\d+', x) for x in line.split(': closest beacon is at ')]:
				parsed_line.append([int(j) for j in i])
			pairs.append(parsed_line)

	sensors = set()
	beacons = set()
	for pair in pairs:
		distance = abs(pair[0][0] - pair[1][0]) + abs(pair[0][1] - pair[1][1])
		sensors.add((pair[0][0], pair[0][1], distance))
		x = x.union({pair[0][0] - distance, pair[0][0] + distance})
		beacons.add((pair[1][0], pair[1][1]))
	min_x, max_x = min(x), max(x)
	return(min_x, max_x, sensors, beacons)

def search_row(y_val, min_x, max_x, sensors, beacons):
	# For part 1, given a row to check and the possible range of x values, counts the number of points that cannot be beacons
	count = 0
	for x_val in range(min_x, max_x):
		if visible(x_val, y_val, sensors) and ((x_val, y_val) not in beacons):
			count += 1
	return(count)

def visible(x, y, sensors):
	# If a point is within a sensor's reach, return True, else return False
	for sensor in sensors:
		if abs(sensor[0] - x) + abs(sensor[1] - y) <= sensor[2]:
			return True
	return False

if __name__ == "__main__":
	start_time = time.time()
	part1 = main1()
	print(f" Part 1 solution: {part1}")
	part2 = main2()
	print(f" Part 2 solution: {part2}")
	print("Process finished --- %s seconds ---" % (time.time() - start_time))