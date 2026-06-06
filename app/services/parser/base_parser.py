from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ParsedRide:
    started_at: datetime
    service_type: str
    status: str
    fare_brl: float
    surge_brl: float | None
    tip_brl: float | None
    duration_seconds: int | None
    distance_km: float | None
    pickup_postal_code: str | None
    destination_postal_code: str | None
    raw_ocr_text: str


class BaseParser(ABC):

    @abstractmethod
    def parse(self, raw_text: str) -> list[ParsedRide]:
        """
        Recebe texto bruto extraído pelo ML Kit.
        Retorna lista de corridas parseadas.
        """
        pass

    @abstractmethod
    def can_parse(self, raw_text: str) -> bool:
        """
        Retorna True se esse parser consegue processar o texto.
        Usado pelo parser_factory para escolher o parser certo.
        """
        pass