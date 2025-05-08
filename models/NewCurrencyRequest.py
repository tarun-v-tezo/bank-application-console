from dataclasses import dataclass

@dataclass
class NewCurrencyRequest:
    currencyCode: str
    currencyName: str
    symbol: str
    exchangeRate: float