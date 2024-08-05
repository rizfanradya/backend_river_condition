from sqlalchemy.orm import Session
from models.data import Data
from schemas.data import DataSchema
from typing import Optional
from sqlalchemy import or_
from utils import send_error_response


def CreateData(session: Session, new_data: DataSchema):
    try:
        new_data_info = Data(**new_data.dict())
        session.add(new_data_info)
        session.commit()
        session.refresh(new_data_info)
        return new_data_info
    except Exception as error:
        send_error_response(
            str(error),
            f'error when create data'
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
            f'error when update data'
        )


def DeleteData(session: Session, id: int):
    query = GetDataById(session, id)
    session.delete(query)
    session.commit()
    return f'Data id "{id}" deleted success'
