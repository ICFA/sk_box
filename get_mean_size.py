import sys

def get_mean_size(data):
    data = [int(i.split()[4]) for i in data]
    data = sum(int(i) for i in data)/len(data)
    return data

if __name__ == '__main__':
    data = sys.stdin.readlines()[1:]
    mean_size = get_mean_size(data)
    print(round(mean_size, 2))
