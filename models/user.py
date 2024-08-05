from sqlalchemy.schema import Column
from sqlalchemy.types import String, Boolean, Integer
from database import Base
from sqlalchemy import ForeignKey


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("role.id"))
    username = Column(String(length=100), unique=True, nullable=False)
    password = Column(String(length=300), nullable=False)
    first_name = Column(String(length=255), nullable=False)
    last_name = Column(String(length=255))
    is_active = Column(Boolean)
