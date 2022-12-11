import os

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(f"{dir_path}/input.txt", "r") as f:
        content = f.read().splitlines()
        sizes = {'/' : 0}
        dirs = {'/' : []}
        visited_files = []

        for line in content:
            current_command = line.split()
            if current_command[0] == '$' and current_command[1] == 'cd':
                if current_command[2] == '/':
                    path = ['']
                elif current_command[2] == '..':
                    path.pop()
                else:
                    path.append(current_command[2])
                
            elif current_command[0] == 'dir':
                if path == ['']:
                    dir_str = '/' + current_command[1]
                    if dir_str not in dirs:
                        sizes[dir_str] = 0
                        dirs[dir_str] = []
                else:
                    dir_str = '/'.join(path) + '/' + current_command[1]
                    if dir_str not in dirs:
                        sizes[dir_str] = 0
                        dirs[dir_str] = []

            elif current_command[0].isnumeric():
                if path == ['']:
                    dir_str = '/' + current_command[1]
                    if dir_str not in visited_files:
                        visited_files.append(dir_str)
                        sizes['/'] += int(current_command[0])
                else:
                    dir_str = '/'.join(path) + '/' + current_command[1]
                    if dir_str not in visited_files:
                        visited_files.append(dir_str)
                        sizes['/'] += int(current_command[0])
                        partial_path = ''
                        for i in range(1, len(path)):
                            partial_path = partial_path + '/' + path[i]
                            sizes[partial_path] += int(current_command[0])
        return(sizes)

def part1():
    sizes = main()
    tot_size = 0
    for size in sizes:
        if sizes[size] <= 100000:
            tot_size += sizes[size]
    print(tot_size)

def part2():
    sizes = main()
    poss_del = []
    required_space = 30000000 - (70000000 - sizes['/'])
    for directory in sizes:
        if sizes[directory] > required_space:
            poss_del.append(sizes[directory])
    print(min(poss_del))

if __name__ == "__main__":
    part1()
    part2()
