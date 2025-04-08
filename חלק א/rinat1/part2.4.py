import pandas as pd

import os
import math

def split_file(file_path):
    """פיצול קובץ הלוג לחלקים קטנים יותר."""
    part_files = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        part_num = 0
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 2:
                time_parts = parts[0].strip().split(' ')
                if len(time_parts) == 2:
                    """ החלק של התאריך """
                    formated_date = '_'.join(time_parts[0].split('/'))
                    part_filename = f'log_part_{formated_date}.txt'
                    part_files.add(part_filename)
                    with open(part_filename, 'a+', encoding='utf-8') as part_file:
                        part_file.write(line)
    return part_files

def count_values(file_path, hourly_data):
    """ספירת שכיחויות של קודי השגיאה בלבד, ללא ה-Timestamp."""
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 2:
                time_parts = parts[0].strip().split(' ')
                if len(time_parts) == 2:
                    """ החלק של השעה """
                    date_parts = time_parts[1].split(':')
                    if len(date_parts) == 2:
                        try:
                            hour = int(date_parts[0])
                            value = float(parts[1].strip())
                            """ דלג על מה שלא מספר """
                            if math.isnan(value):
                                continue
                            lst = hourly_data.get(hour, [])
                            lst.append(value)
                            hourly_data[hour] = lst
                        except ValueError:
                            continue  # אם הערך אינו מספר

def merge_counts(part_files, hourly_data):
    """חיבור ספירות השכיחות מכל החלקים."""
    for part_file in part_files:
        count_values(part_file, hourly_data)
        os.remove(part_file)  # מחיקת הקובץ החלקי לאחר עיבודו

def convert_to_avgs(hourly_data):
    for key, value in hourly_data.items():
        """ חשב את הממוצעים """
        if sum(value):
            hourly_data[key] = sum(value) / len(value)
        else:
            hourly_data[key] = 0

def split_parquet_file(file_path):
    """פיצול קובץ הלוג לחלקים קטנים יותר."""
    part_files = set()
    """Reads a Parquet file and prints each row as a string."""
    try:
        df = pd.read_parquet(file_path)
        for _, row in df.iterrows():
            line = row.to_string()
            line_parts = line.split('\n');
            timestamp = None
            hour = None
            value = None
            for line_part in line_parts:
                sub_parts = line_part.split()
                if len(sub_parts) == 3 and sub_parts[0] == 'timestamp':
                    timestamp = sub_parts[1]
                    hour = int(sub_parts[2].split(':')[0])
                elif len(sub_parts) == 2 and sub_parts[0] == 'mean_value':
                    value = float(sub_parts[1])
            if timestamp and hour and value:
                formated_date = '_'.join(timestamp.split('-'))
                part_filename = f'log_part_{formated_date}.txt'
                part_files.add(part_filename)
                timestamp = '/'.join(timestamp.split('-'))
                with open(part_filename, 'a+', encoding='utf-8') as part_file:
                    part_file.write(timestamp + ' ' + str(hour) + ':00,' + str(value) + '\n')
    except Exception as e:
        print(f"Error reading parquet file: {e}")
    return part_files

# כתיבת הקובץ
def write_results(hourly_data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for key, value in hourly_data.items():
            file.write(str(key) + ' ' + str(value) + '\n')

if __name__ == "__main__":
    """ לשים כאן קובץ csv או קובץ parquet """
    file_path = "time_series.parquet"  # שם הקובץ
    #file_path = "time_series.csv"  # שם הקובץ
    file_path_parts = file_path.split('.')
    part_files = []
    if file_path_parts[1] == 'csv':
        part_files = split_file(file_path)
    elif file_path_parts[1] == 'parquet':
        part_files = split_parquet_file(file_path)

    # מילון לאגירת הנתונים לפי שעה
    hourly_data = {}
    merge_counts(part_files, hourly_data)
    convert_to_avgs(hourly_data)
    write_results(hourly_data, file_path + ".txt")

