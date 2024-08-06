from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, DateTime, Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime

class MasterData(Base):
    __tablename__ = "master_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    description = Column(Text, nullable=True)
    location = Column(Text, nullable=False)  # Mengubah dari POINT menjadi TEXT
    origin_filepath = Column(String(255), nullable=True)
    thumbnail_filepath = Column(String(255), nullable=True)
    upload_date = Column(DateTime, default=datetime.datetime.utcnow)

    # user = relationship("User", back_populates="master_data")
