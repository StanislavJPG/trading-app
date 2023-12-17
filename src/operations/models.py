from sqlalchemy import Integer, Column, String, TIMESTAMP
from sqlalchemy.orm import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()


class Operations(Base):
    __tablename__ = 'operations'

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    figi = Column(String)
    instrument_type = Column(String, nullable=True)
    date = Column(TIMESTAMP)
    type = Column(String)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
