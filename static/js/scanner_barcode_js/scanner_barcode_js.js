let isScanning = false;
let html5QrCode;

const csrfToken = getCSRFToken();

function onScanSuccess(decodedText, decodedResult) {
    if (isScanning) return;
    isScanning = true;

    const formData = new FormData();
    formData.append('barcode', decodedText);

    fetch('', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken, // змінна збереження токену
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (data.products.length > 1) {
                    showProductOptions(data.products);  // Ця функція буде в productList.js
                } else {
                    addProductToList(data.products[0]); // Ця функція буде в productList.js
                }
            } else {
                alert(data.message);
            }
        })
        .catch(error => console.error('Error:', error))
        .finally(() => {
            setTimeout(() => {
                isScanning = false;
            }, 2000);
        });
}

function onScanFailure(error) {
    console.warn(`Помилка сканування: ${error}`);
}

function startScanner() {
    Html5Qrcode.getCameras().then(devices => {
        if (devices && devices.length) {
            let cameraId = devices[devices.length - 1].id;
            html5QrCode = new Html5Qrcode("reader");
            html5QrCode.start(
                cameraId,
                {
                    fps: 10,
                    qrbox: {width: 250, height: 250}
                },
                onScanSuccess,
                onScanFailure
            );
        }
    }).catch(err => {
        console.error("Error getting cameras", err);
    });
}

// Ініціалізація сканера при завантаженні сторінки
startScanner();
