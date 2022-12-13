document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#toggleLists').onclick = toggleLists;
    document.querySelector('#saveListsBtn').onclick = saveLists;
    document.querySelector('#cancelListsBtn').onclick = toggleLists;
    document.querySelector('#newListBtn').onclick = addNewList; 
    document.querySelector('#togglePhotos').onclick = togglePhotos;
    document.querySelector('#tripPhoto').onclick = togglePhotos;

    // Edit post function when "edit post" link is clicked
    document.querySelectorAll('#prevBtn').forEach(prevBtn => {
        prevBtn.addEventListener('click', () => slideshow((prevBtn.dataset.photoid), -1))
    });
    // Edit post function when "edit post" link is clicked
    document.querySelectorAll('#nextBtn').forEach(nextBtn => {
        nextBtn.addEventListener('click', () => slideshow((nextBtn.dataset.photoid), 1))
    });

});

function toggleLists() {
    const lists = document.querySelector('#selectListPopUp')
    lists.style.animationPlayState = 'paused';
    if (lists.style.display.trim() === 'block') {
        lists.style.display = 'none';
    } else {
        lists.style.display = 'block';
        lists.style.animationPlayState = 'running';
    }
    window.onkeyup = function (event) {
        if (event.keyCode == 27) {
            document.querySelector('#selectListPopUp').style.display = 'none';
        }
    }
}

function saveLists() {
    const lists = document.querySelector('#selectListPopUp')
    const listsBtn = document.querySelector('#toggleLists')
    if (lists.style.display.trim() === 'block') {
        lists.style.display = 'none';
        listsBtn.innerHTML = 'Lists Saved'
    } else {
        lists.style.display = 'block';
    }
}

function addNewList() {
    const listForm = document.querySelector('#newListForm')
    if (listForm.style.display.trim() === 'block') {
        listForm.style.display = 'none';
    } else {
        listForm.style.display = 'block';
    }
}

function togglePhotos() {
    const slideshow = document.querySelector('#slideshowContainer')
    const photo = document.querySelector('#photo1')
    const buttons = document.querySelector('#buttons1')
    slideshow.style.animationPlayState = 'paused';
    if (slideshow.style.display.trim() === 'block') {
        slideshow.style.display = 'none';
        photo.className = 'hiddenSlide';
        buttons.className = 'hiddenSlide';
    } else {
        slideshow.style.display = 'block';
        slideshow.style.animationPlayState = 'running';
        photo.className = 'visibleSlide'
        buttons.className = 'visibleSlide';
    }
    document.querySelector('#closePhotosBtn').onclick = function () {
        document.querySelector('#slideshowContainer').style.display = 'none';
            document.querySelector(`#photo1`).className = 'hiddenSlide';
            document.querySelector(`#buttons1`).className = 'hiddenSlide';
    }
    
    window.onkeyup = function (event) {
        if (event.keyCode == 27) {
            document.querySelector('#slideshowContainer').style.display = 'none';
            document.querySelector(`#photo1`).className = 'hiddenSlide';
            document.querySelector(`#buttons1`).className = 'hiddenSlide';
        }
    }
}

// Next/previous controls
function slideshow(id, n) {
    var current = document.querySelector(`#photo${id}`);
    var buttons = document.querySelector(`#buttons${id}`);
    var newId = parseInt(id) + parseInt(n);
    if (newId >= 1) {
        var newPhoto = document.querySelector(`#photo${newId}`);
        var newBtns = document.querySelector(`#buttons${newId}`);
        if (newPhoto !== null && newPhoto !== undefined) {
            // object exists
            current.className = 'hiddenSlide';
            buttons.className = 'hiddenSlide';
            newPhoto.className = 'visibleSlide';
            newBtns.className = 'visibleSlide';
        } else {
            // object does not exist
            var first = document.querySelector('#photo1');
            var firstBtns = document.querySelector('#buttons1')
            current.className = 'hiddenSlide';
            buttons.className = 'hiddenSlide';
            first.className = 'visibleSlide';
            firstBtns.className = 'visibleSlide';
        }
    }
    document.querySelector('#closePhotosBtn').onclick = function () {
        document.querySelector('#slideshowContainer').style.display = 'none';
        document.querySelector(`#photo${newId}`).className = 'hiddenSlide';
        document.querySelector(`#buttons${newId}`).className = 'hiddenSlide';
    };
    
    window.onkeyup = function (event) {
        if (event.keyCode == 27) {
            document.querySelector('#slideshowContainer').style.display = 'none';
            document.querySelector(`#photo${newId}`).className = 'hiddenSlide';
            document.querySelector(`#buttons${newId}`).className = 'hiddenSlide';
        }
    }
}