document.addEventListener('DOMContentLoaded', function () {

    const itemsContainer = document.getElementById('items-container');

    if (!itemsContainer) return; // защита (если блока нет)

    function updateItemLabels() {
        itemsContainer.querySelectorAll('.item-input').forEach((itemEl, index) => {
            const label = itemEl.querySelector('label');
            if (label) label.textContent = `Пункт ${index + 1}`;
        });
    }

    function createItemInput(index) {
        const item = document.createElement('div');
        item.className = 'mb-3 item-input';
        item.innerHTML = `
            <label>Пункт ${index}</label>
            <div class="input-with-button">
                <input type="text" name="items[]" class="form-control" placeholder="Введите пункт списка">
                <button type="button" class="btn btn-sm btn-danger remove-item">×</button>
            </div>
        `;
        return item;
    }

    function ensureAtLeastOneItem() {
        if (itemsContainer.querySelectorAll('.item-input').length === 0) {
            itemsContainer.appendChild(createItemInput(1));
        }
        updateItemLabels();
    }

    itemsContainer.addEventListener('keydown', function(e) {
        if (e.target.name === 'items[]' && e.key === 'Enter') {
            e.preventDefault();
            const itemCount = itemsContainer.querySelectorAll('.item-input').length + 1;
            const newItem = createItemInput(itemCount);
            itemsContainer.appendChild(newItem);
            newItem.querySelector('input').focus();
            updateItemLabels();
        }
    });

    itemsContainer.addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-item')) {
            const removed = e.target.closest('.item-input');
            if (removed) {
                removed.remove();
                ensureAtLeastOneItem();
            }
        }
    });

    // запуск при загрузке
    ensureAtLeastOneItem();
});