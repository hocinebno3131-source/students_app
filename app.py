from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)

CSV_FILE = "students.csv"

# -------------------------------
# صفحة الاستمارة للطلبة
# -------------------------------
@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        data = [
            request.form["last_name"],
            request.form["first_name"],
            request.form["class"],
            request.form["group"],
            request.form["phone"],
            request.form["note"]
        ]

        # تحقق إذا كان الملف موجود أو أضف رأس الأعمدة إذا جديد
        file_exists = os.path.exists(CSV_FILE)
        with open(CSV_FILE, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, delimiter=";")
            if not file_exists:
                writer.writerow(["last_name", "first_name", "class", "group", "phone", "note"])
            writer.writerow(data)

        return redirect("/success")

    return render_template("form.html")


# -------------------------------
# صفحة نجاح الإرسال
# -------------------------------
@app.route("/success")
def success():
    return "<h2>تم إرسال البيانات بنجاح ✅</h2>"


# -------------------------------
# صفحة الأدمن — عرض الجدول مع فلتر
# -------------------------------
@app.route("/admin")
def admin():
    students = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f, delimiter=";")
            students = list(reader)

    # الحصول على قائمة الأقسام والفوجات الموجودة
    classes = sorted({s['class'] for s in students})
    groups = sorted({s['group'] for s in students})

    # قراءة الفلتر من الرابط
    selected_class = request.args.get('class')
    selected_group = request.args.get('group')

    # فلترة الطلاب حسب الاختيار
    filtered_students = students
    if selected_class:
        filtered_students = [s for s in filtered_students if s['class'] == selected_class]
    if selected_group:
        filtered_students = [s for s in filtered_students if s['group'] == selected_group]

    # تجميع حسب الفوج والقسم بعد الفلترة
    grouped_students = {}
    for student in filtered_students:
        key = f"{student['class']} - {student['group']}"
        if key not in grouped_students:
            grouped_students[key] = []
        grouped_students[key].append(student)

    return render_template(
        "admin.html",
        grouped_students=grouped_students,
        classes=classes,
        groups=groups,
        selected_class=selected_class,
        selected_group=selected_group
    )


# -------------------------------
# تشغيل التطبيق
# -------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
