import json
import sqlite3
import geopandas as gpd

# ─── Municípios da Região Metropolitana de São Paulo ───────────────────────────
RMSP = {
    'São Paulo', 'Guarulhos', 'São Bernardo do Campo', 'Santo André',
    'Osasco', 'Mogi das Cruzes', 'Diadema', 'Carapicuíba', 'Itaquaquecetuba',
    'Taboão da Serra', 'Barueri', 'Suzano', 'Embu das Artes', 'Cotia',
    'Itapevi', 'Francisco Morato', 'Franco da Rocha', 'Mairiporã',
    'Santana de Parnaíba', 'Ferraz de Vasconcelos', 'Mauá',
    'São Caetano do Sul', 'Ribeirão Pires', 'Rio Grande da Serra',
    'Arujá', 'Biritiba Mirim', 'Guararema', 'Salesópolis',
    'Santa Isabel', 'Caieiras', 'Cajamar', 'Pirapora do Bom Jesus',
    'Vargem Grande Paulista', 'Jandira', 'Osasco', 'Poa',
    'Guarulhos', 'Guarujá'
}

# ─── Popula districts — Grande SP via IBGE ────────────────────────────────────
def insert_rmsp_districts(conn: sqlite3.Connection, ibge_path: str, start_id: int) -> list:
    """
    Municípios da RMSP viram districts do tipo 'municipality'.
    Retorna lista de (district_id, shapely_polygon) para uso no geo lookup.
    """
    gdf = gpd.read_file(ibge_path)

    # Converte CRS para WGS84 (lat/lng padrão)
    gdf = gdf.to_crs(epsg=4326)

    # Filtra só RMSP excluindo São Paulo capital (já coberta pelo GeoSampa)
    rmsp_gdf = gdf[
        gdf['NM_MUN'].isin(RMSP) & (gdf['NM_MUN'] != 'São Paulo')
    ]

    districts_for_lookup = []
    inserted = 0

    for i, (_, row) in enumerate(rmsp_gdf.iterrows(), start=start_id):
        name     = row['NM_MUN']
        polygon  = row['geometry']
        centroid = polygon.centroid

        polygon_geojson = json.dumps({
            'type': polygon.geom_type,
            'coordinates': list(polygon.__geo_interface__['coordinates'])
        })

        conn.execute("""
            insert or ignore into districts
                (id, zone_id, name, type, city, center_lat, center_lng, polygon)
            values (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            i,
            6,           # zone_id 6 = Grande SP
            name,
            'municipality',
            name,
            centroid.y,
            centroid.x,
            polygon_geojson,
        ))

        districts_for_lookup.append((i, polygon))
        inserted += 1

    conn.commit()
    print(f"✓ {inserted} municípios da Grande SP inseridos")
    return districts_for_lookup

