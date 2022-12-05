import re

def main1():
	with open("./input.txt", "r") as f:
		# read the input and split into the two sections
		[stacks_raw, instructions] = f.read().split('\n\n')
		stacks_split = stacks_raw.splitlines()
		num_cols = int(stacks_split[-1].split()[-1])
		
		# populate the stacks as a list of strings
		stacks = ['' for _ in range(num_cols)]
		for col in range(len(stacks_split)-1):
			for cargo in range(num_cols):
				val = stacks_split[col][4*cargo + 1 : 4*cargo + 2]
				if val != ' ':
					stacks[cargo] += val

		# find the relevant integers from the list of instructions and apply the moves
		instructions = [[int(i) for i in re.findall(r'\d+', line)] for line in instructions.splitlines()]
		for instruction in instructions:
			for x in range(instruction[0]):
				stacks[instruction[2] - 1] = stacks[instruction[1] - 1][0] + stacks[instruction[2] - 1]
				stacks[instruction[1] - 1] = stacks[instruction[1] - 1][1:]

		message = ''
		for stack in stacks:
			message += stack[0][0]
		print(message)

def main2():
	with open("./input.txt", "r") as f:
		[stacks_raw, instructions] = f.read().split('\n\n')
		stacks_split = stacks_raw.splitlines()
		num_cols = int(stacks_split[-1].split()[-1])

		stacks = ['' for _ in range(num_cols)]
		for col in range(len(stacks_split)-1):
			for cargo in range(num_cols):
				val = stacks_split[col][4*cargo + 1 : 4*cargo + 2]
				if val != ' ':
					stacks[cargo] += val

		instructions = [[int(i) for i in re.findall(r'\d+', line)] for line in instructions.splitlines()]
		for instruction in instructions:
			stacks[instruction[2] - 1] = stacks[instruction[1] - 1][:instruction[0]] + stacks[instruction[2] - 1]
			stacks[instruction[1] - 1] =  stacks[instruction[1] - 1][instruction[0]:]

		message = ''
		for stack in stacks:
			message += stack[0][0]
		print(message)

if __name__ == "__main__":
	part1 = main1()
	part2 = main2()