from datetime import datetime

from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, Column, JSON, Boolean
from sqlalchemy.orm import DeclarativeMeta, declarative_base, relationship

Base: DeclarativeMeta = declarative_base()


class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    permissions = Column(JSON)
    user = relationship("src.auth.models.User")


class User(Base):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    role_id = Column(ForeignKey(Role.id))
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
