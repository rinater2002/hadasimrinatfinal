import os
import heapq
import re
from collections import Counter

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
            match = re.search(r"Error: (\w+)", line)  # חיפוש קוד השגיאה
            if match:
                error_code = match.group(1)  # חילוץ קוד השגיאה
                counter[error_code] += 1
    return counter

def merge_counts(part_files):
    """חיבור ספירות השכיחות מכל החלקים."""
    total_counter = Counter()
    for part_file in part_files:
        total_counter.update(count_errors(part_file))
        os.remove(part_file)  # מחיקת הקובץ החלקי לאחר עיבודו
    return total_counter

def top_n_errors(file_path, N):
    """מציאת N קודי השגיאה השכיחים ביותר, החזרת רשימה בלבד."""
    part_files = split_file(file_path)
    total_counts = merge_counts(part_files)
    return heapq.nlargest(N, total_counts.items(), key=lambda x: x[1])

# דוגמה לשימוש
if __name__ == "__main__":
    file_path = "logs.txt"  # שם הקובץ
    N = 5  # מספר קודי השגיאה השכיחים ביותר
    result = top_n_errors(file_path, N)
    print(result)  # הצגת הפלט בפורמט רשימה בלבד
