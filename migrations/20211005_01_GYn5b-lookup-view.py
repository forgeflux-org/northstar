"""
lookup view
"""

from yoyo import step

__depends__ = {'20211002_01_HmaHC-interfaces-and-forges'}

steps = [
    step("""

        CREATE VIEW northstar_lookup (
            interface_url, forge_url
        )
        AS
        SELECT 
            interface.URL, forge.URL 
        FROM 
            northstar_interfaces interface,
            northstar_forges forge,
            northstar_interface_forge_directory dir
        WHERE 
            dir.forge_id = forge.ID
        AND
            dir.interface_id = interface.ID;
    """)
]
