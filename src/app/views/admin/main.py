from flask import Blueprint, jsonify, render_template, request
from app.db.implementations import PostgresDbConnector
from app.db.repositories.implementations import (
    TransportRepository,
    TransportTypeRepository,
    TransportationStopRepository,
    RouteScheduleRepository,
    RouteRepository,
    TransportationStopScheduleRepository,
    TransportWorkerRepository,
)
from app.services import (
    TransportService,
    TransportationStopService,
    RouteScheduleService,
    RouteService,
    TransportationStopScheduleService,
)
from app.services.dto import Transport, TransportationStop, RouteSchedule
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


@view.route(
    "/transportation_stop/<int:tr_stop_id>", methods=["POST", "DELETE"]
)
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


@view.route("/route_schedule/", methods=["GET"])
def route_schedule_list():
    route_schedule_serv = RouteScheduleService(
        RouteScheduleRepository(PostgresDbConnector),
        RouteService(RouteRepository(PostgresDbConnector)),
        TransportService(
            TransportRepository(PostgresDbConnector),
            TransportTypeRepository(PostgresDbConnector),
        ),
        TransportationStopScheduleService(
            TransportationStopScheduleRepository(PostgresDbConnector),
            RouteScheduleRepository(PostgresDbConnector),
            TransportationStopService(
                TransportationStopRepository(PostgresDbConnector)
            ),
        ),
    )
    tr_stop_serv = TransportationStopService(
        TransportationStopRepository(PostgresDbConnector)
    )
    routes_serv = RouteService(RouteRepository(PostgresDbConnector))
    transport_serv = TransportService(
        TransportRepository(PostgresDbConnector),
        TransportTypeRepository(PostgresDbConnector),
    )

    route_schedule_list = convert(route_schedule_serv.get_all())
    transpot_type = convert(
        TransportTypeRepository(PostgresDbConnector).get_all()
    )
    transportation_stop_list = convert(tr_stop_serv.get_all())
    routes = convert(routes_serv.get_all())
    transport_list = convert(transport_serv.get_all())
    transport_workers = convert(
        TransportWorkerRepository(PostgresDbConnector).get_all()
    )
    return render_template(
        "admin_route_schedule.html",
        route_schedule_list=route_schedule_list,
        transport_type=transpot_type,
        transportation_stop_list=transportation_stop_list,
        routes=routes,
        transport_list=transport_list,
        transport_workers=transport_workers,
    )


@view.route("/route_schedule/<int:route_sched_id>", methods=["POST", "DELETE"])
def route_schedule_action(route_sched_id):
    route_schedule_serv = RouteScheduleService(
        RouteScheduleRepository(PostgresDbConnector),
        RouteService(RouteRepository(PostgresDbConnector)),
        TransportService(
            TransportTypeRepository(PostgresDbConnector),
            TransportTypeRepository(PostgresDbConnector),
        ),
        TransportationStopScheduleService(
            TransportationStopScheduleRepository(PostgresDbConnector),
            RouteScheduleRepository(PostgresDbConnector),
            TransportationStopService(
                TransportationStopRepository(PostgresDbConnector)
            ),
        ),
    )
    if request.method == "DELETE":
        route_schedule_serv.delete(route_sched_id)
    elif request.method == "POST":
        data = request.get_json()
        data["id"] = route_sched_id
        route_schedule = RouteSchedule.from_dict(data)
        if route_sched_id == 0:
            route_schedule_serv.create(route_schedule)
        else:
            route_schedule_serv.update(route_schedule)
    return jsonify(success=True)
