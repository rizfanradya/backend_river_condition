from sqlalchemy.orm import Session
from models.master import MasterData
from models.user import User
from schemas.master import MasterDataCreateSchema
from fastapi import UploadFile
import os
from utils import send_error_response, save_file, create_thumbnail
from typing import Optional


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
            return send_error_response(
                'Wrong file type, only accept jpeg or png',
                'Wrong file type, only accept jpeg or png'
            )
        if os.fstat(file.file.fileno()).st_size > MAX_FILE_SIZE_BYTES:
            return send_error_response(
                'File too large, only accept file below 2MB',
                'File too large, only accept file below 2MB'
            )

        new_data_info = MasterData(
            user_id=new_data.user_id,
            description=new_data.description,
            location=new_data.location,
            site_condition=new_data.site_condition,
            rivera_condition=new_data.rivera_condition,
            riverb_condition=new_data.riverb_condition,
            riverc_condition=new_data.riverc_condition,
            riverd_condition=new_data.riverd_condition,
            rivere_condition=new_data.rivere_condition,
            weather_condition=new_data.weather_condition
        )

        session.add(new_data_info)
        session.commit()
        session.refresh(new_data_info)

        file_extension = file.filename.split('.')[-1]
        filename = f'{new_data_info.id}.{file_extension}'
        origin_filepath = os.path.join(origin_dir, filename)
        thumbnail_filepath = os.path.join(thumbnail_dir, filename)
        await save_file(file, origin_filepath)
        create_thumbnail(origin_filepath, thumbnail_filepath)

        new_data_info.file = f'{new_data_info.id}.{file_extension}'
        session.commit()
        session.refresh(new_data_info)
        return new_data_info
    except Exception as error:
        return send_error_response(
            str(error),
            'Failed to create data'
        )


def GetAllData(session: Session, user_id: Optional[int] = None, limit: int = 10, offset: int = 0):
    query = session.query(MasterData).order_by(MasterData.id.desc())
    if user_id:
        user_info = session.query(User).get(user_id)
        if user_info != 'admin':
            query = query.filter(MasterData.user_id == user_id)
    data = query.offset(offset).limit(limit).all()
    for item in data:
        item.thumbnail_filepath = f"/89.116.20.146:8000/thumbnails/{item.file}"
    return data


def GetDataById(session: Session, id: int):
    data = session.query(MasterData).filter(MasterData.id == id).first()
    if data is None:
        send_error_response(
            f"Data with id {id} not found",
            f"Data with id {id} not found"
        )
    data.origin_filepath = f"/89.116.20.146:8000/origin/{data.file}"
    return data
