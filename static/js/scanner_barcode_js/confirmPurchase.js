// Переконайтесь, що CSRF токен завантажується

document.getElementById('cash-btn').addEventListener('click', function () {
    confirmPurchase('готівка');
});

document.getElementById('card-btn').addEventListener('click', function () {
    confirmPurchase('карта');
});

function confirmPurchase(paymentMethod) {
    const formData = new FormData();

    if (productList.length === 0) {
        alert("Список покупок порожній!");
        return;
    }

    const productsData = productList.map(product => ({
        id: product.id,
        quantity: product.quantity
    }));

    formData.append('products_data', JSON.stringify(productsData));
    formData.append('payment_method', paymentMethod);

    fetch('/scan/confirm-purchase/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken,
        },
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                productList = [];
                renderProductList();
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Виникла помилка при обробці запиту.');
        });
}
