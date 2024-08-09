from sqlalchemy.orm import Session
from models.master import MasterData
from schemas.master import MasterDataCreateSchema
from fastapi import UploadFile
import os
import uuid
from PIL import Image as PILImage
import aiofiles
import datetime
from utils import send_error_response


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
        allowed_content_types = ['image/jpeg', 'image/png', 'image/jpg']
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        origin_dir = os.path.join(base_dir, 'uploads', 'origin')
        thumbnail_dir = os.path.join(base_dir, 'uploads', 'thumbnails')
        
        os.makedirs(origin_dir, exist_ok=True)
        os.makedirs(thumbnail_dir, exist_ok=True)

        if file.content_type not in allowed_content_types:
            send_error_response(
                'Wrong file type, only accept jpeg or png',
                'Wrong file type, only accept jpeg or png'
            )
        if os.fstat(file.file.fileno()).st_size > MAX_FILE_SIZE_BYTES:
            send_error_response(
                'File too large, only accept file below 2MB',
                'File too large, only accept file below 2MB'
            )

        file_extension = file.filename.split('.')[-1]
        filename = f'{uuid.uuid4()}.{file_extension}'
        
        origin_filepath = os.path.join(origin_dir, filename)
        thumbnail_filepath = os.path.join(thumbnail_dir, filename)

        await save_file(file, origin_filepath)
        create_thumbnail(origin_filepath, thumbnail_filepath)

        new_data_info = MasterData(
            user_id=new_data.user_id,
            description=new_data.description,
            location=new_data.location,
            origin_filepath=origin_filepath,
            thumbnail_filepath=thumbnail_filepath,
            upload_date=datetime.datetime.utcnow()
        )
        
        session.add(new_data_info)
        session.commit()
        session.refresh(new_data_info)

        return new_data_info
    except Exception as error:
        send_error_response(
            str(error),
            'Failed to create data'
        )
