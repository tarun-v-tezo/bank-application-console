from dataclasses import dataclass

@dataclass
class AcceptedCurrency:
    id: int
    currencyCode: str
    currencyName: str
    symbol: str
    exchangeRate: float