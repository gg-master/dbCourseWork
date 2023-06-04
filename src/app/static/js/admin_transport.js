$(document).ready(function () {
    let activeTransportId = 0;

    $(document).on("click", ".table_body a", function (e) {
        e.preventDefault();
        let href = $(this).attr("href") //get href
        let [id, action] = href.split("_"); // извлекаем идентификатор из href

        let transport = tranposrt_list.find(function (item) {
            return item.id === parseInt(id);
        });

        if (action == "delete") { deleteTransport(id); return; }

        let selectElement = document.getElementById("transport_type");
        selectElement.innerHTML = "";

        // Создаем и добавляем элементы <option> в выпадающий список
        transpot_type.forEach(function (item) {
            let option = document.createElement("option");
            option.value = item.id;
            option.text = item.name;

            if (item.name == transport.transport_type.name) {
                option.selected = true; // Устанавливаем атрибут selected
            }
            selectElement.appendChild(option);
        });

        // Загружаем данные из массива в форму (проще чем делать запрос)
        document.getElementById("brand").value = transport.brand;
        document.getElementById("registration_number").value = transport.registration_number;
        document.getElementById("manufacturer").value = transport.manufacturer;
        document.getElementById("manufacturing_date").value = transport.manufacturing_date;
        document.getElementById("capacity").value = transport.capacity;
        updateCapacityValue(transport.capacity)
        document.getElementById("is_repaired").checked = transport.is_repaired;

        validateFormFields();

        if (action === "show") {
            let modalTitle = document.getElementById("modal_title");
            modalTitle.textContent = "Просмотр записи";

            let formFields = document.querySelectorAll(".modal-body input, .modal-body select");
            formFields.forEach(function (field) {
                field.disabled = true;
            });
            document.getElementById("save_btn").style.display = "none";
        }
        else if (action === 'edit') {
            let modalTitle = document.getElementById("modal_title");
            modalTitle.textContent = "Редактирование записи";

            activeTransportId = transport.id
        }
        $('.record-modal-lg').modal('show');
    });

    function deleteTransport(transportId) {
        fetch(`/admin/transport/${transportId}`, {
            method: "DELETE"
        })
            .then(function (response) {
                // Обработка ответа от сервера
                if (response.ok) {
                    console.log("Транспорт успешно удален");
                    // Самый простой вариант после удаления просто перезагрузить страницу
                    location.reload()
                } else {
                    console.log("Ошибка при удалении транспорта");
                }
            })
            .catch(function (error) {
                console.log("Произошла ошибка при выполнении запроса:", error);
            });
    }

    function validateFormFields() {
        let brandField = document.getElementById("brand");
        let registrationNumberField = document.getElementById("registration_number");
        let manufacturerField = document.getElementById("manufacturer");
        let manufacturingDateField = document.getElementById("manufacturing_date");

        // Проверка поля "Марка"
        if (brandField.value.trim() === "" || brandField.value.length > 128) {
            displayErrorMessage(brandField,
                "Поле должно быть не пустым и содержать не более 128 символов.");
            return false;
        } else {
            hideErrorMessage(brandField);
        }

        // Проверка поля "Регистрационный номер"
        if (registrationNumberField.value.trim() === "" || registrationNumberField.value.length > 128) {
            displayErrorMessage(registrationNumberField,
                "Поле должно быть не пустым и содержать не более 128 символов.");
            return false;
        } else {
            hideErrorMessage(registrationNumberField);
        }

        // Проверка поля "Производитель"
        if (manufacturerField.value.trim() === "" || manufacturerField.value.length > 256) {
            displayErrorMessage(manufacturerField,
                "Поле должно быть не пустым и содержать не более 256 символов.");
            return false;
        } else {
            hideErrorMessage(manufacturerField);
        }

        // Проверка поля "Дата выпуска"
        let currentDate = new Date();
        let manufacturingDate = new Date(manufacturingDateField.value);
        if (manufacturingDateField.value.trim() === "" ||
            manufacturingDate.toISOString().split('T')[0] > 
            currentDate.toISOString().split('T')[0]) {
            displayErrorMessage(manufacturingDateField,
                "Поле должно содержать дату, меньшую или равную текущей дате.");
            return false;
        } else {
            hideErrorMessage(manufacturingDateField);
        }

        return true;
    }

    function displayErrorMessage(element, message) {
        element.classList.add("is-invalid"); // Добавляем класс Bootstrap для отображения поля с ошибкой
        let errorMessageElement = document.getElementById(element.id + "_error");
        errorMessageElement.textContent = message;
        errorMessageElement.style.display = "block";
    }

    function hideErrorMessage(element) {
        element.classList.remove("is-invalid"); // Удаляем класс Bootstrap для скрытия поля с ошибкой
        let errorMessageElement = document.getElementById(element.id + "_error");
        if (errorMessageElement == null) return;
        errorMessageElement.textContent = "";
        errorMessageElement.style.display = "none";
    }

    document.getElementById("create_new_btn").addEventListener("click", function () {
        activeTransportId = 0;

        document.getElementById("modal_title").textContent = "Создание записи";

        let selectElement = document.getElementById("transport_type");
        selectElement.innerHTML = "";

        // Создаем и добавляем элементы <option> в выпадающий список
        transpot_type.forEach(function (item) {
            let option = document.createElement("option");
            option.value = item.id;
            option.text = item.name;
            selectElement.appendChild(option);
        });
        $('.record-modal-lg').modal('show');
    });

    // Добавляем валидацию при клике на кнопку "Сохранить"
    document.getElementById("save_btn").addEventListener("click", function () {
        if (!validateFormFields()) return;

        let selectElement = document.getElementById("transport_type");
        let selectedOption = selectElement.options[selectElement.selectedIndex];

        let formData = {
            brand: document.getElementById("brand").value,
            registration_number: document.getElementById("registration_number").value,
            manufacturer: document.getElementById("manufacturer").value,
            manufacturing_date: document.getElementById("manufacturing_date").value,
            capacity: document.getElementById("capacity").value,
            is_repaired: document.getElementById("is_repaired").checked,
            transport_type: {
                id: selectedOption.value,
                name: selectedOption.text,
            }
        };

        fetch(`/admin/transport/${activeTransportId}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(formData)
        })
            .then(function (response) {
                // Обработка ответа от сервера
                if (response.ok) {
                    console.log("Транспорт успешно сохранен");
                    // Самый простой вариант после удаления просто перезагрузить страницу
                    $('.record-modal-lg').modal('hide');
                    location.reload()
                } else {
                    console.log("Ошибка при сохранении транспорта");
                }
            })
            .catch(function (error) {
                console.log("Произошла ошибка при выполнении запроса:", error);
            });
    });

    // Обработчик события изменения значения ползунка
    document.getElementById("capacity").addEventListener("input", function () {
        updateCapacityValue(this.value);
    });

    // Функция для обновления текстового элемента с выбранным значением
    function updateCapacityValue(value) {
        document.getElementById("capacity_value").textContent = value;
    }
    $('.record-modal-lg').on('hidden.bs.modal', function (e) {
        document.getElementById("brand").value = "";
        document.getElementById("registration_number").value = "";
        document.getElementById("manufacturer").value = "";
        document.getElementById("manufacturing_date").value = "";
        document.getElementById("capacity").value = "10";
        document.getElementById("is_repaired").checked = false;

        let formFields = document.querySelectorAll(".modal-body input, .modal-body select");
        formFields.forEach(function (field) {
            field.disabled = false;
        });
        document.getElementById("save_btn").style.display = "block";
    })

});

$("#manufacturing_date").datepicker({
    dateFormat: "yy-mm-dd", // Формат даты: ГГГГ-ММ-ДД
    showButtonPanel: true, // Показать панель с кнопками
    closeText: "Закрыть", // Текст кнопки "Закрыть"
    currentText: "Сегодня", // Текст кнопки "Сегодня"
    showOtherMonths: true, // Показать дни других месяцев
    selectOtherMonths: true, // Возможность выбора дней других месяцев
    autoclose: true, // Закрытие календаря после выбора даты
});