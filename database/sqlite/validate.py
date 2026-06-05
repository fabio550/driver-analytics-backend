import sqlite3

conn = sqlite3.connect('database/geo.db')

# Contagens
print("\n── Contagens ────────────────────────────────────")
print(f"zones:         {conn.execute('select count(*) from zones').fetchone()[0]}")
print(f"districts:     {conn.execute('select count(*) from districts').fetchone()[0]}")
print(f"postal_codes:  {conn.execute('select count(*) from postal_codes').fetchone()[0]}")

# Zones
print("\n── Zones ────────────────────────────────────────")
for row in conn.execute('select id, name, type from zones'):
    print(f"  {row[0]:2} | {row[1]:20} | {row[2]}")

# Districts por zone
print("\n── Districts por zone ───────────────────────────")
for row in conn.execute("""
    select z.name, count(d.id), d.type
    from zones z
    join districts d on d.zone_id = z.id
    group by z.name, d.type
    order by z.id
"""):
    print(f"  {row[0]:20} | {row[1]:3} districts | {row[2]}")

# Amostra de districts SP capital
print("\n── Amostra SP capital ───────────────────────────")
for row in conn.execute("""
    select d.name, d.type, z.name, d.center_lat, d.center_lng
    from districts d
    join zones z on z.id = d.zone_id
    where d.type = 'sp_district'
    limit 10
"""):
    print(f"  {row[0]:20} | {row[2]:15} | {row[3]:.4f}, {row[4]:.4f}")

# Amostra RMSP
print("\n── Amostra Grande SP ────────────────────────────")
for row in conn.execute("""
    select d.name, d.center_lat, d.center_lng
    from districts d
    where d.type = 'municipality'
"""):
    print(f"  {row[0]:25} | {row[1]:.4f}, {row[2]:.4f}")

# Verifica districts sem centroide
print("\n── Districts sem centroide ──────────────────────")
missing = conn.execute("""
    select count(*) from districts
    where center_lat is null or center_lng is null
""").fetchone()[0]
print(f"  {missing} districts sem centroide")

conn.close()
print("\n✓ Validação concluída\n")