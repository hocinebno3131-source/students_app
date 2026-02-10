from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)

CSV_FILE = "students.csv"

# صفحة الاستمارة للطلبة
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

        with open(CSV_FILE, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(data)

        return redirect("/success")

    return render_template("form.html")


# صفحة نجاح الإرسال
@app.route("/success")
def success():
    return "<h2>تم إرسال البيانات بنجاح ✅</h2>"


# صفحة الأدمن — عرض الجدول
@app.route("/admin")
def admin():
    students = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f, delimiter=";")
            students = list(reader)

    return render_template("admin.html", students=students)


if __name__ == "__main__":
    app.run(debug=True)