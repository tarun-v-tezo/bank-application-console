from dataclasses import dataclass
from typing import Optional


@dataclass
class NewBankRequest:
    name: str
    rtgs: Optional[float] = None
    imps: Optional[float] = None
    ortgs: Optional[float] = None
    oimps: Optional[float] = None
    acceptedCurrencyIds: Optional[list[int]] = None