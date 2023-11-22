const networkFilter = document.getElementById('network-filter');
const rows = document.querySelectorAll('tr');
const contractRows = document.getElementById('contract-rows');
const rowsPerPage = 20;

function showRows(startIndex, endIndex) {
    rows.forEach((row, index) => {
        if (index >= startIndex && index < endIndex) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

function showPage(page) {
    const startIndex = (page - 1) * rowsPerPage;
    const endIndex = startIndex + rowsPerPage;
    showRows(startIndex, endIndex);
}

networkFilter.addEventListener('change', function () {
    const selectedNetwork = networkFilter.value;

    rows.forEach(row => {
        if (selectedNetwork === 'all' || row.classList.contains(selectedNetwork)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
});

// Initially show the first page
showPage(1);