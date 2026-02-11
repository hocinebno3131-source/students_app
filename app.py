from flask import Flask, render_template, request, redirect
import csv
import os
from collections import defaultdict

app = Flask(__name__)

CSV_FILE = "students.csv"
ADMIN_PASSWORD = "admin123"

# -------------------------
# دالة قراءة كل الطلبة
# -------------------------
def read_students():
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f, delimiter=";"))

# -------------------------
# صفحة الاستمارة للطلبة
# -------------------------
@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":

        last_name = request.form["last_name"].strip()
        first_name = request.form["first_name"].strip()
        class_name = request.form["class"].strip()
        group = request.form["group"].strip()
        phone = request.form["phone"].strip()
        note = request.form["note"].strip()

        students = read_students()

        # ✅ منع التكرار
        for s in students:
            if (
                s["last_name"] == last_name and
                s["first_name"] == first_name and
                s["class"] == class_name and
                s["group"] == group
            ):
                return "<h3>⚠️ هذا الطالب مسجل مسبقاً</h3>"

        data = [last_name, first_name, class_name, group, phone, note]

        file_exists = os.path.exists(CSV_FILE)
        with open(CSV_FILE, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, delimiter=";")
            if not file_exists:
                writer.writerow(["last_name","first_name","class","group","phone","note"])
            writer.writerow(data)

        return redirect("/success")

    return render_template("form.html")

# -------------------------
# صفحة نجاح الإرسال
# -------------------------
@app.route("/success")
def success():
    return "<h2>تم إرسال البيانات بنجاح ✅</h2>"

# -------------------------
# صفحة الأدمن (كما هي — لم نغيرها)
# -------------------------
@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "GET":
        return render_template("admin_password.html", message="")

    password = request.form.get("password")
    if password != ADMIN_PASSWORD:
        return render_template("admin_password.html", message="كلمة المرور غير صحيحة ❌")

    students = read_students()

    grouped = defaultdict(list)
    for s in students:
        key = f"{s['class']} — {s['group']}"
        grouped[key].append(s)

    classes = sorted({s['class'] for s in students})
    groups = sorted({s['group'] for s in students})

    return render_template(
        "admin.html",
        grouped=grouped,
        classes=classes,
        groups=groups,
        selected_class="",
        selected_group=""
    )

# -------------------------
# تشغيل التطبيق
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
