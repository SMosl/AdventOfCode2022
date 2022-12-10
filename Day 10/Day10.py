import os

def main1():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		X = 1
		cycle = 0
		signal_sum = 0
		strength_checks = {_ for _ in range(20, 260, 40)}
		
		while(len(line := f.readline().split()) != 0):
			if line[0] == 'noop':
				cycle += 1
				if cycle in strength_checks:
					signal_sum += cycle * X
			else:
				cycle += 1
				if cycle in strength_checks:
					signal_sum += cycle * X
				cycle += 1
				if cycle in strength_checks:
					signal_sum += cycle * X
				X += int(line[1])
		print(signal_sum)

def main2():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		X = {0,1,2}
		cycle = 0
		display = ''
		
		while(len(line := f.readline().split()) != 0):
			if line[0] == 'noop':
				cycle = (cycle + 1) % 40
				if ((cycle - 1) % 40) in X:
					display += '#'
				else:
					display += '.'
			else:
				cycle = (cycle + 1) % 40
				if ((cycle - 1) % 40) in X:
					display += '#'
				else:
					display += '.'
				cycle = (cycle + 1) % 40
				if ((cycle - 1) % 40) in X:
					display += '#'
				else:
					display += '.'
				X = {(x + int(line[1])) % 40 for x in X}
		
		print_display(display, dir_path)

def print_display(display, dir_path):
	# NOTE: last character on third line is clearly incorrect, will fix later (though let's be honest I probably won't)
	with open(f"{dir_path}/output.txt", 'w') as f:
		for i in range(6):
			for j in range(40):
				f.write(display[j + (40 * i)])
			f.write('\n')

if __name__ == "__main__":
	main1()
	main2()