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
import pytest

from northstar.db import DBMap
from northstar.errors import (
    F_D_NOT_URL,
    F_D_INVALID_PAYLOAD,
    Error,
    F_D_INTERFACE_UNREACHABLE,
    F_D_EMPTY_FORGE_LIST,
)


def test_db_map(app):
    interface_url = "https://interface.example.com"
    forges = ["https://forge.example.com", "ssh://forge.example.com"]
    DBMap.register(forge_urls=forges, interface_url=interface_url)
    for forge in forges:
        assert DBMap.get_interfaces_exact_match(forge)[0] == interface_url

    with pytest.raises(Error) as error:
        DBMap.register(forge_urls=forges, interface_url="foo")
    assert error, F_D_NOT_URL

    with pytest.raises(Error) as error:
        DBMap.register(forge_urls=[], interface_url=interface_url)
    assert error, F_D_EMPTY_FORGE_LIST

    with pytest.raises(Error) as error:
        DBMap.register(forge_urls=["foo"], interface_url=interface_url)
    assert error, F_D_NOT_URL
