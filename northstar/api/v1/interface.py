"""
Interface related routes
"""
# North Star ---  A lookup service for forged fed ecosystem
# Copyright © 2021 Aravinth Manivannan <realaravinth@batsense.net
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from urllib.parse import urlparse, urlunparse

import requests
from flask import Blueprint, jsonify, request

from northstar.db import get_db
from .errors import Error

bp = Blueprint("API_V1_INTERFACE", __name__, url_prefix="/interface")


F_D_EMPTY_FORGE_LIST = Error(
    errcode="F_D_EMPTY_FORGE_LIST", error="The forge list submited is empty", status=400
)
F_D_INTERFACE_UNREACHABLE = Error(
    errcode="F_D_INTERFACE_UNREACHABLE",
    error="The interface was unreachable with the publicly accessible URL provided",
    status=503,
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
        return "versions" in data and len(data["versions"]) is not 0
    return False


@bp.route("/register", methods=["POST"])
def register():
    """Regiter interface"""

    data = request.get_json()
    if "forge_url" in data and "interface_url" in data:
        forge_url = data["forge_url"]
        interface_url = clean_url(data["interface_url"])
        if not_url(interface_url):
            resp = jsonify({})
            resp.status = 400
            return resp

        if len(forge_url) == 0:
            return F_D_EMPTY_FORGE_LIST.get_error_resp()

        new_forge_url = []
        for forge in forge_url:
            url = clean_url(forge)
            if not_url(url):
                resp = jsonify({})
                resp.status = 400
                return resp
            new_forge_url.append(url)

        forge_url = new_forge_url

        if not verify_interface_online(interface_url):
            return F_D_INTERFACE_UNREACHABLE.get_error_resp()

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

    resp = jsonify({})
    resp.status = 400
    return resp
