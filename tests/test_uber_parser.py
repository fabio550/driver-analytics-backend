from app.services.parser.uber_parser import UberParser

# Texto simulando o que o ML Kit entregaria
RAW_TEXT = RAW_TEXT = """
SEX., 05 de JUN.

R$ 18,92

Uber X • 14 min 32 seg • 5,87 km

18:43

R$ 2,25 Preço dinâmico

Rua Serra de Botucatu, Tatuape - Sao Paulo - SP, 03317-000, BR

Rua Itapura, Tatuape - Sao Paulo - SP, 03310-000, BR



R$ 0,00

Uber X - Cancelado pelo usuário

19:02

Rua Monte Serrat, Tatuape - Sao Paulo - SP, 03312-001, BR

Rua Cantagalo, Tatuape - Sao Paulo - SP, 03319-000, BR



R$ 12,47

Comfort * 9 min 48 segs * 3 km

20:11

R$ 3,00 Valor extra (valor a mais deixado pelo usuario)

Rua Antonio de Barros, Tatuape - Sao Paulo - SP, 03401-000, BR

Avenida Radial Leste, Vila Matilde - Sao Paulo - SP, 03502-000, BR


sáb., 6 de jun.

R$ 34,90

Uber Flash · 22 min 15 segundos · 11.4 km

08:17

Rua da Consolação, Consolacao - Sao Paulo - SP, 01302-000, BR

Avenida Brigadeiro Faria Lima, Itaim Bibi - Sao Paulo - SP, 04538-132, BR


R$ 27,35

Uber Moto • 18 min 09 seg • 8,6 km

13:54

R$ 1,50 Preço dinâmico

R$ 4,00 Valor extra

Rua Vergueiro, Liberdade - Sao Paulo - SP, 01504-001, BR

Praça da Se, Se - Sao Paulo - SP, 01001-000, BR


R$ 0,00

Uber Pet · Você cancelou

23:41

Rua Domingos de Morais, Vila Mariana - Sao Paulo - SP, 04010-100, BR

Rua Domingos de Morais, Vila Mariana - Sao Paulo - SP, 04010-100, BR


R$ 42,90

Uber Black - 21 min 44 seg - 11,2 km

23:58

R$ 6,50 Preço dinâmico

R$ 10,00 Valor extra (valor a mais deixado pelo usuário)

Rua Funchal, Vila Olimpia - Sao Paulo - SP, 04551-060, BR

Avenida Paulista, Bela Vista - Sao Paulo - SP, 01310-100, BR
"""

parser = UberParser()

print(f"can_parse: {parser.can_parse(RAW_TEXT)}")
print()

rides = parser.parse(RAW_TEXT)
print(f"Corridas encontradas: {len(rides)}")
print()

for i, ride in enumerate(rides, 1):
    print(f"── Corrida {i} ──────────────────────────")
    print(f"  started_at:    {ride.started_at}")
    print(f"  service_type:  {ride.service_type}")
    print(f"  status:        {ride.status}")
    print(f"  fare_brl:      {ride.fare_brl}")
    print(f"  surge_brl:     {ride.surge_brl}")
    print(f"  tip_brl:       {ride.tip_brl}")
    print(f"  duration_secs: {ride.duration_seconds}")
    print(f"  distance_km:   {ride.distance_km}")
    print(f"  pickup_cep:    {ride.pickup_postal_code}")
    print(f"  dest_cep:      {ride.destination_postal_code}")
    print()