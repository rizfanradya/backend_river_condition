from datetime import datetime, timedelta
from typing import Union, Any
import jwt
import os
from dotenv import load_dotenv
import hashlib
from fastapi import HTTPException

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 60 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
JWT_REFRESH_SECRET_KEY = os.environ.get('JWT_REFRESH_SECRET_KEY')
IP_SERVER_HOSTNAME = os.environ.get('IP_SERVER_HOSTNAME')
SERVER_PORT = os.environ.get('SERVER_PORT')
DB_HOSTNAME = os.environ.get('DB_HOSTNAME')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME')


# print('JWT_SECRET_KEY', JWT_SECRET_KEY)
# print('JWT_REFRESH_SECRET_KEY', JWT_REFRESH_SECRET_KEY)
# print('IP_SERVER_HOSTNAME', IP_SERVER_HOSTNAME)
# print('SERVER_PORT', SERVER_PORT)
# print('DB_HOSTNAME', DB_HOSTNAME)
# print('DB_PORT', DB_PORT)
# print('DB_USER', DB_USER)
# print('DB_PASSWORD', DB_PASSWORD)
# print('DB_NAME', DB_NAME)


def create_access_token(subject: Union[str, Any], expires_delta=None):
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    encoded_jwt = jwt.encode(payload={"exp": expires_delta, "id": str(subject)},
                             key=str(JWT_SECRET_KEY),
                             algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta=None):
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    encoded_jwt = jwt.encode(payload={"exp": expires_delta, "id": str(subject)},
                             key=str(JWT_REFRESH_SECRET_KEY),
                             algorithm=ALGORITHM)
    return encoded_jwt


def file_management(database, folder, db_column_name):
    db_list_files = [
        getattr(data, db_column_name) for data in database if getattr(data, db_column_name)
    ]
    local_list_files = os.listdir(folder)
    files_to_delete = [f for f in local_list_files if f not in db_list_files]
    for file_name in files_to_delete:
        file_path = os.path.join(folder, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)


def send_error_response(error: str, message: str) -> HTTPException:
    raise HTTPException(
        status_code=404,
        detail={
            "message": message,
            "error": error,
        }
    )


def data_that_must_exist_in_the_database():
    from models.role import Role
    from models.user import User
    from database import SessionLocal
    session = SessionLocal()
    role_super_admin = session.query(Role).where(
        Role.role == 'super administrator').first()
    role_admin = session.query(Role).where(
        Role.role == 'administrator').first()
    role_user = session.query(Role).where(Role.role == 'user').first()
    if not role_super_admin:
        session.add(Role(role='super administrator'))
        session.commit()
    if not role_admin:
        session.add(Role(role='administrator'))
        session.commit()
    if not role_user:
        session.add(Role(role='user'))
        session.commit()
    role_super_admin = session.query(Role).where(
        Role.role == 'super administrator').first()
    user_super_admin = session.query(User).where(
        User.role_id == role_super_admin.id).first()  # type: ignore
    if not user_super_admin:
        encode_password = '@SuperAdmin123'.encode()
        hash_password = hashlib.md5(encode_password).hexdigest()
        session.add(User(
            username='superadmin',
            password=hash_password,
            first_name='Super',
            last_name='Admin',
            role_id=role_super_admin.id,  # type: ignore
            is_active=True
        ))
        session.commit()
