let productList = [];

function addProductToList(product) {
    const existingProduct = productList.find(p => p.id === product.id);
    if (existingProduct) {
        existingProduct.quantity += 1;
    } else {
        productList.push({...product, quantity: 1});
    }
    renderProductList();
}

function renderProductList() {
    const productListDiv = document.getElementById('product-list');
    productListDiv.innerHTML = '';

    productList.forEach((product, index) => {
        const productElement = `
            <div class="product">
                <img src="${product.image}" alt="${product.name}">
                <div class="product-details">
                    <p>${product.name}</p>
                    <p>Ціна: ${product.price} грн</p>
                    <div class="quantity-controls">
                        <button class="quantity-btn minus-btn" onclick="changeQuantity(${index}, -1)">-</button>
                        <span class="quantity-value">${product.quantity}</span>
                        <button class="quantity-btn plus-btn" onclick="changeQuantity(${index}, 1)">+</button>
                    </div>
                </div>
                <button class="remove-btn" onclick="removeProduct(${index})">Видалити</button>
            </div>
        `;
        productListDiv.innerHTML += productElement;
    });

    updateTotalSum();
}

function showProductOptions(products) {
    const modal = document.getElementById('productModal');
    const productOptions = document.getElementById('productOptions');
    productOptions.innerHTML = '';

    products.forEach(product => {
        const option = document.createElement('div');
        option.classList.add('product-option');
        option.innerHTML = `
            <img src="${product.image}" alt="${product.name}">
            <div class="product-name">${product.name}</div>
            <div class="product-price">${product.price} грн</div>
        `;
        option.onclick = () => {
            addProductToList(product);
            modal.style.display = 'none';
        };
        productOptions.appendChild(option);
    });

    modal.style.display = 'block';
}

function changeQuantity(index, change) {
    const product = productList[index];
    product.quantity += change;
    if (product.quantity <= 0) {
        if (confirm('Ви бажаєте видалити товар?')) {
            removeProduct(index);
        } else {
            product.quantity = 1;
        }
    }
    renderProductList();
}

function removeProduct(index) {
    productList.splice(index, 1);
    renderProductList();
}

function updateTotalSum() {
    const totalSum = productList.reduce((sum, product) => sum + parseFloat(product.price) * product.quantity, 0);
    const totalSumElement = document.getElementById('total-sum');
    totalSumElement.textContent = `Загальна сума: ${totalSum.toFixed(2)} грн`;
}
