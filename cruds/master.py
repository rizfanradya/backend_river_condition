from sqlalchemy.orm import Session
from models.master import MasterData
from schemas.master import MasterDataCreateSchema, MasterDataResponseSchema
from typing import Optional, List
from sqlalchemy import or_
from fastapi import UploadFile, File
import os
import uuid
from PIL import Image as PILImage
import aiofiles
import datetime

async def save_file(file: UploadFile, destination: str):
    async with aiofiles.open(destination, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

def create_thumbnail(image_path: str, thumbnail_path: str, size=(128, 128)):
    with PILImage.open(image_path) as img:
        img.thumbnail(size)
        img.save(thumbnail_path)

async def CreateData(session: Session, new_data: MasterDataCreateSchema, file: UploadFile):
    try:
        MAX_FILE_SIZE_BYTES = 2 * 1024 * 1024  # 2MB
        allowed_content_types = ['image/jpeg', 'image/png']
        base_dir = os.path.dirname(os.path.abspath(__file__))
        upload_dir = os.path.join(base_dir, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)

        if file.content_type not in allowed_content_types:
            return {"error": "Wrong file type, only accept jpeg or png"}
        if os.fstat(file.file.fileno()).st_size > MAX_FILE_SIZE_BYTES:
            return {"error": "File too large, only accept file below 2MB"}

        file_extension = file.filename.split('.')[-1]
        filename = f'{uuid.uuid4()}.{file_extension}'
        origin_filepath = os.path.join(upload_dir, 'origin', filename)
        thumbnail_filepath = os.path.join(upload_dir, 'thumbnails', filename)

        os.makedirs(os.path.dirname(origin_filepath), exist_ok=True)
        os.makedirs(os.path.dirname(thumbnail_filepath), exist_ok=True)

        await save_file(file, origin_filepath)
        create_thumbnail(origin_filepath, thumbnail_filepath)

        location = f'{new_data.location}'  # Mengubah dari POINT ke TEXT

        new_data_info = MasterData(
            user_id=new_data.user_id,
            description=new_data.description,
            location=location,
            origin_filepath=origin_filepath,
            thumbnail_filepath=thumbnail_filepath,
            upload_date=datetime.datetime.utcnow()
        )
        session.add(new_data_info)
        session.commit()
        session.refresh(new_data_info)

        return MasterDataResponseSchema.from_orm(new_data_info)
    except Exception as error:
        return {"error": str(error)}

def GetAllData(session: Session, user_id: Optional[int] = None, limit: int = 10, offset: int = 0):
    query = session.query(MasterData)
    if user_id:
        query = query.filter(MasterData.user_id == user_id)
    data = query.offset(offset).limit(limit).all()
    return [MasterDataResponseSchema.from_orm(item) for item in data]

def GetDataById(session: Session, id: int):
    data = session.query(MasterData).filter(MasterData.id == id).first()
    if data is None:
        return {"error": f"Data with id {id} not found"}
    return MasterDataResponseSchema.from_orm(data)
