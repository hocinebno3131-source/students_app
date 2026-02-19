import sqlite3
import csv

# الاتصال بقاعدة البيانات (سيتم إنشاؤها إذا لم تكن موجودة)
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# إنشاء جدول الطلاب
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    last_name TEXT,
    first_name TEXT,
    section TEXT,
    group_name TEXT,
    phone TEXT
)
""")

# فتح ملف CSV
with open("students.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # لتجاوز أول سطر (العناوين)

    for row in reader:
        cursor.execute("""
        INSERT INTO students (last_name, first_name, section, group_name, phone)
        VALUES (?, ?, ?, ?, ?)
        """, row)

# حفظ التغييرات
conn.commit()
conn.close()

print("✅ تم تحويل البيانات إلى SQLite بنجاح!")