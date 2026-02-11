from flask import Flask, render_template, request, redirect
import csv
import os
from collections import defaultdict

app = Flask(__name__)

CSV_FILE = "students.csv"
ADMIN_PASSWORD = "admin123"

# -------------------------
# صفحة الاستمارة للطلبة
# -------------------------
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
# صفحة الأدمن المحمية مع فلاتر
# -------------------------
@app.route("/admin", methods=["GET", "POST"])
def admin():

    # عرض نموذج كلمة المرور أولاً
    if request.method == "GET":
        return render_template("admin_password.html", message="")

    # التحقق من كلمة المرور
    password = request.form.get("password")
    if password != ADMIN_PASSWORD:
        return render_template("admin_password.html", message="كلمة المرور غير صحيحة ❌")

    # ===== كلمة المرور صحيحة → عرض الجداول =====
    students = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f, delimiter=";")
            students = list(reader)

    # الحصول على الفلاتر من POST
    selected_class = request.form.get("filter_class", "all")
    selected_group = request.form.get("filter_group", "all")

    # تقسيم حسب القسم + الفوج
    grouped = defaultdict(list)
    for s in students:
        if (selected_class == "all" or s["class"] == selected_class) and \
           (selected_group == "all" or s["group"] == selected_group):
            key = f"{s['class']} — {s['group']}"
            grouped[key].append(s)

    classes = sorted({s['class'] for s in students})
    groups = sorted({s['group'] for s in students})

    return render_template(
        "admin.html",
        grouped=grouped,              # ← الاسم مطابق للقالب
        classes=classes,
        groups=groups,
        selected_class=selected_class,
        selected_group=selected_group
    )

# -------------------------
# تشغيل التطبيق
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
