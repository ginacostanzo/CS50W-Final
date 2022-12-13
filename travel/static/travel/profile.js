document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#editProfileBtn').onclick = toggleEditProfile;
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

function toggleEditProfile() {
    const edit = document.querySelector('#editprofile')
    const profile = document.querySelector('#profile')
    const button = document.querySelector('#editProfileBtn')
    if (edit.style.display.trim() === 'block') {
        edit.style.display = 'none';
        profile.style.display = 'block';
        button.innerHTML = 'Edit Profile';
    } else {
        edit.style.display = 'block';
        profile.style.display = 'none';
        button.innerHTML = 'View Profile';
    }
}