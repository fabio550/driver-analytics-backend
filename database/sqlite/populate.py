"""
populate.py — popula o banco SQLite de geo lookup

Fontes:
  - GeoSampa: distritos de SP capital (96 distritos)
  - IBGE: municípios da Grande SP (RMSP)

Uso:
  python -m database.sqlite.populate
"""

import sqlite3
import argparse

from database.sqlite.geo.rmsp_districts import populate_rmsp_districts
from database.sqlite.db_schema import setup_db
from database.sqlite.geo.sp_districts import populate_sp_districts
from database.sqlite.geo.zones import populate_zones


def main():
    parser = argparse.ArgumentParser(description='Popula banco SQLite de geo lookup')

    parser.add_argument('--geosampa',
        default='database/data/geoportal_distrito_municipal_v2.geojson',
        help='Caminho para o GeoJSON do GeoSampa')

    parser.add_argument('--ibge',
        default='database/data/SP_Municipios_2025.zip',
        help='Caminho para o ZIP do IBGE')

    parser.add_argument('--db',
        default='database/geo.db',
        help='Caminho para o arquivo SQLite de saída')

    args = parser.parse_args()

    conn = sqlite3.connect(args.db)

    print("\n── Inicializando banco ──────────────────────────")
    setup_db(conn)

    print("\n── Inserindo zones ──────────────────────────────")
    populate_zones(conn)

    print("\n── Inserindo distritos SP capital (GeoSampa) ───")
    sp_districts = populate_sp_districts(conn, args.geosampa)

    print("\n── Inserindo municípios Grande SP (IBGE) ───────")
    rmsp_districts = populate_rmsp_districts(conn, args.ibge, start_id=len(sp_districts) + 1)

    all_districts = sp_districts + rmsp_districts

    print(f"\n── Total de districts: {len(all_districts)} ──────────────────")

    conn.close()
    print("\n✓ Banco populado com sucesso\n")


if __name__ == '__main__':
    main()