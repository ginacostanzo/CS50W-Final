document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#removeBtn').onclick = removeBtn;
});

function removeBtn() {
    const button = document.querySelector('#removeBtn')
    button.innerHTML = '<strong>Removed</strong> From List';
    button.disabled = true;
    button.className = 'tripStatus';
}