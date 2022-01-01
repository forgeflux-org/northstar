""" Test lookup handler"""
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
from urllib.parse import urlparse, urlunparse

from northstar.app import create_app
from northstar.api.v1.errors import (
    F_D_EMPTY_FORGE_LIST,
    F_D_INVALID_PAYLOAD,
    F_D_INTERFACE_UNREACHABLE,
    F_D_NOT_URL,
    F_D_NO_REGISTERED_INTERFACES,
)
from northstar.api.v1.interface import clean_url, not_url
from northstar.api.v1.interface import verify_interface_online

from test_utils import expect_error


def lookup(client, payload: str):
    payload = {"forge_url": payload}
    return client.post("/api/v1/forge/interfaces", json=payload)


def test_lookup(client, requests_mock):
    """Test interface registration handler"""

    interface_url = "https://interface.example.com/_ff/interface/versions"
    resp = {"versions": ["v0.1.0"]}
    requests_mock.get(interface_url, json=resp)

    forges = ["https://forge.example.com", "ssh://forge.example.com"]

    interface_exists = {"interface_url": interface_url, "forge_url": forges}

    resp = client.post("/api/v1/forge/interfaces", json={})
    assert expect_error(resp, F_D_INVALID_PAYLOAD)

    resp = lookup(client, forges[0])
    assert expect_error(resp, F_D_NO_REGISTERED_INTERFACES)

    resp = lookup(client, "foo")
    assert expect_error(resp, F_D_NOT_URL)

    response = client.post("/api/v1/interface/register", json=interface_exists)
    assert response.status == "200 OK"

    for f in forges:
        resp_interface = lookup(client, f).json
        assert clean_url(interface_url) in resp_interface
