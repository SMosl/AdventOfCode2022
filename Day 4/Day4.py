import re

def main1():
	count = 0
	with open("./input.txt", "r") as f:
		while(len(line := f.readline()) != 0):
			#split each line into the 4 ID's, the filter removes the empty string
			sections = list(filter(None, re.split(',|-|\n',line)))
			#create sets of integers that cover the range
			section1 = {x for x in range(int(sections[0]),int(sections[1]) + 1)}
			section2 = {x for x in range(int(sections[2]),int(sections[3]) + 1)}
			#check if either section intersects fully
			if section1.intersection(section2) == section2 or section1.intersection(section2) == section1:
				count += 1
	print(count)

def main2():
	count = 0
	with open("./input.txt", "r") as f:
		while(len(line := f.readline()) != 0):

			sections = list(filter(None, re.split(',|-|\n', line)))
			section1 = {x for x in range(int(sections[0]),int(sections[1]) + 1)}
			section2 = {x for x in range(int(sections[2]),int(sections[3]) + 1)}
			#check if either intersection is non-empty
			if section1.intersection(section2) or section1.intersection(section2):
				count += 1
	print(count)

if __name__ == "__main__":
	part1 = main1()
	part2 = main2()