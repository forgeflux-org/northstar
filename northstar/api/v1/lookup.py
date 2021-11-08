"""
Lookup related routes
"""
# North Star ---  A lookup service for forged fed ecosystem
# Copyright © 2021 G V Datta Adithya <dat.adithya@gmail.com>
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
from .errors import F_D_NOT_URL, F_D_NO_REGISTERED_INTERFACES, F_D_INVALID_PAYLOAD


bp = Blueprint("API_V1_INTERFACE_LOOKUP", __name__, url_prefix="/forge")


@bp.route("/interfaces", methods=["POST"])
def lookup():
    """Lookup for the interface"""

    # Retrieves the data from the POST request
    data = request.get_json()

    # Check if the data consists of the required field
    if "forge_url" in data:
        # Retrieves the raw forge url
        forge_url = data["forge_url"]

        # Check if the given forge_url is valid
        if len(forge_url) == 0 or not_url(forge_url):
            return F_D_NOT_URL.get_error_resp()

        # Connect to the database
        conn = get_db()
        cur = conn.cursor()

        # Retrieve the interface and forge from the database
        interface_results = cur.execute(
            "SELECT interface_url FROM northstar_lookup WHERE forge_url = (?)",
            (clean_url(forge_url),),
        ).fetchall()
        conn.commit()

        # Check if we received any results
        if len(interface_results) == 0:
            return F_D_NO_REGISTERED_INTERFACES.get_error_resp()

        res = list()
        for r in interface_results:
            res.append(r[0])
        return jsonify(res)

    # If all else fails, throw an error.
    return F_D_INVALID_PAYLOAD.get_error_resp()
