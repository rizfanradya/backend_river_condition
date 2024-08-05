from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer
from database import Base


class Choice(Base):
    __tablename__ = "choice"

    id = Column(Integer, primary_key=True, index=True)
    choice = Column(String(length=255), unique=True, nullable=False)
