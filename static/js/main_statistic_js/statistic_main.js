function toggleDetails(noticeBoard) {
    const details = noticeBoard.nextElementSibling;
    const toggleIcon = noticeBoard.querySelector('.toggle-icon');
    if (details.style.display === "none") {
        details.style.display = "block";
        toggleIcon.textContent = "⟪";
    } else {
        details.style.display = "none";
        toggleIcon.textContent = "⟫";
    }
}

function toggleSettings(button) {
    const details = button.closest('.details');
    const quantityDisplays = details.querySelectorAll('.quantity-display');
    const quantityControls = details.querySelectorAll('.quantity-controls');

    if (button.textContent === "Налаштування") {
        quantityDisplays.forEach(display => display.style.display = "none");
        quantityControls.forEach(control => control.style.display = "inline-flex");
        button.textContent = "Підтвердити";
    } else {
        quantityControls.forEach(control => {
            const quantityValue = parseInt(control.querySelector('.quantity-value').textContent);
            const paymentProductId = control.dataset.paymentProductId;
            updateQuantityOnServer(paymentProductId, quantityValue, control);
        });
        button.textContent = "Налаштування";
    }
}

function changeQuantity(button, change) {
    const quantityElement = button.parentElement.querySelector('.quantity-value');
    let quantity = parseInt(quantityElement.textContent);
    quantity += change;

    if (quantity <= 0) {
        quantity = 0;
        button.parentElement.querySelector('.minus-btn').style.display = 'none';
    } else {
        button.parentElement.querySelector('.minus-btn').style.display = 'inline-block';
    }

    quantityElement.textContent = quantity;
}

function updateQuantityOnServer(paymentProductId, quantity, controlElement) {
    fetch('/update-quantity/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `payment_product_id=${paymentProductId}&quantity=${quantity}`
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                if (data.action === 'deleted') {
                    // Видаляємо елемент зі списку
                    const listItem = controlElement.closest('li');
                    listItem.remove();
                } else {
                    // Оновлюємо відображення кількості
                    const quantityDisplay = controlElement.previousElementSibling;
                    quantityDisplay.querySelector('.quantity-value').textContent = quantity;
                    quantityDisplay.style.display = "inline";
                    controlElement.style.display = "none";
                }
            } else {
                console.error('Помилка оновлення кількості:', data.message);
            }
        })
        .catch(error => {
            console.error('Помилка:', error);
        });
}