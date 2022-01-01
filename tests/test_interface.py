""" Test interface handlers"""
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
)
from northstar.api.v1.interface import clean_url, not_url
from northstar.api.v1.interface import verify_interface_online
from northstar.db import get_db

from test_utils import expect_error


def test_interface_register(client, requests_mock):
    """Test interface registration handler"""

    interface_url = "https://interface.example.com/_ff/interface/versions"
    resp = {"versions": ["v0.1.0"]}
    requests_mock.get(interface_url, json=resp)

    forges = ["https://forge.example.com", "ssh://forge.example.com"]

    interface_exists = {"interface_url": interface_url, "forge_url": forges}

    conn = get_db()
    cur = conn.cursor()

    interface_id = None
    forge_ids = {}

    def get_interface_id(interface_url):
        return cur.execute(
            "SELECT ID FROM northstar_interfaces WHERE URL = ?",
            (clean_url(interface_url),),
        ).fetchone()[0]

    def get_forge_id(forge_url):
        return cur.execute(
            "SELECT ID FROM northstar_forges WHERE URL = ?", (clean_url(forge_url),)
        ).fetchone()[0]

    for i in range(2):
        response = client.post("/api/v1/interface/register", json=interface_exists)
        assert response.status == "200 OK"
        assert response.json == {}

        if i == 0:
            interface_id = get_interface_id(interface_url)
        else:
            assert interface_id == get_interface_id(interface_url)

        for forge in forges:
            forge_id = get_forge_id(forge)
            if i == 0:
                forge_ids[forge] = forge_id
            else:
                assert forge_ids[forge] == forge_id

            res = cur.execute(
                """
            SELECT EXISTS (
                SELECT 1 FROM northstar_interface_forge_directory
                WHERE forge_id = ? AND interface_id = ?
                );""",
                (forge_id, interface_id),
            ).fetchone()[0]
            assert res is 1


def test_interface_register_errors(client, requests_mock):
    """Test interface errors"""
    interface_url = "https://interface.example.com/_ff/interface/versions"
    resp = {"versions": ["v0.1.0"]}
    requests_mock.get(interface_url, json=resp)

    forges = ["https://forge.example.com", "ssh://forge.example.com"]

    interface_exists = {"interface_url": interface_url, "forge_url": forges}

    # not url
    not_url_payload = interface_exists
    not_url_payload["interface_url"] = "foo"
    response = client.post("/api/v1/interface/register", json=not_url_payload)
    assert expect_error(response, F_D_NOT_URL)

    not_url_payload["interface_url"] = interface_url
    not_forge_urls = forges
    not_forge_urls.append("foo")
    not_url_payload["forge_url"] = not_forge_urls
    response = client.post("/api/v1/interface/register", json=not_url_payload)
    assert expect_error(response, F_D_NOT_URL)

    ## empty request
    response = client.post("/api/v1/interface/register", json={})
    assert expect_error(response, F_D_INVALID_PAYLOAD)

    # Empty forge list error
    empty_forge_list = interface_exists
    empty_forge_list["forge_url"] = []
    response = client.post("/api/v1/interface/register", json=empty_forge_list)
    assert expect_error(response, F_D_EMPTY_FORGE_LIST)


def test_clean_url(client):
    """Test clean_url works"""
    urls = [
        "https://example.com/foo",
        "https://example.com/foo?q=sdf",
        "https://example.com",
    ]
    for url in urls:
        cleaned = urlparse(clean_url(url))
        assert cleaned.scheme == "https"
        assert cleaned.netloc == "example.com"
        assert cleaned.path == ""
        assert cleaned.query == ""


def test_verify_instance_online(client, requests_mock):
    interface_url = "https://interfac9.example.com/_ff/interface/versions"
    resp = {"versions": ["v0.1.0"]}
    requests_mock.get(interface_url, json=resp)

    assert verify_interface_online(clean_url(interface_url)) is True

    interface_url = "https://interface2.example.com/_ff/interface/versions"
    resp = {"versions": []}
    requests_mock.get(interface_url, json=resp)
    assert verify_interface_online(clean_url(interface_url)) is not True

    interface_url = "https://interface3.example.com/_ff/interface/versions"
    resp = {"versions": []}
    requests_mock.get(interface_url, json={})
    assert verify_interface_online(clean_url(interface_url)) is not True


def test_verify_instance_online_unreachable(client):
    """Test unreachable interface verification"""
    interface_url = "https://example.com"
    assert verify_interface_online(clean_url(interface_url)) is not True

    forges = ["https://forge.example.com", "ssh://forge.example.com"]

    interface_exists = {"interface_url": interface_url, "forge_url": forges}

    response = client.post("/api/v1/interface/register", json=interface_exists)
    expect_error(response, F_D_INTERFACE_UNREACHABLE)


def test_not_url(client):
    """Test not_url works"""
    urls = [
        "https://example.com/foo",
        "https://example.com/foo?q=sdf",
        "https://example.com",
    ]
    not_urls = ["foo", "2342"]
    for url in urls:
        assert not_url(url) is False
        cleaned = clean_url(url)
        assert not_url(cleaned) is False

    for url in not_urls:
        assert not_url(url) is True
        cleaned = clean_url(url)
        assert not_url(cleaned) is True
