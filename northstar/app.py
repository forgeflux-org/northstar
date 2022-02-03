"""
North Star Application
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os

from flask import Flask

from . import db
from .api import V1_bp
from .pages import bp as pages


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config:
        app.config.from_mapping(test_config)

    if "DATABASE" not in app.config:
        app.config.from_mapping(
            DATABASE=os.path.join(app.instance_path, "northstar.db"),
        )

    try:
        os.makedirs(app.instance_path)
        db.init_app(app)
    except OSError:
        pass

    @app.after_request
    def flock_google(response):
        response.headers["Permissions-Policy"] = "interest-cohort=()"
        return response

    app.register_blueprint(V1_bp)
    app.register_blueprint(pages)
    return app
