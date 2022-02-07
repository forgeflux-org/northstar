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

from northstar.db import DBMap
from northstar.errors import (
    F_D_NOT_URL,
    F_D_INVALID_PAYLOAD,
    Error,
    F_D_INTERFACE_UNREACHABLE,
)
from northstar.utils import clean_url, not_url, verify_interface_online

bp = Blueprint("API_V1_INTERFACE", __name__, url_prefix="/interface")


@bp.route("/register", methods=["POST"])
def register():
    """Register interface"""

    data = request.get_json()

    try:
        if any(["forge_url" not in data, "interface_url" not in data]):
            raise F_D_INVALID_PAYLOAD

        interface_url = clean_url(data["interface_url"])
        if not_url(interface_url):
            raise F_D_NOT_URL

        if not verify_interface_online(interface_url):
            raise F_D_INTERFACE_UNREACHABLE

        DBMap.register(forge_urls=data["forge_url"], interface_url=interface_url)
        return jsonify({})
    except Error as error:
        return error.get_error_resp()
    except Exception as error:
        print(error)
        raise error
