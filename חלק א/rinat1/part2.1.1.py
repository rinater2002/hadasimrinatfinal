import os
import re

# פונקציה לבדיקה אם הקובץ קיים
def check_file_exists(filename):
    if not os.path.exists(filename):
        print(f"שגיאה: הקובץ {filename} לא נמצא.")
        return False
    print("הקובץ נקרא בהצלחה!")
    return True

# פונקציה לבדיקה אם פורמט התאריך תקין
def check_timestamp_format(lines):
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')
    invalid_dates = []
    
    for line in lines:
        parts = line.strip().split(',')
        if len(parts) < 2:
            continue  # התעלמות משורות לא תקינות
        timestamp = parts[0].strip()
        if not date_pattern.match(timestamp):
            invalid_dates.append(timestamp)
    
    if invalid_dates:
        print(f"שגיאה: נמצאו {len(invalid_dates)} תאריכים בפורמט לא תקין: {invalid_dates[:5]}")
    else:
        print("פורמט התאריכים תקין.")

# פונקציה לבדיקה אם יש כפילויות
def check_duplicates(lines):
    seen = set()
    duplicates = 0

    for line in lines:
        clean_line = line.strip()
        if clean_line in seen:
            duplicates += 1
        else:
            seen.add(clean_line)

    if duplicates > 0:
        print(f"נמצאו {duplicates} רשומות כפולות.")
    else:
        print("אין רשומות כפולות.")

# פונקציה לבדיקה אם יש ערכים חסרים
def check_missing_values(lines):
    missing_values = 0

    for line in lines:
        parts = line.strip().split(',')
        if len(parts) < 2 or not parts[1].strip():
            missing_values += 1

    if missing_values > 0:
        print(f"נמצאו {missing_values} ערכים חסרים בעמודת value.")
    else:
        print("אין ערכים חסרים.")

# פונקציה לבדיקה אם יש ערכים חריגים (לדוגמה, מספרים שליליים)
def check_anomalous_values(lines):
    invalid_values = []

    for line in lines:
        parts = line.strip().split(',')
        if len(parts) < 2:
            continue  # התעלמות משורות לא תקינות
        try:
            value = float(parts[1].strip())
            if value < 0:
                invalid_values.append(value)
        except ValueError:
            continue  # אם הערך אינו מספר

    if invalid_values:
        print(f"נמצאו {len(invalid_values)} ערכים שליליים בעמודת value.")
    else:
        print("לא נמצאו ערכים חריגים.")

# פונקציה ראשית לבדיקת הקובץ
def validate_time_series_file(filename):
    if not check_file_exists(filename):
        return  # עצירת הבדיקות אם הקובץ לא קיים

    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    check_timestamp_format(lines)
    check_duplicates(lines)
    check_missing_values(lines)
    check_anomalous_values(lines)

# קריאה לפונקציה הראשית עם שם הקובץ
validate_time_series_file("time_series.txt")
