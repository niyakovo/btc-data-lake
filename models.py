from sqlalchemy import Column, Integer, Float, String, DateTime
from database import Base


class DBBTCPrice(Base):
    __tablename__ = "btc_price"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True, unique=True)
    price = Column(Float)