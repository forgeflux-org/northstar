"""
Lookup related routes
"""
# North Star ---  A lookup service for forged fed ecosystem
# Copyright © 2021 Aravinth Manivannan <realaravinth@batsense.net>
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
from urllib.parse import urlparse, urlunparse

import requests
from flask import Blueprint, jsonify, request

from northstar.db import get_db
from .errors import Error

bp = Blueprint("API_V1_INTERFACE", __name__, url_prefix="/forge")

F_D_NO_REGISTERED_INTERFACES = Error(
    errcode="F_D_NO_REGISTERED_INTERFACES",
    error="No interfaces are registered against the queried forge",
    status=400,
)

F_D_INTERNAL_SERVER_ERROR = Error(
    errcode="F_D_INTERNAL_SERVER_ERROR",
    error="Operation could not be performed due to internal errors.",
    status=500,
)


def clean_url(url: str):
    """Remove paths and tracking elements from URL"""
    parsed = urlparse(url)
    cleaned = urlunparse((parsed.scheme, parsed.netloc, "", "", "", ""))
    return cleaned


def not_url(url: str):
    """Check if the URL pased is indeed a URL"""
    parsed = urlparse(url)
    return (
        len(parsed.scheme) == 0
        or len(parsed.netloc) == 0
        or parsed.netloc == "localhost"
    )


def verify_interface_online(url: str):
    """Verify if interface instance is reachable"""
    parsed = urlparse(url)
    path = "/_ff/interface/versions"
    url = urlunparse((parsed.scheme, parsed.netloc, path, "", "", ""))
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        return "versions" in data and len(data["versions"]) != 0
    return False


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
            return F_D_NO_REGISTERED_INTERFACES.get_error_resp()

        # Connect to the database
        conn = get_db()
        cur = conn.cursor()

        # Retrieve the interface and forge from the database
        interface_results = cur.execute(
            "SELECT interface_url, forge_url FROM northstar_lookup WHERE forge_url = (?)",
            (clean_url(forge_url),),
        ).fetchall()
        conn.commit()

        # Check if we received any results
        if len(interface_results) == 0:
            return F_D_NO_REGISTERED_INTERFACES.get_error_resp()

        # Return retrieved interfaces and forges
        return jsonify({"results": [{res[0]: res[1]} for res in interface_results]})

    # If all else fails, throw an error.
    return F_D_INTERNAL_SERVER_ERROR
