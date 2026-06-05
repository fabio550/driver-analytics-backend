create table shifts (
  id uuid primary key default gen_random_uuid(),
  started_at timestamp with time zone not null,
  ended_at timestamp with time zone not null,
  start_odometer_km float not null,
  end_odometer_km float not null,
  notes text,
  pauses jsonb default '[]'::jsonb,
  created_at timestamp with time zone default now()
);