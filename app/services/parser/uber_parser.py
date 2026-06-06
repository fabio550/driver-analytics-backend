import re
from datetime import datetime
from app.services.parser.base_parser import BaseParser, ParsedRide


# ─── Regex patterns ────────────────────────────────────────────────────────────

# R$ 23,67
RE_FARE = re.compile(r'^R\$\s+(\d+[.,]\d{2})$')

# R$ 2,50 Preço dinâmico
RE_SURGE = re.compile(
    r'^R\$\s*(\d+[.,]\d{2})\s+Preço\s+dinâmico',
    re.IGNORECASE
)

# R$ 5,00 Valor extra (valor a mais deixado pelo usuário)
RE_TIP = re.compile(
    r'^R\$\s*(\d+[.,]\d{2})\s+Valor\s+extra',
    re.IGNORECASE
)
# Uber X · 16 min 10 segundos · 6.31 km
# Comfort · 44 min 47 seg · 22,65 km
# Uber Moto · 8 min 30 seg · 3 km
# Uber X · Você cancelou
# Uber X · Cancelado pelo usuário

SEP = r'(?:·|•|-|\*)'

RE_SERVICE = re.compile(
    rf'^(.+?)\s+{SEP}\s+'
    rf'(?:(\d+)\s+min\s+(\d+)\s+(?:segundos?|segs?)\s+{SEP}\s+(\d+(?:[.,]\d+)?)\s+km'
    rf'|(Você cancelou|Cancelado pelo usuário))$'
)

# sáb., 23 de mai.
RE_DATE = re.compile(
    r'^(?:seg|ter|qua|qui|sex|sáb|dom)\.,?\s+(\d{1,2})\s+de\s+'
    r'(jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez)\.?$',
    re.IGNORECASE
)

# 23:44 ou 0:20
RE_TIME = re.compile(r'\b(\d{1,2}):(\d{2})\b')

# CEP: 04077-900
RE_CEP = re.compile(r'(\d{5}-\d{3})')

MONTHS = {
    'jan': 1,
    'fev': 2,
    'mar': 3,
    'abr': 4,
    'mai': 5,
    'jun': 6,
    'jul': 7,
    'ago': 8,
    'set': 9,
    'out': 10,
    'nov': 11,
    'dez': 12,
}


# ─── Helpers ───────────────────────────────────────────────────────────────────

def parse_brl(value: str) -> float:
    return float(value.replace('.', '').replace(',', '.'))


def parse_duration(minutes: str, seconds: str) -> int:
    return int(minutes) * 60 + int(seconds)


def parse_distance(value: str) -> float:
    return float(value.replace(',', '.'))


def normalize_status(raw_status: str | None) -> str:
    if raw_status is None:
        return 'completed'

    if raw_status == 'Você cancelou':
        return 'cancelled_by_driver'

    if raw_status == 'Cancelado pelo usuário':
        return 'cancelled_by_rider'

    return 'unknown'


def infer_year(month: int, day: int) -> int:
    """
    Assume que screenshots são recentes.
    Se a data calculada ficar muito no futuro,
    assume que pertence ao ano anterior.
    """
    now = datetime.now()
    year = now.year

    try:
        candidate = datetime(year, month, day)
    except ValueError:
        return year

    if (candidate - now).days > 30:
        year -= 1

    return year


# ─── Parser ────────────────────────────────────────────────────────────────────

class UberParser(BaseParser):

    def can_parse(self, raw_text: str) -> bool:
        return 'Uber' in raw_text or 'Comfort' in raw_text

    def parse(self, raw_text: str) -> list[ParsedRide]:
        lines = [l.strip() for l in raw_text.splitlines() if l.strip()]

        rides = []
        current_date = None

        i = 0

        while i < len(lines):
            line = lines[i]

            date_match = RE_DATE.match(line)
            if date_match:
                day = int(date_match.group(1))
                month = MONTHS[date_match.group(2).lower()]

                current_date = (day, month)

                i += 1
                continue

            fare_match = RE_FARE.match(line)

            if fare_match and current_date:
                fare_brl = parse_brl(fare_match.group(1))

                surge_brl = None
                tip_brl = None

                service_type = None
                status = 'completed'

                duration_secs = None
                distance_km = None

                pickup_cep = None
                dest_cep = None

                ride_time = None

                raw_lines = [line]

                i += 1

                while i < len(lines):
                    l = lines[i]
                    raw_lines.append(l)

                    surge_match = RE_SURGE.match(l)
                    if surge_match:
                        surge_brl = parse_brl(surge_match.group(1))
                        i += 1
                        continue

                    tip_match = RE_TIP.match(l)
                    if tip_match:
                        tip_brl = parse_brl(tip_match.group(1))
                        i += 1
                        continue

                    svc_match = RE_SERVICE.match(l)

                    if svc_match:
                        service_type = svc_match.group(1).strip()

                        status = normalize_status(
                            svc_match.group(5)
                        )

                        if status == 'completed':
                            duration_secs = parse_duration(
                                svc_match.group(2),
                                svc_match.group(3),
                            )

                            distance_km = parse_distance(
                                svc_match.group(4)
                            )

                        time_match = RE_TIME.search(l)

                        if not time_match and i + 1 < len(lines):
                            next_line = lines[i + 1]

                            time_match = RE_TIME.match(next_line)

                            if time_match:
                                i += 1

                        if time_match:
                            ride_time = (
                                int(time_match.group(1)),
                                int(time_match.group(2)),
                            )

                        i += 1
                        continue

                    cep_match = RE_CEP.search(l)

                    if cep_match:
                        cep = cep_match.group(1)

                        if pickup_cep is None:
                            pickup_cep = cep
                        else:
                            dest_cep = cep

                        i += 1
                        continue

                    if RE_FARE.match(l) or RE_DATE.match(l):
                        break

                    i += 1

                started_at = None

                if current_date and ride_time:
                    day, month = current_date
                    year = infer_year(month, day)

                    try:
                        started_at = datetime(
                            year=year,
                            month=month,
                            day=day,
                            hour=ride_time[0],
                            minute=ride_time[1],
                        )
                    except ValueError:
                        pass

                if service_type and started_at:
                    rides.append(
                        ParsedRide(
                            started_at=started_at,
                            service_type=service_type,
                            status=status,
                            fare_brl=fare_brl,
                            surge_brl=surge_brl,
                            tip_brl=tip_brl,
                            duration_seconds=duration_secs,
                            distance_km=distance_km,
                            pickup_postal_code=pickup_cep,
                            destination_postal_code=dest_cep,
                            raw_ocr_text='\n'.join(raw_lines),
                        )
                    )

                continue

            i += 1

        return rides