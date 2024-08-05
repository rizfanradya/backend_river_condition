from sqlalchemy.orm import Session
from schemas.choice import ChoiceSchema
from models.choice import Choice
from typing import Optional
from sqlalchemy import or_
from utils import send_error_response


def CreateChoice(session: Session, new_data: ChoiceSchema):
    try:
        new_data_info = Choice(**new_data.dict())
        session.add(new_data_info)
        session.commit()
        session.refresh(new_data_info)
        return new_data_info
    except Exception as error:
        send_error_response(
            str(error),
            f'Choice "{new_data.choice}" is already exist'
        )


def GetAllChoice(session: Session, limit: int, offset: int, search: Optional[str] = None):
    query = session.query(Choice)
    if search:
        query = query.filter(or_(*[getattr(Choice, column).ilike(
            f"%{search}%"
        ) for column in Choice.__table__.columns.keys()]))
    return {
        "total_data": query.count(),
        "limit": limit,
        "offset": offset,
        "search": search,
        "data": query.offset(offset).limit(limit).all()
    }


def GetChoiceById(session: Session, id: int):
    query = session.query(Choice).get(id)
    if query is None:
        send_error_response(
            f'Choice with id "{id}" not found',
            f'Choice with id "{id}" not found'
        )
    return query


def UpdateChoice(session: Session, id: int, info_update: ChoiceSchema):
    query = GetChoiceById(session, id)
    try:
        for attr, value in info_update.__dict__.items():
            setattr(query, attr, value)
        session.commit()
        session.refresh(query)
        return query.__dict__
    except Exception as error:
        send_error_response(
            str(error),
            f'Choice "{info_update.choice}" is already exist'
        )


def DeleteChoice(session: Session, id: int):
    query = GetChoiceById(session, id)
    session.delete(query)
    session.commit()
    return {"detail": f'Choice id "{id}" deleted success'}
