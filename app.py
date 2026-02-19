from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
from collections import defaultdict
import os

app = Flask(__name__)

DATABASE = "database.db"
ADMIN_PASSWORD = "admin123"

# -------------------------
# الاتصال بقاعدة البيانات
# -------------------------
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# -------------------------
# قراءة كل الطلبة
# -------------------------
def read_students():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    # تحويل كل Row إلى dict عادية
    students = [dict(row) for row in rows]
    # إضافة _index لكل طالب لتسهيل الحذف
    for i, s in enumerate(students):
        s["_index"] = i
    return students

# -------------------------
# صفحة الاستمارة
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

        conn = get_db_connection()

        # منع التكرار (اللقب + الاسم + القسم)
        existing = conn.execute("""
            SELECT * FROM students
            WHERE last_name=? AND first_name=? AND section=?
        """, (last_name, first_name, class_name)).fetchone()

        if existing:
            conn.close()
            return redirect("/?duplicate=1")

        # إضافة الطالب
        conn.execute("""
            INSERT INTO students (last_name, first_name, section, group_name, phone, note)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (last_name, first_name, class_name, group, phone, note))

        conn.commit()
        conn.close()

        return redirect("/success")

    return render_template("form.html")

# -------------------------
@app.route("/success")
def success():
    return "<h2>تم إرسال البيانات بنجاح ✅</h2>"

# -------------------------
# صفحة الأدمن
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
        key = f"{s['section']} — {s['group_name']}"
        grouped[key].append(s)

    classes = sorted({s['section'] for s in students})
    groups = sorted({s['group_name'] for s in students})

    return render_template(
        "admin.html",
        grouped=grouped,
        classes=classes,
        groups=groups,
        selected_class="",
        selected_group=""
    )

# -------------------------
# حذف طالب
# -------------------------
@app.route("/delete_student", methods=["POST"])
def delete_student_ajax():
    student_id = request.form.get("id")

    conn = get_db_connection()
    conn.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    conn.close()

    return jsonify({"status": "success"})

# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
