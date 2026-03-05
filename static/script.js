window.addEventListener("DOMContentLoaded", () => {
const urlParams = new URLSearchParams(window.location.search);
if (urlParams.get("duplicate") === "1") {
document.getElementById("duplicateModal").style.display = "flex";
}
});

function closeDuplicateModal() {
document.getElementById("duplicateModal").style.display = "none";
}

let currentEditing = null;
let currentIndex = null;

// -------------------------
// تعديل صف
// -------------------------
function editRow(index) {

```
if(currentEditing !== null) return;

const row = document.getElementById("row-" + index);
const cells = row.querySelectorAll("td");

row.classList.add("editing-row");
currentEditing = index;

cells.forEach((cell, i) => {

    if(i === 2){ // class

        const value = cell.innerText;
        const options = [{% for c in classes %}'{{ c }}',{% endfor %}];

        let select = `<select>`;

        options.forEach(opt=>{
            select += `<option value="${opt}" ${opt===value?'selected':''}>${opt}</option>`;
        });

        select += `</select>`;

        cell.innerHTML = select;
    }

    else if(i === 3){ // group

        const value = cell.innerText;
        const options = [{% for g in groups %}'{{ g }}',{% endfor %}];

        let select = `<select>`;

        options.forEach(opt=>{
            select += `<option value="${opt}" ${opt===value?'selected':''}>${opt}</option>`;
        });

        select += `</select>`;

        cell.innerHTML = select;
    }

    else if(i < cells.length-1){

        const text = cell.innerText;

        cell.innerHTML = `<input type="text" value="${text}" style="width:100%">`;
    }

});

toggleButtons(row,true);
```

}

// -------------------------
// الغاء التعديل
// -------------------------
function cancelEdit(index){

```
const row = document.getElementById("row-"+index);
const cells = row.querySelectorAll("td");
const inputs = row.querySelectorAll("input,select");

inputs.forEach((input,i)=>{

    if(input.tagName === "SELECT"){
        cells[i].innerText = input.value;
    }
    else{
        cells[i].innerText = input.defaultValue;
    }

});

row.classList.remove("editing-row");

toggleButtons(row,false);

currentEditing = null;
```

}

// -------------------------
// تبديل الازرار
// -------------------------
function toggleButtons(row,editing){

```
const editBtn = row.querySelector(".edit-btn");
const deleteBtn = row.querySelector(".delete-btn");
const saveBtn = row.querySelector(".save-btn");
const cancelBtn = row.querySelector(".cancel-btn");

if(editing){
    editBtn.style.display="none";
    deleteBtn.style.display="none";
    saveBtn.style.display="inline-block";
    cancelBtn.style.display="inline-block";
}
else{
    editBtn.style.display="inline-block";
    deleteBtn.style.display="inline-block";
    saveBtn.style.display="none";
    cancelBtn.style.display="none";
}
```

}

// -------------------------
// تحقق العربية
// -------------------------
function isArabic(text){
return /^[\u0600-\u06FF0-9\s]+$/.test(text);
}

// -------------------------
// حفظ التعديل
// -------------------------
function saveRow(index){

```
const row = document.getElementById("row-"+index);
const inputs = row.querySelectorAll("input,select");

for(let i=0;i<inputs.length;i++){

    const input = inputs[i];

    if(input.tagName==="INPUT" && input.value && !isArabic(input.value)){
        document.getElementById("arabicModal").style.display="flex";
        return;
    }
}

const data={
    index:index,
    last_name:inputs[0].value,
    first_name:inputs[1].value,
    class:inputs[2].value,
    group:inputs[3].value,

    test1:inputs[4].value,
    exam1:inputs[5].value,
    evaluation1:inputs[6].value,

    test2:inputs[7].value,
    exam2:inputs[8].value,
    evaluation2:inputs[9].value,

    test3:inputs[10].value,
    exam3:inputs[11].value,
    evaluation3:inputs[12].value,

    note:inputs[13].value
};

fetch("/edit_student",{
    method:"POST",
    headers:{"Content-Type":"application/x-www-form-urlencoded"},
    body:new URLSearchParams(data)
})
.then(res=>res.json())
.then(resp=>{

    if(resp.status==="success"){

        const cells=row.querySelectorAll("td");

        cells[0].innerText=data.last_name;
        cells[1].innerText=data.first_name;
        cells[2].innerText=data.class;
        cells[3].innerText=data.group;

        for(let i=4;i<=12;i++){
            cells[i].innerText=inputs[i].value;
        }

        cells[13].innerText=data.note;

        row.classList.remove("editing-row");

        toggleButtons(row,false);

        currentEditing=null;
    }
    else{
        alert("حدث خطأ أثناء الحفظ ❌");
    }

});
```

}

// -------------------------
// حذف الطالب
// -------------------------
function showDeleteModal(index){

```
currentIndex=index;

document.getElementById("deleteModal").style.display="flex";
```

}

document.getElementById("deleteCancel").addEventListener("click",()=>{

```
document.getElementById("deleteModal").style.display="none";
```

});

document.getElementById("deleteConfirm").addEventListener("click",()=>{

```
if(currentIndex!==null){

    fetch("/delete_student",{
        method:"POST",
        headers:{"Content-Type":"application/x-www-form-urlencoded"},
        body:"index="+currentIndex
    })
    .then(res=>res.json())
    .then(data=>{

        if(data.status==="success"){

            const row=document.getElementById("row-"+currentIndex);

            if(row) row.remove();
        }

        else{
            alert("حدث خطأ أثناء الحذف ❌");
        }

        document.getElementById("deleteModal").style.display="none";

        currentIndex=null;

    });
}
```

});

// -------------------------
// الطباعة
// -------------------------
function printTables(){

```
window.print();
```

}

function closeArabicModal(){

```
document.getElementById("arabicModal").style.display="none";
```

}
