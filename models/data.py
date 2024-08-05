from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, DateTime, Text
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class Data(Base):
    __tablename__ = "data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    # user = relationship("User", back_populates="data")
    choice_id = Column(Integer, ForeignKey("choice.id"))
    # choice = relationship("Choice", back_populates="data")
    datetime = Column(DateTime)
    location = Column(String(length=255))
    information = Column(Text)
    image = Column(String(length=255))
