let items = []; // data inventory utama

// Fungsi untuk merender tabel
function renderTable(data) {
    const tableBody = document.getElementById("table-body");
    tableBody.innerHTML = "";

    data.forEach(item => {
        const row = `
            <tr>
                <td>${item.id}</td>
                <td>${item.name}</td>
                <td>${item.category}</td>
                <td>${item.qty}</td>
                <td>${item.location}</td>
            </tr>
        `;
        tableBody.innerHTML += row;
    });
}
function loadInventory("inventory.json") {
    items = "inventory.json";

    sortById();

    renderTable(items);
}
// SORTING FUNCTIONS
function sortById() {
    items.sort((a, b) => a.id.localeCompare(b.id));
    renderTable(items);
}
function sortByName() {
    items.sort((a, b) => a.name.localeCompare(b.name));
    renderTable(items);
}
function sortByCategory() {
    items.sort((a, b) => a.category.localeCompare(b.category));
    renderTable(items);
}
function sortByQty() {
    items.sort((a, b) => a.qty - b.qty); // ascending
    renderTable(items);
}
// Sorting hasil search
function renderSearchResults(results) {
    // urutkan dulu sebelum tampil
    results.sort((a, b) => a.id.localeCompare(b.id));

    renderTable(results);

}
