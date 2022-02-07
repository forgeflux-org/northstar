"""
Lookup related routes
"""
# North Star ---  A lookup service for forged fed ecosystem
# Copyright © 2022 G V Datta Adithya <dat.adithya@gmail.com>
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

from northstar.db import DBMap
from northstar.errors import Error, F_D_INVALID_PAYLOAD

bp = Blueprint("API_V1_INTERFACE_LOOKUP", __name__, url_prefix="/forge")


@bp.route("/interfaces", methods=["POST"])
def lookup():
    """Lookup for the interface"""

    # Retrieves the data from the POST request
    data = request.get_json()

    # Check if the data consists of the required field
    if "forge_url" in data:

        try:
            res = DBMap.get_interfaces_exact_match(forge_url=data["forge_url"])
            return jsonify(res)
        except Error as error:
            return error.get_error_resp()
        except Exception as error:
            print(error)
            raise error
    # If all else fails, throw an error.
    return F_D_INVALID_PAYLOAD.get_error_resp()
