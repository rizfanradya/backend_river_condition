from sqlalchemy.orm import Session
from schemas.role import RoleSchema
from models.role import Role
from typing import Optional
from sqlalchemy import or_
from utils import send_error_response


def CreateRole(session: Session, role_info: RoleSchema):
    try:
        new_role_info = Role(**role_info.dict())
        session.add(new_role_info)
        session.commit()
        session.refresh(new_role_info)
        return new_role_info
    except Exception as error:
        send_error_response(
            str(error),
            f'Role "{role_info.role}" is already exist'
        )


def GetAllRole(session: Session, limit: int, offset: int, search: Optional[str] = None):
    all_role = session.query(Role)
    if search:
        all_role = all_role.filter(or_(*[getattr(Role, column).ilike(
            f"%{search}%"
        ) for column in Role.__table__.columns.keys()]))
    return {
        "total_data": all_role.count(),
        "limit": limit,
        "offset": offset,
        "search": search,
        "data": all_role.offset(offset).limit(limit).all()
    }


def GetRoleById(session: Session, id: int):
    role_info = session.query(Role).get(id)
    if role_info is None:
        send_error_response(
            f'Role with id "{id}" not found',
            f'Role with id "{id}" not found'
        )
    return role_info


def UpdateRole(session: Session, id: int, info_update: RoleSchema):
    role_info = GetRoleById(session, id)
    try:
        for attr, value in info_update.__dict__.items():
            setattr(role_info, attr, value)
        session.commit()
        session.refresh(role_info)
        return role_info.__dict__
    except Exception as error:
        send_error_response(
            str(error),
            f'Role "{info_update.role}" is already exist'
        )


def DeleteRole(session: Session, id: int):
    role_info = GetRoleById(session, id)
    session.delete(role_info)
    session.commit()
    return f'Role id "{id}" deleted success'
