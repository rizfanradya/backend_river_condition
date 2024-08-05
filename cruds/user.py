from sqlalchemy.orm import Session
from schemas.user import UserSchema
from password_validator import PasswordValidator
import hashlib
from models.user import User
from models.role import Role
from utils import create_access_token, create_refresh_token, ALGORITHM, JWT_SECRET_KEY, JWT_REFRESH_SECRET_KEY, send_error_response
from typing import Optional
from sqlalchemy import or_
import jwt

schema_password_validator = PasswordValidator()
schema_password_validator.min(8).has().uppercase(
).has().lowercase().has().digits().has().symbols()


def CreateUser(session: Session, user_info: UserSchema):
    if not schema_password_validator.validate(user_info.password):
        send_error_response(
            "Password must consist of at least 8 characters, contain at least one uppercase letter, one lowercase letter, one digit, one special character or symbol, and cannot contain spaces",
            "Password must consist of at least 8 characters, contain at least one uppercase letter, one lowercase letter, one digit, one special character or symbol, and cannot contain spaces"
        )
    try:
        encode_password = user_info.password.encode()
        hash_password = hashlib.md5(encode_password).hexdigest()
        new_user_info = User(**user_info.dict())
        new_user_info.password = hash_password  # type: ignore
        session.add(new_user_info)
        session.commit()
        session.refresh(new_user_info)
        return new_user_info
    except Exception as error:
        send_error_response(
            str(error),
            f'User "{user_info.username}" is already exist'
        )


def GetAllUser(session: Session, limit: int, offset: int, search: Optional[str] = None):
    from models.role import Role

    all_user = session.query(User)
    role_info = session.query(Role).all()
    role_mapping = {role.id: role for role in role_info}

    if search:
        all_user = all_user.filter(or_(*[getattr(User, column).ilike(
            f"%{search}%"
        ) for column in User.__table__.columns.keys()]))

    total_data = all_user.count()
    all_user = all_user.offset(offset).limit(limit).all()

    for user in all_user:
        user.password = ''  # type: ignore
        user.active = "ACTIVE" if user.is_active else "INACTIVE"  # type: ignore
        user.role_name = role_mapping.get(user.role_id).role if role_mapping.get(  # type: ignore
            user.role_id) else None

    return {
        "total_data": total_data,
        "limit": limit,
        "offset": offset,
        "search": search,
        "data": all_user
    }


def GetUserById(session: Session, id: int):
    from models.role import Role
    user_info = session.query(User).get(id)
    if user_info is None:
        send_error_response(
            f'User with id "{id}" not found',
            f'User with id "{id}" not found'
        )
    user_info.password = ''  # type: ignore
    user_info.role_name = session.query(Role).get(  # type: ignore
        user_info.role_id).role if session.query(Role).get(user_info.role_id) else None  # type: ignore
    user_info.active = "ACTIVE" if user_info.is_active else "INACTIVE"  # type: ignore
    return user_info


def GetUserByUsername(session: Session, username: str):
    from models.role import Role
    user_info = session.query(User).where(
        User.username == username).first()
    if user_info is None:
        send_error_response(
            f'User "{username}" not found',
            f'User "{username}" not found'
        )
    user_info.password = ''  # type: ignore
    user_info.role_name = session.query(Role).get(  # type: ignore
        user_info.role_id).role if session.query(Role).get(user_info.role_id) else None  # type: ignore
    user_info.active = "ACTIVE" if user_info.is_active else "INACTIVE"  # type: ignore
    return user_info


def UpdateUser(session: Session, id: int, info_update: UserSchema):
    from cruds.role import GetRoleById
    GetRoleById(session, info_update.role_id)
    user_info = session.query(User).get(id)

    if user_info is None:
        send_error_response(
            f'User with id "{id}" not found',
            f'User with id "{id}" not found'
        )

    if not schema_password_validator.validate(info_update.password):
        send_error_response(
            "Password must consist of at least 8 characters, contain at least one uppercase letter, one lowercase letter, one digit, one special character or symbol, and cannot contain spaces",
            "Password must consist of at least 8 characters, contain at least one uppercase letter, one lowercase letter, one digit, one special character or symbol, and cannot contain spaces"
        )

    try:
        info_update.password = hashlib.md5(
            info_update.password.encode()).hexdigest()
        for attr, value in info_update.__dict__.items():
            setattr(user_info, attr, value)
        session.commit()
        session.refresh(user_info)
        return user_info.__dict__
    except Exception as error:
        send_error_response(
            str(error),
            f'User "{info_update.username}" is already exist'
        )


def DeleteUser(session: Session, id: int):
    user_info = session.query(User).get(id)
    if user_info is None:
        send_error_response(
            f'User with id "{id}" not found',
            f'User with id "{id}" not found'
        )
    session.delete(user_info)
    session.commit()
    return {'detail': f'User with id "{id}" deleted success'}


def GetLogin(session: Session, user_login):
    user_info = session.query(User).where(
        User.username == user_login.username).first()
    if user_info is None:
        send_error_response(f'User not found', f'User not found')
    role_info = session.query(Role).get(user_info.role_id)  # type: ignore
    hash_password = hashlib.md5(user_login.password.encode()).hexdigest()
    if user_info.password == hash_password:  # type: ignore
        return {
            "id": user_info.id,  # type: ignore
            "access_token": create_access_token(
                user_info.id),  # type: ignore
            "refresh_token": create_refresh_token(
                user_info.id),  # type: ignore
            "status": user_info.is_active,  # type: ignore
            "role": role_info.role,  # type: ignore
            "detail": "ok"
        }
    else:
        return {
            "id": user_info.id,  # type: ignore
            "access_token": "",
            "refresh_token": "",
            "status": False,
            "role": None,
            "detail": "Username or Password incorrect"
        }


def TokenAuthorization(session: Session, token: str):
    if JWT_SECRET_KEY is None:
        raise EnvironmentError(f"Environment variable JWT_SECRET_KEY not set")
    try:
        decode_token = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        user_info = session.query(User).get(decode_token.get('id'))
        if user_info is None:
            send_error_response(f'User not found', f'User not found')
        return user_info
    except jwt.ExpiredSignatureError:
        send_error_response(f'Token has expired', f'Token has expired')
    except jwt.InvalidTokenError:
        send_error_response(f'Token is invalid', f'Token is invalid')


def RefreshToken(session: Session, refresh_token: str):
    if JWT_REFRESH_SECRET_KEY is None:
        raise EnvironmentError(f"Environment variable JWT_SECRET_KEY not set")
    try:
        decode_token = jwt.decode(
            refresh_token, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        user_info = session.query(User).get(decode_token.get('id'))
        if user_info is None:
            send_error_response(f'User not found', f'User not found')
        return {
            "access_token": create_access_token(user_info.id),  # type: ignore
            "refresh_token": create_refresh_token(user_info.id)  # type: ignore
        }
    except jwt.ExpiredSignatureError:
        send_error_response(f'Token has expired', f'Token has expired')
    except jwt.InvalidTokenError:
        send_error_response(f'Token is invalid', f'Token is invalid')
