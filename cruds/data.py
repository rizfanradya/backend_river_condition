from sqlalchemy.orm import Session
from models.data import Data
from models.image import Image
from schemas.data import DataSchema
from typing import Optional, List
from sqlalchemy import or_
from utils import send_error_response, file_management
from fastapi import UploadFile, File
import os


def CreateData(session: Session, new_data: DataSchema, image: List[UploadFile] = File(...)):
    try:
        MAX_FILE_SIZE_BYTES = 2 * 1024 * 1024  # 2mb
        allowed_content_types = ['image/jpeg', 'image/png']
        for file in image:
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

        new_data_info = Data(**new_data.dict())
        session.add(new_data_info)
        session.commit()
        session.refresh(new_data_info)
        query_image = session.query(Image).all()
        file_management(query_image, 'uploads', 'image')
        return new_data_info
    except Exception as error:
        send_error_response(
            str(error),
            f'user id or river id not found'
        )


def GetAllData(session: Session, limit: int, offset: int, search: Optional[str] = None):
    query = session.query(Data)
    if search:
        query = query.filter(or_(*[getattr(Data, column).ilike(
            f"%{search}%"
        ) for column in Data.__table__.columns.keys()]))
    return {
        "total_data": query.count(),
        "limit": limit,
        "offset": offset,
        "search": search,
        "data": query.offset(offset).limit(limit).all()
    }


def GetDataById(session: Session, id: int):
    query = session.query(Data).get(id)
    if query is None:
        send_error_response(
            f'Data with id "{id}" not found',
            f'Data with id "{id}" not found'
        )
    return query


def UpdateData(session: Session, id: int, info_update: DataSchema):
    query = GetDataById(session, id)
    try:
        for attr, value in info_update.__dict__.items():
            setattr(query, attr, value)
        session.commit()
        session.refresh(query)
        return query.__dict__
    except Exception as error:
        send_error_response(
            str(error),
            f'user id or river id not found'
        )


def DeleteData(session: Session, id: int):
    query = GetDataById(session, id)
    session.delete(query)
    session.commit()
    return {"detail": f'Data id "{id}" deleted success'}
