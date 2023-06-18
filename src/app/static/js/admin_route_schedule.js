$(document).ready(function () {
    let activeRouteScheduleId = 0;

    let selectedStops = [];

    $(document).on("click", ".main_table a", function (e) {
        e.preventDefault();
        let href = $(this).attr("href")
        let [id, action] = href.split("_");

        let route_schedule = route_schedule_list.find(function (item) {
            return item.id === parseInt(id);
        });

        if (action == "delete") { deleteRouteSchedule(id); return; }

        let routeSelect = document.getElementById("route");
        routeSelect.innerHTML = "";
        routes.forEach(function (item) {
            let option = document.createElement("option");
            option.value = item.id;
            option.text = item.name;
            if (route_schedule.route.id == item.id) {
                option.selected = true;
            }
            routeSelect.appendChild(option);
        });

        let trTypeSelect = document.getElementById("transport_type");
        trTypeSelect.innerHTML = "";
        transport_type.forEach(function (item) {
            let option = document.createElement("option");
            option.value = item.id;
            option.text = item.name;
            if (route_schedule.transport.transport_type.id == item.id) {
                option.selected = true;
            }
            trTypeSelect.appendChild(option);
        });

        let workersSelect = document.getElementById("workers");
        workersSelect.innerHTML = "";
        transport_workers.forEach(function (item) {
            let option = document.createElement("option");
            option.value = item.id;
            option.text = item.full_name;

            if (route_schedule.transport_workers.some(function (type) {
                return type.id === item.id;
            })) {
                option.selected = true;
            }
            workersSelect.appendChild(option);
        });

        route_schedule.included_stop_schedules.forEach(function (item) {
            createStopSchedule(item.stop, item.departure_time)
        });

        loadAvailableTransportByTransportType(trTypeSelect.value, route_schedule.transport)

        validateFormFields();

        if (action === "show") {
            let modalTitle = document.getElementById("modal_title");
            modalTitle.textContent = "Просмотр записи";

            let formFields = document.querySelectorAll(".modal-body input, .modal-body select, .close");
            formFields.forEach(function (field) {
                field.disabled = true;
            });
            document.getElementById("save_btn").style.display = "none";
            document.getElementById("add_trs_sched").style.display = "none";
        }
        else if (action === 'edit') {
            let modalTitle = document.getElementById("modal_title");
            modalTitle.textContent = "Редактирование записи";

            activeRouteScheduleId = route_schedule.id
        }
        $('.record-modal-lg').modal('show');
        $('.selectpicker').selectpicker('refresh');
    });

    document.getElementById('add_trs_sched').addEventListener(
        'click', function () { createStopSchedule(); }
    );

    function createStopSchedule(tr_stop, departure_time) {
        let trs_schedule = document.createElement('tr');
        let trs_sched_id = document.getElementById("table_trs_sched").tBodies[0].rows.length;

        let name_trs_sched = document.createElement('select');
        name_trs_sched.className = "form-control selectpicker trs_sched";
        name_trs_sched.setAttribute('data-live-search', 'true');
        name_trs_sched.id = trs_sched_id + '_name_trs_sched';

        // Заполняем выпдающий список значениями, которые нигде не выбраны
        cur_tr_type_id = document.getElementById('transport_type').value;
        loadAvailableTrStopByTransportType(name_trs_sched, cur_tr_type_id, tr_stop)

        name_trs_sched.addEventListener('change', function () {
            currentValue = parseInt(name_trs_sched.value);
            previousValue = parseInt(name_trs_sched.prev);
            console.log(currentValue, previousValue);

            // Если выбрано значение по умлочанию, то восстанавливаем предыдущее значение
            if (currentValue == -1 && previousValue != -1) {
                selectedStops.splice(selectedStops.indexOf(previousValue), 1);
            }
            else {
                selectedStops.push(currentValue);
            }
            // Обновляем выпадающие списки во всех строках
            let selectElements = document.querySelectorAll('.trs_sched');
            selectElements.forEach(function (select) {
                if (select.value != currentValue) {
                    if (currentValue != -1) {
                        let option = select.querySelector('option[value="' + currentValue + '"]');
                        if (option) option.style.display = 'none';
                    }
                }
                if (previousValue != -1) {
                    let option = select.querySelector('option[value="' + previousValue + '"]');
                    if (option) option.style.display = 'block';
                }
            });
            name_trs_sched.prev = name_trs_sched.value;
            $('.selectpicker').selectpicker('refresh');
        });

        let dateTimeInput = document.createElement('input');
        dateTimeInput.type = 'datetime-local';
        dateTimeInput.className = 'form-control';
        dateTimeInput.value = departure_time ? new Date(departure_time).toISOString().slice(0, -8) : '';
        dateTimeInput.id = trs_sched_id + '_departure_time_sched';

        let deleteButton = document.createElement('button');
        deleteButton.type = 'button';
        deleteButton.className = 'close';
        deleteButton.ariaLabel = 'Close';

        deleteButton.addEventListener('click', function () {
            // Удаляем выбранную остановку из списка выбранных остановок
            let stopId = parseInt(name_trs_sched.value);
            let index = selectedStops.indexOf(stopId);
            if (index > -1) {
                selectedStops.splice(index, 1);
            }
            trs_schedule.remove();
        });

        let spn = document.createElement('span');
        spn.ariaHidden = 'true';
        spn.innerHTML = '&times;';
        deleteButton.appendChild(spn);

        let td = document.createElement('td');
        let name_trs_shed_error = document.createElement('div');
        name_trs_shed_error.className = 'invalid-feedback';
        name_trs_shed_error.id = name_trs_sched.id + "_error";
        td.appendChild(name_trs_sched);
        td.appendChild(name_trs_shed_error)
        trs_schedule.appendChild(td);

        td = document.createElement('td');
        let departure_time_error = document.createElement('div');
        departure_time_error.className = 'invalid-feedback';
        departure_time_error.id = dateTimeInput.id + "_error";
        td.appendChild(dateTimeInput);
        td.appendChild(departure_time_error);
        trs_schedule.appendChild(td);

        td = document.createElement('td');
        td.appendChild(deleteButton);
        trs_schedule.appendChild(td);

        document.getElementById('table_body_trs_sched').appendChild(trs_schedule);
        $('.selectpicker').selectpicker('refresh');
    }

    function loadAvailableTrStopByTransportType(target_select, tr_type_id, selected_tr_stop) {
        target_select.innerHTML = '';
        // Значние по умолчанию
        let option = document.createElement('option');
        option.value = -1;
        option.text = 'Выберите остановку';
        option.selected = true;
        target_select.appendChild(option);
        target_select.prev = option.value;

        transportation_stop_list.forEach(function (item) {
            if (!item.supported_transport_types.some(function (type) {
                return type.id != tr_type_id;
            })) return;

            let option = document.createElement('option');
            option.value = item.id;
            option.text = item.name;

            if (!selectedStops.includes(item.id)) {
                if (item.id == selected_tr_stop?.id) {
                    option.selected = true;
                    option.style.display = 'none';
                    target_select.prev = item.id;
                    selectedStops.push(item.id);
                }
            } else { option.style.display = 'none'; }
            target_select.appendChild(option);

        });
        $('.selectpicker').selectpicker('refresh');
    }

    function loadAvailableTransportByTransportType(tr_type_id, selected_transport) {
        let transportSelect = document.getElementById('transport');
        transportSelect.innerHTML = '';

        transport_list.forEach(function (item) {
            if (item.transport_type.id != tr_type_id || item.is_repaired) return;
            let option = document.createElement('option');
            option.value = item.id;
            option.text = item.brand;
            if (item.id == selected_transport?.id) {
                option.selected = true;
            }
            transportSelect.appendChild(option);
        });
    }

    document.getElementById("transport_type").addEventListener(
        'change',
        function () {
            selectedStops.length = 0;
            val = document.getElementById("transport_type").value;
            let selectElements = document.querySelectorAll('.trs_sched select');
            selectElements.forEach(function (select) {
                loadAvailableTrStopByTransportType(select, val);
            });
            loadAvailableTransportByTransportType(val);
        }
    );

    function validateFormFields() {
        let table_rows_count = document.getElementById("table_trs_sched").tBodies[0].rows.length;
        let isOk = true;
        for (let i = 0; i < table_rows_count; i++) {
            name_trs_sched = document.getElementById(i + '_name_trs_sched');
            departure_time = document.getElementById(i + '_departure_time_sched');

            if (name_trs_sched.value == -1) {
                displayErrorMessage(name_trs_sched, "Необходимо сделать выбор");
                isOk = false;
            } else {
                hideErrorMessage(name_trs_sched);
            }
            if (departure_time.value.trim() === "") {
                displayErrorMessage(departure_time,
                    "Время отправления не должно быть пустым");
                isOk = false;
            } else {
                hideErrorMessage(departure_time);
            }
        }
        let routeField = document.getElementById("route");
        let transportTypeField = document.getElementById("transport_type");
        let transportField = document.getElementById("transport");

        if (routeField.value.trim() === "") {
            displayErrorMessage(routeField, "Должен быть выбран маршрут");
            isOk = false;
        } else {
            hideErrorMessage(routeField);
        }
        if (transportTypeField.value.trim() === "") {
            displayErrorMessage(transportTypeField,
                "Должен быть выбран тип  транспорта");
            isOk = false;
        } else {
            hideErrorMessage(transportTypeField);
        }
        if (transportField.value.trim() === "") {
            displayErrorMessage(transportField,
                "Должен быть выбран транспорт");
            isOk = false;
        } else {
            hideErrorMessage(transportField);
        }
        return isOk;
    }

    function displayErrorMessage(element, message) {
        element.classList.add("is-invalid"); // Добавляем класс Bootstrap для отображения поля с ошибкой
        let errorMessageElement = document.getElementById(element.id + "_error");
        errorMessageElement.textContent = message;
        errorMessageElement.style.display = "block";
        $('.selectpicker').selectpicker('refresh');
    }

    function hideErrorMessage(element) {
        element.classList.remove("is-invalid"); // Удаляем класс Bootstrap для скрытия поля с ошибкой
        let errorMessageElement = document.getElementById(element.id + "_error");
        if (errorMessageElement == null) return;
        errorMessageElement.textContent = "";
        errorMessageElement.style.display = "none";
        $('.selectpicker').selectpicker('refresh');
        element?.parentElement?.classList.remove("is-invalid");
    }

    document.getElementById("create_new_btn").addEventListener("click", function () {
        activeTransportId = 0;

        document.getElementById("modal_title").textContent = "Создание записи";

        let routeSelect = document.getElementById("route");
        routeSelect.innerHTML = "";
        routes.forEach(function (item) {
            let option = document.createElement("option");
            option.value = item.id;
            option.text = item.name;
            routeSelect.appendChild(option);
        });

        let trTypeSelect = document.getElementById("transport_type");
        trTypeSelect.innerHTML = "";
        transport_type.forEach(function (item) {
            let option = document.createElement("option");
            option.value = item.id;
            option.text = item.name;
            trTypeSelect.appendChild(option);
        });

        let workersSelect = document.getElementById("workers");
        workersSelect.innerHTML = "";
        transport_workers.forEach(function (item) {
            let option = document.createElement("option");
            option.value = item.id;
            option.text = item.full_name;
            workersSelect.appendChild(option);
        });
        loadAvailableTransportByTransportType(trTypeSelect.value)
        $('.record-modal-lg').modal('show');
        $('.selectpicker').selectpicker('refresh');
    });

    function deleteRouteSchedule(route_schedule_id) {
        fetch(`/admin/route_schedule/${route_schedule_id}`, {
            method: "DELETE"
        })
            .then(function (response) {
                // Обработка ответа от сервера
                if (response.ok) {
                    console.log("Расписание успешно удалено");
                    // Самый простой вариант после удаления просто перезагрузить страницу
                    location.reload()
                } else {
                    console.log("Ошибка при удалении расписания");
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
            transport: {
                id: document.getElementById("transport").value,
                transport_type: {
                    id: document.getElementById("transport_type").value
                }
            },
            route: {
                id: document.getElementById("route").value
            },
            transport_workers: [],
            included_stop_schedules: []
        };

        let workersSelect = document.getElementById("workers");
        let selectedWorkers = Array.from(workersSelect.selectedOptions);
        selectedWorkers.forEach(function (option) {
            formData.transport_workers.push({
                id: parseInt(option.value)
            });
        });

        let table_rows_count = document.getElementById("table_trs_sched").tBodies[0].rows.length;
        for (let i = 0; i < table_rows_count; i++) {
            name_trs_sched = document.getElementById(i + '_name_trs_sched');
            departure_time = document.getElementById(i + '_departure_time_sched');
            formData.included_stop_schedules.push({
                transportation_stop: {
                    id: parseInt(name_trs_sched.value),
                },
                departure_time: departure_time.value
            });
        }
        fetch(`/admin/route_schedule/${activeRouteScheduleId}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(formData)
        })
            .then(function (response) {
                // Обработка ответа от сервера
                if (response.ok) {
                    console.log("Расписание успешно сохранено");
                    $('.record-modal-lg').modal('hide');
                    location.reload()
                } else {
                    console.log("Ошибка при сохранении расписания");
                }
            })
            .catch(function (error) {
                console.log("Произошла ошибка при выполнении запроса:", error);
            });
    });

    $('.record-modal-lg').on('hidden.bs.modal', function (e) {
        selectedStops.length = 0;
        let formFields = document.querySelectorAll(".modal-body input, .modal-body select, .close");
        formFields.forEach(function (field) {
            field.disabled = false;
        });
        document.getElementById("table_body_trs_sched").innerHTML = '';

        document.getElementById("save_btn").style.display = "block";
        document.getElementById("add_trs_sched").style.display = "block";

        $('.selectpicker').selectpicker('refresh');
        $('.selectpicker').selectpicker('deselectAll');
    })
});