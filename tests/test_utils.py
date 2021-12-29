""" Test utils"""
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from northstar.api.v1.errors import Error
from northstar.api.v1.utils import trim_url


def expect_error(response, err: Error) -> bool:
    """Test responses"""
    data = response.json
    return all(
        [
            str(err.status()) in response.status,
            err.get_error()["error"] == data["error"],
            err.get_error()["errcode"] == data["errcode"],
        ]
    )


def test_trim_url():
    """Test trim_url"""

    url = "https://example.com"
    assert trim_url(url) == url
    assert trim_url(f"{url}/") == url

    path = "/foo/bar"
    assert trim_url(path) == path
    assert trim_url(f"{path}/") == path
