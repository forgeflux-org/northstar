"""
Interfaces and forges
"""

from yoyo import step

__depends__ = {}

steps = [
    step("""
    CREATE TABLE IF NOT EXISTS northstar_interfaces (
        URL VARCHAR(3000) NOT NULL UNIQUE,
        ID INTEGER PRIMARY KEY NOT NULL
    )"""),
    step("""
    CREATE TABLE IF NOT EXISTS northstar_forges (
        URL VARCHAR(3000) NOT NULL UNIQUE,
        ID INTEGER PRIMARY KEY NOT NULL
    )"""),
    step("""
    CREATE TABLE IF NOT EXISTS northstar_interface_forge_directory (
        forge_id INTEGER NOT NULL REFERENCES northstar_forges(ID) ON DELETE CASCADE,
        interface_id INTEGER NOT NULL REFERENCES northstar_forges(ID) ON DELETE CASCADE
    )""")
]
