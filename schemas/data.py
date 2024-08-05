from pydantic import BaseModel
from datetime import datetime


class DataSchema(BaseModel):
    user_id: int
    choice_id: int
    datetime: datetime
    location: str
    information: str
