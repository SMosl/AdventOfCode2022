import os
import re
import numpy as np

def main(part):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		# Part 1 has 20 rounds, part 2 has 10000 rounds
		num_rounds = (9980 * (part - 1)) + 20
		
		sections = [x.splitlines() for x in f.read().split('\n\n')]
		monkeys = {}
		inspections = [0 for _ in range(len(sections))]
		
		# To prevent numbers getting too large (for part 2), we will work with worry levels modulo the lcm of each monkey's test value
		lcm = np.lcm.reduce([int(x[3].split('by ')[1]) for x in sections])
		
		# Find the worry levels of the items that each monkey initially holds
		for i, monkey in enumerate(sections):
			vals = monkey[1].split()[2:]
			monkeys[i] = [np.int64(y[0]) for y in [re.findall(r'\d+', x) for x in vals]]	# Using int64 because part 2 works with larger ints, there's probably a better workaround

		for v in range(num_rounds):
			# Each round, iterate through each monkey in order
			for u, turn in enumerate(sections):
				# Each monkey gets a turn to inspect and throw each item they currently hold
				for old in monkeys[u]:
					inspections[u] += 1
					new = eval(turn[2].split('= ')[1]) % lcm
					
					if part == 1:
						new = new//3

					test = int(turn[3].split('by ')[-1])
					if new % test == 0:
						recipient = int(turn[4].split('monkey ')[1])
						monkeys[recipient] = monkeys[recipient] + [new]
						monkeys[u] = monkeys[u][1:]
					else:
						recipient = int(turn[5].split('monkey ')[1])
						monkeys[recipient] = monkeys[recipient] + [new]
						monkeys[u] = monkeys[u][1:]
		inspections.sort()
		return(inspections[-1] * inspections[-2])

if __name__ == "__main__":
	part1 = main(1)
	part2 = main(2)
	print(f" Part 1 solution: {part1}, Part 2 solution: {part2}")
