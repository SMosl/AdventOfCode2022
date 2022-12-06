import os

get_score1 = {
	'A X' : 4,
	'A Y' : 8,
	'A Z' : 3,
	'B X' : 1,
	'B Y' : 5,
	'B Z' : 9,
	'C X' : 7,
	'C Y' : 2,
	'C Z' : 6
}

get_score2 = {
	'A X' : 3,
	'A Y' : 4,
	'A Z' : 8,
	'B X' : 1,
	'B Y' : 5,
	'B Z' : 9,
	'C X' : 2,
	'C Y' : 6,
	'C Z' : 7
}


def main1():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		score = 0
		while(len(line := f.readline()) != 0):
			score += get_score1[line[:3]]
	print(score)

def main2():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		score = 0
		while(len(line := f.readline()) != 0):
			score += get_score2[line[:3]]
	print(score)

if __name__ == "__main__":
	part1 = main1()
	part2 = main2()