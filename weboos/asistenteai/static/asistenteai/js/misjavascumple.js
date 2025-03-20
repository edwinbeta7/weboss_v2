function fillForm(row) {
    const cells = row.getElementsByTagName('td');
    document.getElementById('id').value = cells[0].textContent;
    document.getElementById('name').value = cells[1].textContent;
    document.getElementById('nameshort').value = cells[2].textContent;
    document.getElementById('mes').value = cells[3].textContent;
    document.getElementById('dia').value = cells[4].textContent;
    document.getElementById('email').value = cells[5].textContent;
}

function clearForm() {
    document.getElementById('id').value = '';
    document.getElementById('name').value = '';
    document.getElementById('nameshort').value = '';
    document.getElementById('mes').value = '';
    document.getElementById('dia').value = '';
    document.getElementById('email').value = '';
}

function createRow1() {
    const table = document.getElementById('companerosTable').getElementsByTagName('tbody')[0];
    const newRow = table.insertRow();
    newRow.insertCell(0).textContent = document.getElementById('id').value;
    newRow.insertCell(1).textContent = document.getElementById('name').value;
    newRow.insertCell(2).textContent = document.getElementById('email').value;
    newRow.insertCell(3).textContent = document.getElementById('phone').value;
    newRow.insertCell(4).textContent = document.getElementById('address').value;
    clearForm();
}

let campoTexto = document.getElementById("mes");

function modifyRow1() {
    const id = document.getElementById('id').value;
    const rows = document.getElementById('companerosTable').getElementsByTagName('tbody')[0].getElementsByTagName('tr');
    for (let row of rows) {
        if (row.getElementsByTagName('td')[0].textContent === id) {
            row.getElementsByTagName('td')[1].textContent = document.getElementById('name').value;
            row.getElementsByTagName('td')[2].textContent = document.getElementById('email').value;
            row.getElementsByTagName('td')[3].textContent = document.getElementById('phone').value;
            row.getElementsByTagName('td')[4].textContent = document.getElementById('address').value;
            clearForm();
            break;
        }
    }
}

function deleteRow1() {
    const id = document.getElementById('id').value;
    const rows = document.getElementById('companerosTable').getElementsByTagName('tbody')[0].getElementsByTagName('tr');
    for (let row of rows) {
        if (row.getElementsByTagName('td')[0].textContent === id) {
            row.remove();
            clearForm();
            break;
        }
    }
}
document.getElementById('mes').addEventListener('keydown', function(event) {
    event.preventDefault(); // Evita que el formulario se envíe automáticamente

    const numero = document.getElementById('mes').value;
    if (validarNumero(numero)) {
        alert("Número válido");
    } else {
        alert("Número no válido. Por favor, introduce un número entre 1 y 12.");
    }
});

function validarNumero(numero) {
    // Convertir a número y comprobar el rango
    const num = parseInt(numero, 10);
    return !isNaN(num) && num >= 1 && num <= 12;
}

