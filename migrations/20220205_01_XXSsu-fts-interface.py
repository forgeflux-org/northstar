"""
fts-interface
"""

from yoyo import step

__depends__ = {'20211005_01_GYn5b-lookup-view'}

steps = [
    step("""
        CREATE VIRTUAL TABLE IF NOT EXISTS fts_interface_forge
        USING FTS5(forge_url, interface_url);
        """)
]
