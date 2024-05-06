import subprocess


def process_count(username: str) -> int:
    user_proc_count = 0

    with open('out.txt', 'w') as out_file:
        subprocess.run(['ps', '-eF'], stdout=out_file)

    with open('out.txt', 'r') as data_file:
        data_line = data_file.readlines()
        for line in data_line:
            if line.startswith(username):
                user_proc_count += 1

    return user_proc_count

def total_memory_usage(root_pid: int) -> int:
    with open('out_2.txt', 'w') as out_file:
        subprocess.run(['ps', '-eF'], stdout=out_file)

    return count_total_memory_usage(root_pid)

def count_total_memory_usage(root_pid: int) -> int:
    with open('out_2.txt', 'r') as data_file:
        data_line = data_file.readlines()

        for line in data_line[1:]:
            if int(line.split()[1]) == root_pid:
                if int(line.split()[2]) != 0:
                    ppid = int(line.split()[2])
                    return count_total_memory_usage(ppid)
                return int(line.split()[5])


if __name__ == '__main__':
    print(total_memory_usage(int(input())))