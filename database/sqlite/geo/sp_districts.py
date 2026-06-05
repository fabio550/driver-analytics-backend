import json
import sqlite3
from database.sqlite.geo.zones import ZONA_MAP
from shapely.geometry import shape, Point
import geopandas as gpd

def insert_sp_districts(conn: sqlite3.Connection, geojson_path: str) -> list:
    """
    Retorna lista de (district_id, shapely_polygon) para uso no geo lookup.
    """

    gdf = gpd.read_file(geojson_path)

    print(f"CRS GeoSampa: {gdf.crs}")

    # Converte para WGS84 (lat/lng)
    if gdf.crs and gdf.crs.to_epsg() != 4326:
        gdf = gdf.to_crs(epsg=4326)

    districts_for_lookup = []
    inserted = 0

    for i, (_, row) in enumerate(gdf.iterrows(), start=1):

        name = row["nm_distrito_municipal"].title()
        zona_str = row.get("nm_regiao_05", "Centro")
        zone_id = ZONA_MAP.get(zona_str, 1)

        polygon = row.geometry
        centroid = polygon.centroid

        polygon_json = json.dumps(polygon.__geo_interface__)

        conn.execute("""
            insert or ignore into districts
                (id, zone_id, name, type, city, center_lat, center_lng, polygon)
            values (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            i,
            zone_id,
            name,
            'sp_district',
            'São Paulo',
            centroid.y,
            centroid.x,
            polygon_json,
        ))

        districts_for_lookup.append((i, polygon))
        inserted += 1

    conn.commit()
    print(f"✓ {inserted} distritos de SP capital inseridos")
    return districts_for_lookup