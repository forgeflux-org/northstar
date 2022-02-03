""" Test static pages"""
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
from flask import Response

from northstar.api.v1.errors import F_D_INVALID_PAYLOAD

from test_utils import expect_error, get_nodeinfo_index, get_nodeinfo_resp


def test_get_search(client):
    """Test interface registration handler"""
    response = client.get("/")
    assert response.status == "200 OK"


def test_get_openapi_docs(client):
    """Test interface registration handler"""
    response = client.get("/docs/openapi/")
    assert response.status == "200 OK"


def test_search(client, requests_mock):
    """Test interface registration handler"""

    base = "https://interface.example.com"
    (interface_url, resp) = get_nodeinfo_index(base)
    requests_mock.get(interface_url, json=resp)
    requests_mock.get(resp["links"][0]["href"], json=get_nodeinfo_resp())

    forges = ["https://forge.example.com", "ssh://forge.example.com"]
    interface_exists = {"interface_url": interface_url, "forge_url": forges}
    response = client.post("/api/v1/interface/register", json=interface_exists)

    response = client.post("/search", data={"search": "foo"})
    assert response.status_code == 404
    page = response.data.decode("utf-8")
    assert "Found no results" in page

    response: Response = client.post("/search", data={"search": forges[0]})
    assert response.status_code == 200
    page = response.data.decode("utf-8")
    assert "Found 1 item" in page
    assert base in page

    response: Response = client.post("/search")
    assert expect_error(response, F_D_INVALID_PAYLOAD)
