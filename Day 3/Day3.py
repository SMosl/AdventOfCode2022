def main1():
	with open("./input.txt", "r") as f:
		final_sum = 0
		while(len(line := f.readline()) != 0):
			x = int(len(line)/2)
			rucksack = [line[:x], line[x:]]
			common = ord(''.join(set(rucksack[0]).intersection(rucksack[1])))
			if common < 91:
				final_sum += common - 38
			else:
				final_sum += common - 96
	print(final_sum)

def main2():
	final_sum = 0
	with open("./input.txt", "r") as f:
		content = f.read().splitlines()
	for i in range(int(len(content)/3)):
		common = ord(''.join(set(content[3*i]).intersection(content[3*i+1]).intersection(content[3*i+2])))
		if common < 91:
			final_sum += common - 38
		else:
			final_sum += common - 96		
	print(final_sum)

if __name__ == "__main__":
	part1 = main1()
	part2 = main2()
