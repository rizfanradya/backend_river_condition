from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer
from database import Base
from sqlalchemy.orm import relationship


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    # user = relationship("User", back_populates="role")
    role = Column(String(length=100), unique=True, nullable=False)
