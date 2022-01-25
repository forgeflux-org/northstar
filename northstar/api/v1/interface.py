"""
Interface related routes
"""
# North Star ---  A lookup service for forged fed ecosystem
# Copyright © 2022 Aravinth Manivannan <realaravinth@batsense.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
from flask import Blueprint, jsonify, request
from .utils import clean_url, not_url

from northstar.db import get_db
from .errors import (
    F_D_EMPTY_FORGE_LIST,
    F_D_INVALID_PAYLOAD,
    F_D_NOT_URL,
)

bp = Blueprint("API_V1_INTERFACE", __name__, url_prefix="/interface")


@bp.route("/register", methods=["POST"])
def register():
    """Register interface"""

    data = request.get_json()
    if any(["forge_url" not in data, "interface_url" not in data]):
        return F_D_INVALID_PAYLOAD.get_error_resp()

    forge_url = data["forge_url"]
    interface_url = clean_url(data["interface_url"])
    if not_url(interface_url):
        return F_D_NOT_URL.get_error_resp()

    if len(forge_url) == 0:
        return F_D_EMPTY_FORGE_LIST.get_error_resp()

    new_forge_url = []
    for forge in forge_url:
        url = clean_url(forge)
        if not_url(url):
            return F_D_NOT_URL.get_error_resp()
        new_forge_url.append(url)

    forge_url = new_forge_url

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO northstar_interfaces (URL) VALUES (?);",
        (interface_url,),
    )
    for forge in forge_url:
        cur.execute(
            "INSERT OR IGNORE INTO northstar_forges (URL) VALUES (?);", (forge,)
        )
    conn.commit()

    for forge in forge_url:
        cur.execute(
            """
        INSERT OR IGNORE INTO
            northstar_interface_forge_directory (forge_id, interface_id)
        VALUES (
                (SELECT ID FROM northstar_forges WHERE URL = ?),
                (SELECT ID FROM northstar_interfaces WHERE URL = ?)
            );""",
            (forge, interface_url),
        )
    conn.commit()
    return jsonify({})
