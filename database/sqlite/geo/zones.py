import sqlite3

# ─── Zonas definidas manualmente para SP capital ───────────────────────────────
# Baseado em nm_regiao_05 do GeoSampa
ZONA_MAP = {
    'Centro':  1,
    'Norte':   2,
    'Sul':     3,
    'Leste':   4,
    'Oeste':   5,
}

ZONES = [
    (1, 'Centro',          'sao_paulo_macro_region'),
    (2, 'Zona Norte',      'sao_paulo_macro_region'),
    (3, 'Zona Sul',        'sao_paulo_macro_region'),
    (4, 'Zona Leste',      'sao_paulo_macro_region'),
    (5, 'Zona Oeste',      'sao_paulo_macro_region'),
    (6, 'Grande SP',       'metro_region'),
]

# ─── Popula zones ──────────────────────────────────────────────────────────────
def insert_zones(conn: sqlite3.Connection):
    conn.executemany(
        "insert or ignore into zones (id, name, type) values (?, ?, ?)",
        ZONES
    )
    conn.commit()
    print(f"✓ {len(ZONES)} zones inseridas")

