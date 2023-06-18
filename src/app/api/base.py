import json
from flask import Blueprint, Response, jsonify, request
from app.db.implementations.db_connector import PostgresDbConnector
from app.db.repositories.implementations.transport import TransportRepository
from app.db.repositories.implementations.transport_type import (
    TransportTypeRepository,
)
from app.misc.payloads import convert

from app.services.transport_service import TransportService

api_blueprint = Blueprint('api', __name__, url_prefix='/api')

# TODO сделать адекватное АПИ
@api_blueprint.route('/transportation', methods=["GET"])
def get_transportation():
    # Получаем значение параметра manufacturing_date из GET-запроса
    manufacturing_date = request.args.get('manufacturing_date')
    transport_serv = TransportService(
        TransportRepository(PostgresDbConnector),
        TransportTypeRepository(PostgresDbConnector),
    )
    data = transport_serv.get_all_transport_from_manufacturing_date(
        manufacturing_date
    )
    # TODO разобраться потом с багом отображения кириллицы...
    response = json.dumps(convert(data), ensure_ascii=False)
    return Response(response, content_type='application/json; charset=utf-8')
