from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, DateTime, Text, Enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime

class MasterData(Base):
    __tablename__ = "master_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    description = Column(Text, nullable=True)
    location = Column(Text, nullable=True)  # Changed from NOT NULL to allow for nullable
    site_condition = Column(Enum('Bersih', 'Kotor'), nullable=True, default='Bersih')
    rivera_condition = Column(Enum('Pasang', 'Surut'), nullable=True, default='Pasang')
    riverb_condition = Column(Enum('Mengalir', 'Tidak Mengalir'), nullable=True, default='Mengalir')
    riverc_condition = Column(Enum('Cepat', 'Lambat'), nullable=True, default='Cepat')
    riverd_condition = Column(Enum('Bau', 'Tidak Bau'), nullable=True, default='Tidak Bau')
    rivere_condition = Column(Enum('Hitam', 'Hijau', 'Jernih', 'Putih Susu'), nullable=True, default='Jernih')
    weather_condition = Column(Enum('Berawan', 'Cerah', 'Hujan'), nullable=True, default='Cerah')
    origin_filepath = Column(String(255), nullable=True)
    thumbnail_filepath = Column(String(255), nullable=True)
    upload_date = Column(DateTime, default=datetime.datetime.utcnow)

    # user = relationship("User", back_populates="master_data")
