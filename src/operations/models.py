from sqlalchemy import MetaData, Integer, Column, String, TIMESTAMP
from sqlalchemy.orm import DeclarativeMeta, declarative_base


Base: DeclarativeMeta = declarative_base()
metadata = MetaData()


class Operations(Base):
    __tablename__ = 'operations'

    id = Column(Integer, primary_key=True)
    quantity = Column(String)
    figi = Column(String)
    instrument_type = Column(String, nullable=True)
    date = Column(TIMESTAMP)
    type = Column(String)
