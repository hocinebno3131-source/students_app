// مصفوفة لتخزين البيانات
let students = [];

// تحميل البيانات عند فتح الصفحة
function loadStudents() {
    // أولًا نجرب localStorage
    const localData = localStorage.getItem("students");
    if(localData){
        students = JSON.parse(localData);
    } else {
        // إذا لم توجد بيانات في localStorage، نحملها من students.json
        fetch('students.json')
            .then(response => response.json())
            .then(data => {
                students = data;
                // نحفظ نسخة في localStorage لتعديلها لاحقًا
                localStorage.setItem("students", JSON.stringify(students));
            });
    }
}

// استدعاء الدالة عند تحميل الصفحة
window.addEventListener("DOMContentLoaded", loadStudents);
