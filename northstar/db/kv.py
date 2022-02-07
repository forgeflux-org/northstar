# North Star ---  A lookup service for forged fed ecosystem
# Copyright © 2022 G V Datta Adithya <dat.adithya@gmail.com>
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
from northstar.utils import clean_url, not_url, verify_interface_online
from northstar.errors import (
    F_D_EMPTY_FORGE_LIST,
    F_D_INVALID_PAYLOAD,
    F_D_INTERFACE_UNREACHABLE,
    F_D_NOT_URL,
    F_D_NO_REGISTERED_INTERFACES,
)

from .conn import get_db


class DBMap:
    @staticmethod
    def register(forge_urls: [str], interface_url: str):
        interface_url = clean_url(interface_url)
        if not_url(interface_url):
            raise F_D_NOT_URL

        if len(forge_urls) == 0:
            raise F_D_EMPTY_FORGE_LIST

        new_forge_url = []
        for forge in forge_urls:
            url = clean_url(forge)
            if not_url(url):
                raise F_D_NOT_URL
            new_forge_url.append(url)

        forge_url = new_forge_url

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

            cur.execute(
                """
            INSERT OR IGNORE INTO
                fts_interface_forge (forge_url, interface_url)
            VALUES ( ?, ? );""",
                (forge, interface_url),
            )

        conn.commit()

    @staticmethod
    def get_interfaces_exact_match(forge_url: str) -> [str]:
        """requirers forge_url to be valid URL"""
        # Check if the given forge_url is valid
        if len(forge_url) == 0 or not_url(forge_url):
            raise F_D_NOT_URL

        # Connect to the database
        conn = get_db()
        cur = conn.cursor()

        # Retrieve the interface and forge from the database
        interface_results = cur.execute(
            "SELECT interface_url FROM northstar_lookup WHERE forge_url = (?)",
            (clean_url(forge_url),),
        ).fetchall()
        conn.commit()

        # Check if we received any results
        if len(interface_results) == 0:
            raise F_D_NO_REGISTERED_INTERFACES

        res = []
        for r in interface_results:
            res.append(r[0])
        return res

    @staticmethod
    def get_interfaces_partial_match(forge_url: str):
        conn = get_db()
        cur = conn.cursor()

        if not forge_url.startswith('"'):
            forge_url = f'"{forge_url}'

        if not forge_url.endswith('"'):
            forge_url = f'{forge_url}"'

        # Retrieve the interface and forge from the database
        interface_results = cur.execute(
            "SELECT interface_url FROM fts_interface_forge WHERE forge_url MATCH (?)",
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
