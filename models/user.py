from sqlalchemy.schema import Column
from sqlalchemy.types import String, Boolean, Integer, Enum
from database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=100), unique=True, nullable=False)
    password = Column(String(length=300), nullable=False)
    first_name = Column(String(length=255), nullable=False)
    last_name = Column(String(length=255))
    role = Column(Enum('admin', 'user'), nullable=False)
    is_active = Column(Boolean, default=True)
