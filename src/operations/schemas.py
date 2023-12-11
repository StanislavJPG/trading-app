from datetime import datetime

from pydantic import BaseModel


class OperationCreate(BaseModel):
    __tablename__ = 'operations'

    id: int
    quantity: str
    figi: str
    instrument_type: str
    date: datetime
    type: str
