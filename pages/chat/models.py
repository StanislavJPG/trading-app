from sqlalchemy import MetaData, Integer, Column, String
from sqlalchemy.orm import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()
metadata = MetaData()


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    message = Column(String(length=40))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
