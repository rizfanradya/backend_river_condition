from pydantic import BaseModel
from datetime import datetime

class MasterDataCreateSchema(BaseModel):
    user_id: int
    description: str
    location: str

class MasterDataResponseSchema(BaseModel):
    id: int
    user_id: int
    description: str
    location: str
    origin_filepath: str
    thumbnail_filepath: str
    upload_date: datetime

    # class Config:
    #     orm_mode = True
