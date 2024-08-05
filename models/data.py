from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, DateTime, Text
from database import Base
from sqlalchemy import ForeignKey


class Data(Base):
    __tablename__ = "data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    choice_id = Column(Integer, ForeignKey("choice.id"))
    datetime = Column(DateTime)
    location = Column(String(length=255))
    information = Column(Text)
