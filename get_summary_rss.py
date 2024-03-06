units_of_info = ['Б', 'КБ', 'МБ', 'ГБ']
def convert(rss_sum):
    for i, e in enumerate(units_of_info):
        if rss_sum < 1024 ** (i + 1):
            return f'{round(rss_sum / (1024 ** i), 3)} {e}'

def get_summary_rss(ps_output_file_path: str) -> str:
    result_sum1 = 0
    result_sum2 = 0
    with open(ps_output_file_path) as output_file:
        lines = output_file.readlines()[1:]
        for line in lines:
            columns = line.split()
            result_sum1 += int(columns[4])
            result_sum2 += int(columns[5])
    return f'{convert(result_sum1)} - вирт. память, {convert(result_sum2)} - опер. память'  


if __name__ == '__main__':
    path = 'output.txt'
    summary_rss = get_summary_rss(path)
    print(summary_rss)