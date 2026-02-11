from flask import Flask, render_template, request, redirect
import csv
import os
from collections import defaultdict

app = Flask(__name__)

CSV_FILE = "students.csv"
ADMIN_PASSWORD = "admin123"   # كلمة مرور الأدمن

# -------------------------
# دالة مساعدة لقراءة الطلاب
# -------------------------
def load_students():
    students = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f, delimiter=";")
            students = list(reader)
    return students

# -------------------------
# صفحة الاستمارة للطلبة
# -------------------------
@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        data = {
            "last_name": request.form["last_name"],
            "first_name": request.form["first_name"],
            "section": request.form["section"],
            "group": request.form["group"],
            "phone": request.form["phone"],
            "note": request.form["note"]
        }

        file_exists = os.path.exists(CSV_FILE)

        with open(CSV_FILE, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=data.keys(), delimiter=";")
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)

        return redirect("/success")

    # خيارات الأقسام والفوج
    sections = [f"أولى علوم{i}" for i in range(1, 8)]
    groups = ["الفوج1", "الفوج2"]

    return render_template("form.html", sections=sections, groups=groups)

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
    if request.method == "POST":
        password = request.form.get("password")
        if password != ADMIN_PASSWORD:
            return render_template("admin_login.html", message="كلمة المرور غير صحيحة ❌")

        # تصفية (اختياري)
        section_filter = request.form.get("section")
        group_filter = request.form.get("group")

        students = load_students()

        if section_filter and section_filter != "all":
            students = [s for s in students if s["section"] == section_filter]

        if group_filter and group_filter != "all":
            students = [s for s in students if s["group"] == group_filter]

        # تجميع حسب الفوج
        grouped_students = defaultdict(list)
        for s in students:
            g = s["group"]
            grouped_students[g].append(s)

        return render_template(
            "admin.html",
            grouped_students=grouped_students,
            sections=[f"أولى علوم{i}" for i in range(1,8)],
            groups=["الفوج1","الفوج2"],
            selected_section=section_filter,
            selected_group=group_filter
        )

    # GET → عرض صفحة تسجيل الدخول للأدمن
    return render_template("admin_login.html", message="")

# -------------------------
# تشغيل التطبيق
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
