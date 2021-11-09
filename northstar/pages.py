"""
Search page
"""
# Bridges software forges to create a distributed software development environment
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
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import subprocess
from flask import Blueprint, render_template

VERSION = "0.1.0"
instance_maintainer = "foo@example.com"
GIT_HASH = subprocess.run(
    ["git", "rev-parse", "HEAD"], capture_output=True
).stdout.decode("utf-8")
GITHUB_LINK = f"https://github.com/forgefedv2/northstar/tree/{GIT_HASH}"

bp = Blueprint("STATIC_PAGES", __name__, url_prefix="/")


@bp.route("/", methods=["GET"])
def get_search_page():
    """Search Page"""
    return render_template(
        "index.html",
        version=VERSION,
        admin_email=instance_maintainer,
        git_hash=GIT_HASH[0:10],
        github_link=GITHUB_LINK,
    )
