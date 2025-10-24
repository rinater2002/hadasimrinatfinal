import os
import heapq
import re
from collections import Counter
from multiprocessing import Pool, cpu_count


def split_file(file_path, chunk_size=10**6):
    """פיצול קובץ הלוג לחלקים קטנים יותר."""
    part_files = []
    with open(file_path, 'r', encoding='utf-8') as file:
        part_num = 0
        while True:
            lines = file.readlines(chunk_size)
            if not lines:
                break
            part_filename = f'log_part_{part_num}.txt'
            with open(part_filename, 'w', encoding='utf-8') as part_file:
                part_file.writelines(lines)
            part_files.append(part_filename)
            part_num += 1
    return part_files


def count_errors(file_path):
    """ספירת שכיחויות של קודי השגיאה בלבד, ללא ה-Timestamp."""
    counter = Counter()
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = re.search(r"Error: (\w+)", line)
            if match:
                error_code = match.group(1)
                counter[error_code] += 1
    return counter


def merge_counts(counters):
    """חיבור ספירות השכיחות מכל התהליכים."""
    total_counter = Counter()
    for c in counters:
        total_counter.update(c)
    return total_counter


def top_n_errors(file_path, N, num_processes=None):
    """מציאת N קודי השגיאה השכיחים ביותר באמצעות multiprocessing."""
    part_files = split_file(file_path)

    # קביעת מספר התהליכים
    if num_processes is None:
        num_processes = max(1, cpu_count() - 1)

    with Pool(processes=num_processes) as pool:
        # מפעיל את הפונקציה count_errors על כל חלק במקביל
        counters = pool.map(count_errors, part_files)

    # מאחדים את כל התוצאות
    total_counts = merge_counts(counters)

    # מוחקים את הקבצים החלקיים
    for part_file in part_files:
        os.remove(part_file)

    # מוצאים את ה-N השכיחים ביותר
    return heapq.nlargest(N, total_counts.items(), key=lambda x: x[1])


if __name__ == "__main__":
    file_path = "logs.txt"
    N = 5
    result = top_n_errors(file_path, N)
    print(result)
