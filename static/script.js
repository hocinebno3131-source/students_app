window.addEventListener("DOMContentLoaded", () => {
    const urlParams = new URLSearchParams(window.location.search);
    if(urlParams.get("duplicate") === "1") {
        document.getElementById("duplicateModal").style.display = "flex";
    }
});

function closeDuplicateModal() {
    document.getElementById("duplicateModal").style.display = "none";
}
