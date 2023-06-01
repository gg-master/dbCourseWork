from flask import Blueprint, render_template

from app.db.implementations import Database
from app.db.repositories.implementations import (
    TransportRepository,
    TransportTypeRepository,
)
from app.services import TransportService

view = Blueprint("admin", __name__, url_prefix="/admin")


@view.route("/transport", methods=["GET"])
def transport_list():
    transport_serv = TransportService(
        TransportRepository(Database), TransportTypeRepository(Database)
    )
    print(transport_serv.get_all())
    return render_template("transport_list.html")
