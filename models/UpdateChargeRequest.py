from dataclasses import dataclass
from typing import Optional


@dataclass
class UpdateChargeRequest:
    bankId: str
    rtgs: Optional[float] = None
    imps: Optional[float] = None
    ortgs: Optional[float] = None
    oimps: Optional[float] = None