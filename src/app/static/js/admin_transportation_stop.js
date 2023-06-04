$(document).ready(function () {
    let activeTrStopId = 0;

    $(document).on("click", ".table_body a", function (e) {
        e.preventDefault();
        let href = $(this).attr("href")
        let [id, action] = href.split("_");

        let tr_stop = tranposrtation_stop_list.find(function (item) {
            return item.id === parseInt(id);
        });

        if (action == "delete") { deleteTransportationStop(id); return; }

        let selectElement = document.getElementById("transport_type");
        selectElement.innerHTML = "";

        // Создаем и добавляем элементы <option> в выпадающий список
        transpot_type.forEach(function (item) {
            let option = document.createElement("option");
            option.value = item.id;
            option.text = item.name;
            
            if (tr_stop.supported_transport_types.some(function (type) {
                return type.id === item.id;
            })) {
                option.selected = true;
            }
            selectElement.appendChild(option);
        });

        // Загружаем данные из массива в форму (проще чем делать запрос)
        document.getElementById("name").value = tr_stop.name;
        document.getElementById("latitude").value = tr_stop.latitude;
        document.getElementById("longitude").value = tr_stop.longitude;

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

            activeTrStopId = tr_stop.id
        }
        $('.record-modal-lg').modal('show');
        $('.selectpicker').selectpicker('refresh');
    });

    function validateFormFields() {
        let nameField = document.getElementById("name");
        let latitudeField = document.getElementById("latitude");
        let longitudeField = document.getElementById("longitude");

        if (nameField.value.trim() === "" || nameField.value.length >= 256) {
            displayErrorMessage(nameField,
                "Поле должно быть не пустым и содержать не более 256 символов.");
            return false;
        } else {
            hideErrorMessage(nameField);
        }

        let latitude = parseFloat(latitudeField.value);
        if (isNaN(latitude) || latitude < -90.0 || latitude > 90.0) {
            displayErrorMessage(latitudeField,
                "Значение должно быть числом в диапазоне от -90.00 до 90.00.");
            return false;
        } else {
            hideErrorMessage(latitudeField);
        }

        let longitude = parseFloat(longitudeField.value);
        if (isNaN(longitude) || longitude < -180.0 || longitude > 180.0) {
            displayErrorMessage(longitudeField,
                "Значение должно быть числом в диапазоне от -180.00 до 180.00.");
            return false;
        } else {
            hideErrorMessage(longitudeField);
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
        $('.selectpicker').selectpicker('refresh');
    });

    function deleteTransportationStop(trStopId) {
        fetch(`/admin/transportation_stop/${trStopId}`, {
            method: "DELETE"
        })
            .then(function (response) {
                // Обработка ответа от сервера
                if (response.ok) {
                    console.log("Остановка успешно удалена");
                    // Самый простой вариант после удаления просто перезагрузить страницу
                    location.reload()
                } else {
                    console.log("Ошибка при удалении остановки");
                }
            })
            .catch(function (error) {
                console.log("Произошла ошибка при выполнении запроса:", error);
            });
    }

    // Добавляем валидацию при клике на кнопку "Сохранить"
    document.getElementById("save_btn").addEventListener("click", function () {
        if (!validateFormFields()) return;

        let formData = {
            name: document.getElementById("name").value,
            latitude: parseFloat(document.getElementById("latitude").value),
            longitude: parseFloat(document.getElementById("longitude").value),
            supported_transport_types: []
        };
    
        let selectElement = document.getElementById("transport_type");
        let selectedOptions = Array.from(selectElement.selectedOptions);
        selectedOptions.forEach(function (option) {
            formData.supported_transport_types.push({
                id: parseInt(option.value),
                name: option.text
            });
        });

        fetch(`/admin/transportation_stop/${activeTrStopId}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(formData)
        })
            .then(function (response) {
                // Обработка ответа от сервера
                if (response.ok) {
                    console.log("Остановка успешно сохранена");
                    $('.record-modal-lg').modal('hide');
                    location.reload()
                } else {
                    console.log("Ошибка при сохранении остановки");
                }
            })
            .catch(function (error) {
                console.log("Произошла ошибка при выполнении запроса:", error);
            });
    });

    $('.record-modal-lg').on('hidden.bs.modal', function (e) {
        document.getElementById("name").value = "";
        document.getElementById("latitude").value = 0;
        document.getElementById("longitude").value = 0;

        let formFields = document.querySelectorAll(".modal-body input, .modal-body select");
        formFields.forEach(function (field) {
            field.disabled = false;
        });
        document.getElementById("save_btn").style.display = "block";
        $('.selectpicker').selectpicker('refresh');
        $('.selectpicker').selectpicker('deselectAll');
    })
});