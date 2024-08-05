from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer
from database import Base
from sqlalchemy import ForeignKey


class Image(Base):
    __tablename__ = "image"

    id = Column(Integer, primary_key=True, index=True)
    data_id = Column(Integer, ForeignKey("data.id"))
    image = Column(String(length=255))
