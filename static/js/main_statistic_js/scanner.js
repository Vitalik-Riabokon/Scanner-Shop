const scannerModal = document.getElementById('scanner-modal');
const openScannerBtn = document.getElementById('open-scanner-btn');
const closeScannerBtn = document.getElementById('close-scanner-btn');

openScannerBtn.addEventListener('click', () => {
    scannerModal.style.display = 'flex';
    startScanner();
});

closeScannerBtn.addEventListener('click', () => {
    scannerModal.style.display = 'none';
    stopScanner();
});

function startScanner() {
    const scanner = new Html5QrcodeScanner('reader', {
        qrbox: {
            width: 250,
            height: 250,
        },
        fps: 20,
    });
    scanner.render(success, error);
}

function stopScanner() {
    const readerElement = document.getElementById('reader');
    readerElement.innerHTML = ''; // Clear the scanner
}

function success(result) {
    document.getElementById('result').innerHTML = `
      <h2>Успіх!</h2>
      <p><a href="${result}">${result}</a></p>
    `;
    stopScanner();
}

function error(err) {
    console.error(err);
}