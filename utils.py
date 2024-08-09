from datetime import datetime, timedelta
from typing import Union, Any
import jwt
import os
from dotenv import load_dotenv
import hashlib
from fastapi import HTTPException, UploadFile
from PIL import Image as PILImage
import aiofiles
import subprocess
import sys

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


def create_access_token(subject: Union[str, Any], client_type: str, expires_delta=None):
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    encoded_jwt = jwt.encode(payload={"exp": expires_delta, "id": str(subject), 'client_type': client_type},
                             key=str(JWT_SECRET_KEY),
                             algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], client_type: str, expires_delta=None):
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    encoded_jwt = jwt.encode(payload={"exp": expires_delta, "id": str(subject), 'client_type': client_type},
                             key=str(JWT_REFRESH_SECRET_KEY),
                             algorithm=ALGORITHM)
    return encoded_jwt


def check_and_remove_orphaned_files():
    from models.master import MasterData
    from database import SessionLocal

    session = SessionLocal()
    try:
        absolute_uploads_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'cruds', 'uploads')
        origin_dir = os.path.join(absolute_uploads_path, 'origin')
        thumbnail_dir = os.path.join(absolute_uploads_path, 'thumbnails')

        file_names_in_db = {md.file.split(
            '.')[0] for md in session.query(MasterData.file).all()}

        for filename in os.listdir(origin_dir):
            file_base_name = filename.split('.')[0]
            if file_base_name not in file_names_in_db:
                file_path = os.path.join(origin_dir, filename)
                os.remove(file_path)
                print(f"Deleted orphaned file: {file_path}")

        for filename in os.listdir(thumbnail_dir):
            file_base_name = filename.split('.')[0]
            if file_base_name not in file_names_in_db:
                file_path = os.path.join(thumbnail_dir, filename)
                os.remove(file_path)
                print(f"Deleted orphaned file: {file_path}")
    finally:
        session.close()


def send_error_response(error: str, message: str) -> HTTPException:
    raise HTTPException(
        status_code=404,
        detail={
            "message": message,
            "error": error,
        }
    )


def data_that_must_exist_in_the_database():
    from models.user import User
    from database import SessionLocal
    session = SessionLocal()
    user_admin = session.query(User).where(
        User.role == 'admin').first()
    if not user_admin:
        encode_password = '@Admin123'.encode()
        hash_password = hashlib.md5(encode_password).hexdigest()
        session.add(User(
            username='admin',
            password=hash_password,
            first_name='Admin',
            last_name='01',
            role='admin',
            is_active=True
        ))
        session.commit()


async def save_file(file: UploadFile, destination: str):
    async with aiofiles.open(destination, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)


def create_thumbnail(image_path: str, thumbnail_path: str, size=(128, 128)):
    with PILImage.open(image_path) as img:
        img.thumbnail(size)
        img.save(thumbnail_path)


def run_shell_commands():
    if os.name == 'posix':  # Linux/macOS
        python_cmd = "python3"
    elif os.name == 'nt':  # Windows
        python_cmd = "python"
    else:
        raise EnvironmentError("Unsupported operating system")

    commands = [
        f"{python_cmd} -m pip install --upgrade pip",
        f"{python_cmd} -m pip install --no-cache-dir -r requirements.txt",
        f"{python_cmd} -m alembic revision --autogenerate -m 'rev'",
        f"{python_cmd} -m alembic upgrade head"
    ]

    for command in commands:
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Command '{command}' failed with error: {e}")
            sys.exit(1)
