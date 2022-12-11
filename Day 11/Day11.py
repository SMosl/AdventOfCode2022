import os
import re
import numpy as np

def main1():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		sections = [x.splitlines() for x in f.read().split('\n\n')]
		monkeys = {}
		inspections = [0 for _ in range(len(sections))]

		for i, monkey in enumerate(sections):
			vals = monkey[1].split()[2:]
			monkeys[i] = [int(y[0]) for y in [re.findall(r'\d+', x) for x in vals]]

		for v in range(20):
			# Each round, iterate through each monkey in order
			for u, turn in enumerate(sections):
				# Each monkey gets a turn to inspect and throw every item they currently hold
				for old in monkeys[u]:
					inspections[u] += 1
					new = eval(turn[2].split('= ')[1])
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
		print(inspections[-1] * inspections[-2])

def main2():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		sections = [x.splitlines() for x in f.read().split('\n\n')]
		monkeys = {}
		inspections = [0 for _ in range(len(sections))]
		# To prevent numbers getting too large, we will work with worry levels modulo the gcd of each monkey's test value
		gcd = np.prod([int(x[3].split('by ')[1]) for x in sections])

		for i, monkey in enumerate(sections):
			vals = monkey[1].split()[2:]
			monkeys[i] = [np.int64(y[0]) for y in [re.findall(r'\d+', x) for x in vals]]	# Now working with larger ints, there's probably a better workaround

		for v in range(10000):
			for u, turn in enumerate(sections):
				for old in monkeys[u]:
					inspections[u] += 1
					new = eval(turn[2].split('= ')[1]) % gcd
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
		print(inspections[-1] * inspections[-2])

if __name__ == "__main__":
	part1 = main1()
	part2 = main2()