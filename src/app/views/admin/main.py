from flask import Blueprint, jsonify, render_template, request
from app.db.implementations import PostgresDbConnector
from app.db.repositories.implementations import (
    TransportRepository,
    TransportTypeRepository,
    TransportationStopRepository,
)
from app.services import TransportService, TransportationStopService
from app.services.dto import Transport, TransportationStop
from app.misc.payloads import convert


view = Blueprint("admin", __name__, url_prefix="/admin")


@view.route('/')
def stat():
    # TODO сделать аналитические запросы
    return render_template("admin_stat.html")


@view.route("/transport/", methods=["GET"])
def transport_list():
    transport_serv = TransportService(
        TransportRepository(PostgresDbConnector),
        TransportTypeRepository(PostgresDbConnector),
    )
    all_tr_types = convert(
        TransportTypeRepository(PostgresDbConnector).get_all()
    )
    all_tr = convert(transport_serv.get_all())
    return render_template(
        "admin_transport_list.html",
        transport=all_tr,
        transport_types=all_tr_types,
    )


@view.route("/transport/<int:transport_id>", methods=["POST", "DELETE"])
def transport_action(transport_id):
    tr_service = TransportService(
        TransportRepository(PostgresDbConnector),
        TransportTypeRepository(PostgresDbConnector),
    )
    if request.method == "DELETE":
        tr_service.delete(transport_id)
    elif request.method == "POST":
        data = request.get_json()
        data["id"] = transport_id
        transport = Transport.from_dict(data)

        if transport_id == 0:
            tr_service.create(transport)
        else:
            tr_service.update(transport)
    return jsonify(success=True)


@view.route("/transportation_stop/", methods=["GET"])
def transportation_stop_list():
    tr_stop_serv = TransportationStopService(
        TransportationStopRepository(PostgresDbConnector)
    )
    all_stops = convert(tr_stop_serv.get_all())
    all_tr_types = convert(
        TransportTypeRepository(PostgresDbConnector).get_all()
    )
    return render_template(
        "admin_transportation_stop_list.html",
        tr_stops=all_stops,
        transport_types=all_tr_types,
    )


@view.route("/transportation_stop/<int:tr_stop_id>", methods=["POST", "DELETE"])
def transportation_stop_action(tr_stop_id):
    tr_stop_serv = TransportationStopService(
        TransportationStopRepository(PostgresDbConnector)
    )
    if request.method == "DELETE":
        tr_stop_serv.delete(tr_stop_id)
    elif request.method == "POST":
        data = request.get_json()
        data["id"] = tr_stop_id
        transport = TransportationStop.from_dict(data)
        if tr_stop_id == 0:
            tr_stop_serv.create(transport)
        else:
            tr_stop_serv.update(transport)
    return jsonify(success=True)
