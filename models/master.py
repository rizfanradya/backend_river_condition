from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, DateTime, Text, Enum
from sqlalchemy import ForeignKey
from database import Base
import datetime
import pytz


class MasterData(Base):
    __tablename__ = "master_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    description = Column(Text)
    location = Column(Text)
    site_condition = Column(Enum('Bersih', 'Kotor'), default='Bersih')
    rivera_condition = Column(Enum('Pasang', 'Surut'), default='Pasang')
    riverb_condition = Column(
        Enum('Mengalir', 'Tidak Mengalir'), default='Mengalir')
    riverc_condition = Column(Enum('Cepat', 'Lambat'), default='Cepat')
    riverd_condition = Column(Enum('Bau', 'Tidak Bau'), default='Tidak Bau')
    rivere_condition = Column(
        Enum('Hitam', 'Hijau', 'Jernih', 'Putih Susu'), default='Jernih')
    weather_condition = Column(
        Enum('Berawan', 'Cerah', 'Hujan'), default='Cerah')
    upload_date = Column(DateTime, default=lambda: datetime.datetime.now(
        pytz.timezone('Asia/Jakarta')))
    file = Column(Text)
