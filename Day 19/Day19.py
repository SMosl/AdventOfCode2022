import os
import time
import re
import numpy as np

def parse_input():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		blueprints = {}
		while(len(line := f.readline().strip()) != 0):
			b = re.match(r'Blueprint (?P<blueprint_ID>\d+): Each ore robot costs (?P<ore_cost>\d+) ore. Each clay robot costs (?P<clay_cost>\d+) ore. Each obsidian robot costs (?P<o_ore_cost>\d+) ore and (?P<o_clay_cost>\d+) clay. Each geode robot costs (?P<g_ore_cost>\d+) ore and (?P<g_o_cost>\d+) obsidian.', line)
			blueprints[int(b['blueprint_ID'])] = {
				'ore' : {'ore' : int(b['ore_cost']), 'clay' : 0, 'obsidian' : 0},
				'clay' : {'ore' : int(b['clay_cost']), 'clay' : 0, 'obsidian' : 0},
				'obsidian' : {'ore' : int(b['o_ore_cost']), 'clay' : int(b['o_clay_cost']), 'obsidian' : 0},
				'geode' : {'ore' : int(b['g_ore_cost']), 'clay' : 0, 'obsidian' : int(b['g_o_cost'])}
			}
		return(blueprints)

def main2():
	blueprints = parse_input()
	max_geodes = []
	for i in (1,2,3):
		max_geodes.append(run_blueprint(blueprints[i], 32))

	return(np.prod(max_geodes))

def main1():
	blueprints = parse_input()
	quality_levels = []

	for i in range(1, len(blueprints)+1):
		quality_levels.append(i * run_blueprint(blueprints[i], 24))

	return(sum(quality_levels))

def run_blueprint(blueprint, part):
	num_geodes_open = 0
	max_ore = max(blueprint['ore']['ore'], blueprint['clay']['ore'], blueprint['obsidian']['ore'], blueprint['geode']['ore'])
	max_clay = blueprint['obsidian']['clay']
	max_obs = blueprint['geode']['obsidian']

	# each state is a tuple (time passed, total ore, total clay, total obsidian, total geodes, num ore r's, num clay r's, num obsidian r's, num geod r's)
	states = {(0, 0, 0, 0, 0, 1, 0, 0, 0)}

	for i in range(part):
		new_states = set()
		for cur in states:
			# prioritise building a geode robot
			if cur[1] >= blueprint['geode']['ore'] and cur[3] >= blueprint['geode']['obsidian']:
				new_states.add((i, cur[1] + cur[5] - blueprint['geode']['ore'], cur[2] + cur[6], cur[3] + cur[7] - blueprint['geode']['obsidian'], cur[4] + cur[8], cur[5], cur[6], cur[7], cur[8] + 1))
			else:
				# option to wait and not build any new robot
				new_states.add((i, cur[1] + cur[5], cur[2] + cur[6], cur[3] + cur[7], cur[4] + cur[8], cur[5], cur[6], cur[7], cur[8]))
				# build an ore robot
				if cur[1] >= blueprint['ore']['ore'] and cur[5] < max_ore:
					new_states.add((i, cur[1] + cur[5] - blueprint['ore']['ore'], cur[2] + cur[6], cur[3] + cur[7], cur[4] + cur[8], cur[5] + 1, cur[6], cur[7], cur[8]))
				# build a clay robot
				if cur[1] >= blueprint['clay']['ore'] and cur[6] < max_clay:
					new_states.add((i, cur[1] + cur[5] - blueprint['clay']['ore'], cur[2] + cur[6], cur[3] + cur[7], cur[4] + cur[8], cur[5], cur[6] + 1, cur[7], cur[8]))
				# build an obsidian robot
				if cur[1] >= blueprint['obsidian']['ore'] and cur[2] >= blueprint['obsidian']['clay'] and cur[7] < max_obs:
					new_states.add((i, cur[1] + cur[5] - blueprint['obsidian']['ore'], cur[2] + cur[6] - blueprint['obsidian']['clay'], cur[3] + cur[7], cur[4] + cur[8], cur[5], cur[6], cur[7] + 1, cur[8]))
		
		states = simplify(new_states, i, part, blueprint)

	num_geodes_open = max(x[4] for x in states)	
	return(num_geodes_open)

def simplify(states, time_passed, part, blueprint):
	simplified_states = set()
	time_left = part - time_passed
	# store (num_ore, num_clay, num_obs, num_geo, num_robots) to get rid of any states that are strictly worse
	optimal = (0,0,0,0,0)
	# if you were to build a geode or obsidian robot every turn, you would need:
	max_materials_needed = (max(time_left * blueprint['geode']['ore'], time_left * blueprint['obsidian']['ore']), time_left * blueprint['obsidian']['clay'], time_left * blueprint['geode']['obsidian'])
	# assume you want to build a robot each turn, and prioritise better robots
	for state in states:
		# If a state has more materials and more robots than the optimal state, it is the new optimal state
		if state[1] > optimal[0] and state[2] > optimal[1] and state[3] > optimal[2] and state[4] > optimal[3] and (state[5] + state[6] + state[7] + state[8] > optimal[4]):
			optimal = (state[1], state[2], state[3], state[4], state[5] + state[6] + state[7] + state[8])
			simplified_states.add((state[0], min(state[1], max_materials_needed[0]), min(state[2], max_materials_needed[1]), min(state[3], max_materials_needed[2]), state[4], state[5], state[6], state[7], state[8]))
		# If a state is strictly terrible, get rid
		elif state[1] < optimal[0] and state[2] < optimal[1] and state[3] < optimal[2] and state[4] < optimal[3] and (state[5] + state[6] + state[7] + state[8] <= optimal[4]):
			continue # consider this state E L I M I N A T E D
		else:
			# We can compress all states with more resources than necessary down to a single state
			simplified_states.add((state[0], min(state[1], max_materials_needed[0]), min(state[2], max_materials_needed[1]), min(state[3], max_materials_needed[2]), state[4], state[5], state[6], state[7], state[8]))

	return(simplified_states)

if __name__ == "__main__":
	
	start_time = time.time()
	part1 = main1()
	print(f" Part 1 solution: {part1}")
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	mid_time = time.time()
	part2 = main2()
	print(f" Part 2 solution: {part2}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))