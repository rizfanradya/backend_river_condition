from sqlalchemy.orm import Session
from models.data import Data
from models.image import Image
from schemas.data import DataSchema
from typing import Optional, List
from sqlalchemy import or_
from utils import send_error_response, file_management
from fastapi import UploadFile, File
import os
import uuid


def CreateData(session: Session, new_data: DataSchema, images: List[UploadFile] = File(...)):
    try:
        MAX_FILE_SIZE_BYTES = 2 * 1024 * 1024  # 2MB
        allowed_content_types = ['image/jpeg', 'image/png']
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        upload_dir = os.path.join(base_dir, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)

        saved_images = []
        for file in images:
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

            file_extension = file.filename.split('.')[-1]  # type: ignore
            filename = f'{uuid.uuid4()}.{file_extension}'
            file_path = os.path.join(upload_dir, filename)

            try:
                with open(file_path, 'wb') as f:
                    f.write(file.file.read())
            except Exception as error:
                return send_error_response(str(error), 'Failed to save file')

            if not os.path.exists(file_path):
                return send_error_response(
                    'File not found after saving',
                    'File not found after saving'
                )
            saved_images.append((filename, file_path))

        new_data_info = Data(**new_data.dict())
        session.add(new_data_info)
        session.commit()
        session.refresh(new_data_info)

        for filename, file_path in saved_images:
            new_image = Image(
                data_id=new_data_info.id,
                image=filename,
            )
            session.add(new_image)
        session.commit()

        query_image = session.query(Image).all()
        file_management(query_image, 'uploads', 'image')
        new_data_info.id
        return {
            "data": new_data_info.__dict__,
            "images": [{
                "filename": filename,
                "file_path": file_path
            } for filename, file_path in saved_images]
        }
    except Exception as error:
        return send_error_response(
            str(error),
            'An error occurred during data creation'
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
