from sqlalchemy.schema import Column
from sqlalchemy.types import String, Boolean, Integer
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("role.id"))
    # role = relationship("Role", back_populates="user")
    username = Column(String(length=100), unique=True, nullable=False)
    password = Column(String(length=300), nullable=False)
    first_name = Column(String(length=255), nullable=False)
    last_name = Column(String(length=255))
    is_active = Column(Boolean)
    # role = Column(Integer, nullable=False)
    # data = relationship("Data", back_populates="user")
