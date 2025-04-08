# import datetime
# from collections import defaultdict

# # קריאת הקובץ
# filename = "time_series.txt"

# # מילון לאחסון הסכומים והכמויות לפי שעה
# hourly_data = defaultdict(lambda: {"sum": 0, "count": 0})

# with open(filename, "r", encoding="utf-8") as file:
#     for line in file:
#         parts = line.strip().split(",")  
#         if len(parts) != 2:
#             continue  # התעלמות משורות לא תקינות

#         timestamp_str, value_str = parts
#         try:
#             # המרת חותמת זמן לפורמט datetime
#             timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
#             value = float(value_str)  

#             # יצירת מפתח לפי שעה
#             hour_key = timestamp.replace(minute=0, second=0)

#             # הוספת הערך למילון
#             hourly_data[hour_key]["sum"] += value
#             hourly_data[hour_key]["count"] += 1
#         except ValueError:
#             continue  # התעלמות משגיאות המרה

# # חישוב הממוצעים
# print("זמן התחלה       | ממוצע")
# print("-" * 25)
# for hour, data in sorted(hourly_data.items()):
#     avg = data["sum"] / data["count"]
#     print(f"{hour} | {avg:.1f}")


# from datetime import datetime
# from collections import defaultdict

# # קריאת הנתונים מהקובץ
# file_path = "time_series.txt"

# data = []
# with open(file_path, "r") as file:
#     for line in file:
#         parts = line.strip().split(",")  # בהנחה שכל שורה מכילה timestamp, value
#         if len(parts) != 2:
#             continue  # דילוג על שורות לא תקינות
#         timestamp_str, value_str = parts
#         try:
#             timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
#             value = float(value_str)
#             data.append((timestamp, value))
#         except ValueError:
#             continue  # דילוג על שורות עם נתונים שגויים

# # חישוב ממוצע לכל שעה
# hourly_data = defaultdict(list)

# for timestamp, value in data:
#     hour_key = timestamp.replace(minute=0, second=0)  # מעגלים לשעה הקרובה
#     hourly_data[hour_key].append(value)

# # חישוב ממוצע לערכים בכל שעה
# hourly_averages = {hour: sum(values) / len(values) for hour, values in hourly_data.items()}

# # הדפסת טבלה באופן ידני
# print("\n+---------------------+---------+")
# print("|   זמן התחלה        |  ממוצע  |")
# print("+---------------------+---------+")
# for hour, avg in sorted(hourly_averages.items()):
#     print(f"| {hour} |  {avg:.1f}   |")
# print("+---------------------+---------+")




# from datetime import datetime
# from collections import defaultdict

# # קריאת הנתונים מהקובץ
# file_path = "time_series.txt"

# # מילון לשמירת הערכים לפי השעה
# hourly_data = defaultdict(list)

# with open(file_path, "r") as file:
#     for line in file:
#         parts = line.strip().split(",")  # בהנחה שכל שורה מכילה timestamp, value
#         if len(parts) != 2:
#             continue  # דילוג על שורות לא תקינות
#         timestamp_str, value_str = parts
#         try:
#             timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
#             value = float(value_str)
#             hour_key = timestamp.replace(minute=0, second=0)  # מעגלים לשעה הקרובה
#             hourly_data[hour_key].append(value)
#         except ValueError:
#             continue  # דילוג על שורות עם נתונים שגויים

# # חישוב ממוצע לכל שעה שמופיעה בקובץ
# hourly_averages = {hour: sum(values) / len(values) for hour, values in hourly_data.items()}

# # הדפסת התוצאה בצורה מסודרת
# print("\n+---------------------+---------+")
# print("|   זמן התחלה        |  ממוצע  |")
# print("+---------------------+---------+")
# for hour, avg in sorted(hourly_averages.items()):
#     print(f"| {hour} |  {avg:.2f}   |")
# print("+---------------------+---------+")


from collections import defaultdict
import math

# נתיב לקובץ
file_path = "time_series.txt"

# מילון לאגירת הנתונים לפי שעה
hourly_data = defaultdict(list)

# קריאת הנתונים מהקובץ
with open(file_path, "r", encoding="utf-8") as file:
    next(file)  # דילוג על שורת הכותרת
    for line in file:
        parts = line.strip().split()  # חלוקה לפי רווחים
        if len(parts) != 3:
            continue  # דילוג על שורות לא תקינות

        date, time, value = parts
        hour = time.split(":")[0]  # חילוץ השעה בלבד
        try:
            value = float(value)  # המרה למספר
            """ דלג על מה שלא מספר """
            if math.isnan(value):
                continue
            hourly_data[hour].append(value)
        except ValueError:
            continue  # דילוג על שגיאות המרה

# חישוב ממוצע לכל שעה
averages = {hour: sum(values) / len(values) for hour, values in hourly_data.items()}

# הצגת הפלט בטבלה
print(f"{'זמן התחלה':<15}{'ממוצע'}")
print("-" * 25)
for hour in sorted(averages.keys(), key=int):  # מיון השעות לפי סדר עולה
    print(f"{hour}:00{' ' * 5}{averages[hour]:.2f}")
