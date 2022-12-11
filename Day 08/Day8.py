import os
import numpy as np

def main1():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		content = f.read().splitlines()
		# Record the maximum values for each of the four directions, this starts as the heights of trees on the perimeter
		u_max = content[0]
		d_max = content[-1]
		l_max = ''.join([x[0] for x in content])
		r_max = ''.join([x[-1] for x in content])
		# Create a list of trees that are visible, this begins populated by trees on the perimeter
		visible_indices = ([[0, x] for x in range(len(content[0]))] +
			[[len(content) - 1, x] for x in range(len(content[0]))] +
			[[x, 0] for x in range(1, len(content) - 1)] +
			[[x, len(content[0]) - 1] for x in range(1, len(content) - 1)])

		# Find all trees that are visible from above
		for y, row in enumerate(content):
			for x, col in enumerate(row):
				if col > u_max[x]:
					u_max = u_max[:x] + col + u_max[x + 1:]
					if [y,x] not in visible_indices:
						visible_indices.append([y,x])

		# Find all remaining trees that are visible from left
		for y, row in enumerate(content):
			for x, col in enumerate(row):
				if col > l_max[y]:
					l_max = l_max[:y] + col + l_max[y + 1:]
					if [y,x] not in visible_indices:
						visible_indices.append([y,x])

		# Find all remaining trees that are visible from right
		for y, row in enumerate(content):
			for x, col in enumerate(row[::-1]):
				if col > r_max[y]:
					r_max = r_max[:y] + col + r_max[y + 1:]
					if [y,(len(content[0]) - 1) - x] not in visible_indices:
						visible_indices.append([y, (len(content[0]) - 1) - x])

		# Find all remaining trees that are visible from below
		for y, row in enumerate(content[::-1]):
			for x, col in enumerate(row):
				if (col > d_max[x]):
					d_max = d_max[:x] + col + d_max[x + 1:]
					if [(len(content) - 1) - y, x] not in visible_indices:
						visible_indices.append([(len(content) - 1) - y, x])

		print(len(visible_indices))

def main2():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(f"{dir_path}/input.txt", "r") as f:
		content = f.read().splitlines()
		
		directions = [[0,-1],[0,1],[-1,0],[1,0]]
		max_score = 0

		for y, row in enumerate(content):
			for x, col in enumerate(row):
				score = [0 for _ in range(len(directions))]
				for s, direction in enumerate(directions):
					next_coord = [y + direction[0], x + direction[1]]
					while next_coord[0] in range(len(content)) and next_coord[1] in range(len(content[0])):
						next_val = content[next_coord[0]][next_coord[1]]
						if next_val >= col:
							score[s] += 1
							break
						else:
							score[s] += 1
							next_coord = [next_coord[0] + direction[0], next_coord[1] + direction[1]]
				tot_score = np.prod(score)
				if tot_score > max_score:
					max_score = tot_score
		print(max_score)

if __name__ == "__main__":
	main1()
	main2()
