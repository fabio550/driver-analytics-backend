create table if not exists postal_codes (
  postal_code text primary key,
  district_id integer not null,
  lat real,
  lng real
);

create table if not exists districts (
  id integer primary key,
  zone_id integer not null,
  name text not null, -- Pinheiros, Sé, Osasco, Itaquera, Mogi das Cruzes, etc
  type text not null, -- sp_district | municipality
  city text not null,
  center_lat real,
  center_lng real,
  polygon text -- GeoJSON serializado, opcional por enquanto
);

create table if not exists zones (
  id integer primary key,
  name text not null,
  type text not null, -- sao_paulo_macro_region | metro_region
  center_lat real,
  center_lng real,
  polygon text -- GeoJSON serializado, opcional por enquanto
);

create index if not exists idx_postal_codes_district 
  on postal_codes(district_id);

create index if not exists idx_districts_zone 
  on districts(zone_id);