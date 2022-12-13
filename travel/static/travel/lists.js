document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#newListBtn').onclick = addNewList;
});

function addNewList() {
    const listForm = document.querySelector('#newListForm')
    if (listForm.style.display.trim() === 'block') {
        listForm.style.display = 'none';
    } else {
        listForm.style.display = 'block';
    }
}