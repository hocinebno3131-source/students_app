from flask import Flask, render_template, request, redirect
import csv
import os
from collections import defaultdict

app = Flask(__name__)

CSV_FILE = "students.csv"
ADMIN_PASSWORD = "admin123"   # يمكنك تغييرها

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
                writer.writerow([
                    "last_name","first_name","class","group","phone","note"
                ])

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
# صفحة الأدمن المحمية
# -------------------------
@app.route("/admin", methods=["GET", "POST"])
def admin():

    # عرض صفحة كلمة المرور
    if request.method == "GET":
        return render_template("admin_password.html", message="")

    password = request.form.get("password")

    if password != ADMIN_PASSWORD:
        return render_template(
            "admin_password.html",
            message="كلمة المرور غير صحيحة ❌"
        )

    # ===== بعد نجاح كلمة المرور =====

    students = []

    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f, delimiter=";")
            for row in reader:
                students.append(row)

    # تقسيم حسب القسم + الفوج بشكل آمن
    grouped = defaultdict(list)

    for s in students:
        cls = s.get("class", "غير محدد")
        grp = s.get("group", "غير محدد")
        key = f"{cls} — {grp}"
        grouped[key].append(s)

    # قوائم الفلترة بشكل آمن
    classes = sorted({
        s.get("class") for s in students if s.get("class")
    })

    groups = sorted({
        s.get("group") for s in students if s.get("group")
    })

    return render_template(
        "admin.html",
        grouped=grouped,
        classes=classes,
        groups=groups
    )


# -------------------------
# تشغيل التطبيق
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
