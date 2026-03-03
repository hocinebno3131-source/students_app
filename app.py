from flask import Flask, render_template, request, redirect, jsonify
import csv
import os
from collections import defaultdict

app = Flask(__name__)

CSV_FILE = "students.csv"
ADMIN_PASSWORD = "admin123"

# -------------------------
# قراءة كل الطلبة
# -------------------------
def read_students():
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f, delimiter=";"))

# -------------------------
# إعادة كتابة الملف بعد التعديل أو الحذف
# -------------------------
def write_students(students):
    with open(CSV_FILE, "w", newline="", encoding="utf-8-sig") as f:
        fieldnames = ["last_name","first_name","class","group","phone","note"]
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(students)

# -------------------------
# صفحة الاستمارة + منع التكرار
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

        # منع التكرار
        for s in students:
            if (
                s["last_name"] == last_name and
                s["first_name"] == first_name and
                s["class"] == class_name and
                s["group"] == group
            ):
                return redirect("/?duplicate=1")

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
@app.route("/success")
def success():
    return render_template("success.html")

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

    # نضيف index لكل طالب (مهم للحذف والتعديل)
    for i, s in enumerate(students):
        s["_index"] = i
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
# مسار حذف طالب عبر POST
# -------------------------
@app.route("/delete_student", methods=["POST"])
def delete_student_post():
    index = request.form.get("index")
    if index is None:
        return jsonify({"status": "error", "message": "لم يتم تحديد الطالب"})
    
    try:
        index = int(index)
    except ValueError:
        return jsonify({"status": "error", "message": "رقم غير صالح"})

    students = read_students()
    if 0 <= index < len(students):
        students.pop(index)
        write_students(students)
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error", "message": "الطالب غير موجود"})

# -------------------------
# مسار تعديل طالب عبر POST
# -------------------------
@app.route("/edit_student", methods=["POST"])
def edit_student():
    try:
        index = int(request.form.get("index"))
        last_name = request.form.get("last_name").strip()
        first_name = request.form.get("first_name").strip()
        class_name = request.form.get("class").strip()
        group = request.form.get("group").strip()
        phone = request.form.get("phone").strip()
        note = request.form.get("note").strip()
    except:
        return jsonify({"status":"error", "message":"بيانات غير صحيحة"})

    students = read_students()
    if 0 <= index < len(students):
        students[index]["last_name"] = last_name
        students[index]["first_name"] = first_name
        students[index]["class"] = class_name
        students[index]["group"] = group
        students[index]["phone"] = phone
        students[index]["note"] = note

        write_students(students)
        return jsonify({"status":"success"})
    else:
        return jsonify({"status":"error", "message":"الطالب غير موجود"})

# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
