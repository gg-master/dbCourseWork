$(document).ready(function () {
    // получаем элемент input с id="manufacturing_date"
    let manufacturingDateInput = document.querySelector('#manufacturing_date');

    // добавляем обработчик события изменения значения поля
    manufacturingDateInput.addEventListener('change', (event) => {
        let selectedDate = manufacturingDateInput.value; // получаем выбранную дату

        // делаем AJAX-запрос на сервер
        fetch(`/api/transportation?manufacturing_date=${selectedDate}`)
            .then(response => response.json())
            .then(data => {
                // обновляем содержимое таблицы с id="manufactured_transport_table" полученными данными
                const tableBody = document.querySelector('#manufactured_transport_table');
                tableBody.innerHTML = ''; // очищаем содержимое tbody перед добавлением новых данных
                data.forEach(item => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                    <td>${item.id}</td>
                    <td>${item.transport_type.name}</td>
                    <td>${item.brand}</td>
                    <td>${item.registration_number}</td>
                    <td>${item.manufacturing_date}</td>
                `;
                    tableBody.appendChild(row);
                });
            })
            .catch(error => console.error(error));
    });
});
