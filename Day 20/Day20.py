import os
import time

def main(part):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	sequence = []
	with open(f"{dir_path}/input.txt", "r") as f:
		while(len(line := f.readline().strip()) != 0):
			if part == 1:
				sequence.append(int(line))
			else:
				sequence.append(int(line) * 811589153)
	indices = [x for x in range(len(sequence))]

	# Part 2 repeats the mixing 10 times, Part 1 does it once
	for j in range((part * 9) - 8):
		for i in range(len(sequence)):
			# Find where i is in indices, this is the current index of the current value in the sequence
			cur_index = indices.index(i)
			# Remove this index from the list of indices
			del indices[cur_index]
			# Find the new index
			new_index = (cur_index + sequence[i]) % len(indices)	# note that it's modulo the set of indices, not the sequence (we removed an index!)
			# Add the index back to the list of indices in the correct position
			indices.insert(new_index, i)
	sequence = [sequence[x] for x in indices]

	val_0_i = sequence.index(0)
	solution = sequence[(val_0_i + 1000) % (len(indices))] + sequence[(val_0_i + 2000) % (len(indices))] + sequence[(val_0_i + 3000) % (len(indices))]
	return(solution)

if __name__ == "__main__":
	
	start_time = time.time()
	part1 = main(1)
	print(f" Part 1 solution: {part1}")
	print("Part 1 finished --- %s seconds ---" % (time.time() - start_time))
	mid_time = time.time()
	part2 = main(2)
	print(f" Part 2 solution: {part2}")
	print("Part 2 finished --- %s seconds ---" % (time.time() - mid_time))