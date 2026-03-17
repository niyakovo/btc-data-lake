from pydantic import BaseModel
from datetime import datetime


class BTCPriceResponse(BaseModel):
    id: int
    timestamp: datetime
    price: float

    class Config:
        from_attributes = True