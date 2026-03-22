from pydantic import BaseModel
from datetime import datetime
from typing import List


class BTCPriceResponse(BaseModel):
    id: int
    timestamp: datetime
    price: float

    class Config:
        from_attributes = True
    
class FileSelection(BaseModel):
    files:List[str]