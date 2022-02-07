"""
Search page
"""
# Bridges software forges to create a distributed software development environment
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
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import subprocess
import sqlite3

from flask import (
    Blueprint,
    render_template,
    send_from_directory,
    request,
    make_response,
)
from dynaconf import settings

from northstar.db import get_db
from northstar.utils import trim_url, clean_url
from northstar.errors import (
    Error,
    F_D_NO_REGISTERED_INTERFACES,
    F_D_INVALID_PAYLOAD,
)

VERSION = "0.1.0"
GIT_HASH = subprocess.run(
    ["git", "rev-parse", "HEAD"], capture_output=True, check=True
).stdout.decode("utf-8")


GITHUB_LINK = f"{trim_url(settings.SOURCE_CODE)}/tree/{GIT_HASH}"

bp = Blueprint("STATIC_PAGES", __name__, url_prefix="")


@bp.route("/", methods=["GET"])
def index():
    """Index Page"""
    return render_template(
        "index.html",
        version=VERSION,
        admin_email=settings.INSTANCE_MAINTAINER,
        git_hash=GIT_HASH[0:10],
        github_link=GITHUB_LINK,
    )


def interface__lookup(forge_url: str):
    conn = get_db()
    cur = conn.cursor()

    # Retrieve the interface and forge from the database
    interface_results = cur.execute(
        "SELECT interface_url FROM northstar_lookup WHERE forge_url LIKE (?)",
        (forge_url,),
    ).fetchall()
    conn.commit()

    # Check if we received any results
    if len(interface_results) == 0:
        raise F_D_NO_REGISTERED_INTERFACES

    res = []
    for r in interface_results:
        res.append(r[0])
    return res


@bp.route("/search", methods=["POST"])
def search():
    """Search Page"""

    def no_res():
        res = make_response(
            render_template(
                "result.html",
                version=VERSION,
                admin_email=settings.INSTANCE_MAINTAINER,
                git_hash=GIT_HASH[0:10],
                github_link=GITHUB_LINK,
                interfaces=[],
                search_item=search_item,
            )
        )
        res.status = 404
        return res

    if "search" not in request.form:
        return F_D_INVALID_PAYLOAD.get_error_resp()

    search_item = request.form["search"]

    try:
        interfaces = interface__lookup(search_item)
        return render_template(
            "result.html",
            version=VERSION,
            admin_email=settings.INSTANCE_MAINTAINER,
            git_hash=GIT_HASH[0:10],
            github_link=GITHUB_LINK,
            interfaces=interfaces,
            search_item=search_item,
        )

    except Error as error:
        if error.errcode == F_D_NO_REGISTERED_INTERFACES.errcode:
            return no_res()
        return error.get_error_resp()

    except sqlite3.OperationalError as error:
        if "no such table: northstar_lookup" in error.args:
            return no_res()
        raise error


@bp.route("/docs/openapi/", methods=["GET"])
def get_openapi_docs():
    """OpenAPI Docs page"""
    return send_from_directory("static/docs/openapi", "index.html")
