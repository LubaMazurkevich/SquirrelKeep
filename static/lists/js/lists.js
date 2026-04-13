document.addEventListener('DOMContentLoaded', function () {

    const itemsContainer = document.getElementById('items-container');
    const addItemBtn = document.getElementById('add-item-btn');

    if (!itemsContainer || !addItemBtn) return;

    // Обновляет нумерацию видимых пунктов
    function updateItemLabels() {
        let counter = 1;
        itemsContainer.querySelectorAll('.item-input').forEach(itemEl => {
            if (itemEl.style.display !== 'none') {
                const label = itemEl.querySelector('label');
                if (label) label.textContent = `Пункт ${counter++}`;
            }
        });
    }

    const emptyFormTemplate = document.getElementById('empty-form-template');
    const totalFormsInput = document.querySelector('[name$="-TOTAL_FORMS"]');

    if (emptyFormTemplate && totalFormsInput) {
        // ── Режим редактирования: formset ──────────────────────────────

        addItemBtn.addEventListener('click', function () {
            const totalForms = parseInt(totalFormsInput.value);
            const wrapper = document.createElement('div');
            wrapper.innerHTML = emptyFormTemplate.innerHTML.replace(/__prefix__/g, totalForms);
            const newRow = wrapper.firstElementChild;
            totalFormsInput.value = totalForms + 1;
            itemsContainer.appendChild(newRow);
            newRow.querySelector('input[type="text"]').focus();
            updateItemLabels();
        });

        itemsContainer.addEventListener('click', function (e) {
            if (!e.target.classList.contains('remove-item')) return;
            const row = e.target.closest('.item-input');
            if (!row) return;
            const idInput = row.querySelector('input[name$="-id"]');
            if (idInput && idInput.value) {
                // Существующий пункт: помечаем DELETE, скрываем строку
                const deleteCheckbox = row.querySelector('input[type="checkbox"]');
                if (deleteCheckbox) deleteCheckbox.checked = true;
                row.style.display = 'none';
            } else {
                // Новый пункт (ещё не сохранён): просто убираем из DOM
                row.remove();
            }
            updateItemLabels();
        });

    } else {
        // ── Режим создания: обычные items[] ───────────────────────────

        function createItemInput() {
            const item = document.createElement('div');
            item.className = 'mb-3 item-input';
            item.innerHTML = `
                <label>Пункт</label>
                <div class="input-with-button">
                    <input type="text" name="items[]" class="form-control" placeholder="Введите пункт списка">
                    <button type="button" class="btn btn-sm btn-danger remove-item">×</button>
                </div>
            `;
            return item;
        }

        function ensureAtLeastOneItem() {
            if (itemsContainer.querySelectorAll('.item-input').length === 0) {
                itemsContainer.appendChild(createItemInput());
            }
            updateItemLabels();
        }

        addItemBtn.addEventListener('click', function () {
            const newItem = createItemInput();
            itemsContainer.appendChild(newItem);
            newItem.querySelector('input[type="text"]').focus();
            updateItemLabels();
        });

        itemsContainer.addEventListener('click', function (e) {
            if (e.target.classList.contains('remove-item')) {
                const removed = e.target.closest('.item-input');
                if (removed) {
                    removed.remove();
                    ensureAtLeastOneItem();
                }
            }
        });

        ensureAtLeastOneItem();
    }

    // Enter добавляет новый пункт в обоих режимах
    itemsContainer.addEventListener('keydown', function (e) {
        if (e.key !== 'Enter') return;
        const tag = e.target.tagName;
        const type = (e.target.type || '').toLowerCase();
        if (tag !== 'INPUT' || (type && type !== 'text')) return;
        e.preventDefault();
        addItemBtn.click();
    });

    updateItemLabels();
});