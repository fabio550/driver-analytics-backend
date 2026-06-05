create table rides (
    id uuid primary key default gen_random_uuid(),
    shift_id uuid references shifts(id),
    dedup_hash text unique not null,
    started_at timestamp with time zone not null,
    app text not null,
    service_type text not null,
    status text not null,
    fare_brl float not null,
    surge_brl float,
    tip_brl float,
    duration_seconds int,
    distance_km float,
    pickup_postal_code text,
    destination_postal_code text,
    raw_ocr_text text not null,
    imported_at timestamp with time zone default now()
);