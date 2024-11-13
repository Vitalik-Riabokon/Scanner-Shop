const dateField = document.querySelector('input[name="date"]');
dateField.addEventListener('change', function () {
    document.getElementById('filterForm').submit();
});