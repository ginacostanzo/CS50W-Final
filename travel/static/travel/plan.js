document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#addTag').onclick = createNewTagField;
});

function createNewTagField() {
    const original = document.querySelector('#tagDiv');
    const inputHTML = `<input list="tags" name="tags[]" class="planInput tags" placeholder="Type a tag" type='text'/> `;
    original.insertAdjacentHTML('beforeend', inputHTML);
}