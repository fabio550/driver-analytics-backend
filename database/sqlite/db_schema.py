
import sqlite3


def create_tables(conn: sqlite3.Connection):
    conn.executescript("""
        create table if not exists zones (
            id         integer primary key,
            name       text not null,
            type       text not null,
            center_lat real,
            center_lng real,
            polygon    text
        );

        create table if not exists districts (
            id         integer primary key,
            zone_id    integer not null,
            name       text not null,
            type       text not null,
            city       text not null,
            center_lat real,
            center_lng real,
            polygon    text
        );

        create table if not exists postal_codes (
            postal_code text primary key,
            district_id integer not null
        );

        create index if not exists idx_postal_codes_district
            on postal_codes(district_id);

        create index if not exists idx_districts_zone
            on districts(zone_id);
    """)
    conn.commit()
    print("✓ Schema criado")
