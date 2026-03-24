document.addEventListener('DOMContentLoaded', function () {

    const itemsContainer = document.getElementById('items-container');
    const addItemBtn = document.getElementById('add-item-btn'); // кнопка «Новый пункт»

    if (!itemsContainer || !addItemBtn) return; // защита (если блоков нет)

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

    // добавление нового пункта по Enter
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

    // добавление нового пункта по кнопке
    addItemBtn.addEventListener('click', function() {
        const itemCount = itemsContainer.querySelectorAll('.item-input').length + 1;
        const newItem = createItemInput(itemCount);
        itemsContainer.appendChild(newItem);
        newItem.querySelector('input').focus();
        updateItemLabels();
    });

    // удаление пункта
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