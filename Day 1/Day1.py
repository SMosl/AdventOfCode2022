import os

def main1():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		content = f.read().split('\n\n')

	cals = []
	for elf in content:
		cals.append(sum([int(x) for x in elf.split('\n')]))
	max_cals = max(cals)

	return(max_cals,cals)


def main2(cals):
	sorted_list = sorted(cals, reverse=True)
	return(sum([x for x in sorted_list[:3]]))


if __name__ == "__main__":
	part1 = main1()
	print(part1[0])

	part2 = main2(part1[1])
	print(part2)
