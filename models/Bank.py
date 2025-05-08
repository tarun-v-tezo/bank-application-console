from dataclasses import dataclass


@dataclass
class Bank:
    id: str
    name: str
    acceptedCurrencyIds: list[int]
    rtgs: float
    imps: float
    ortgs: float
    oimps: float