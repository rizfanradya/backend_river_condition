from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from schemas.master import MasterDataCreateSchema
from cruds.master import CreateData, GetAllData, GetDataById
from typing import Optional
from cruds.user import TokenAuthorization

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")
router = APIRouter()


@router.post('/master')
async def create_master_data(
    user_id: int = Form(...),
    description: str = Form(...),
    longitude: float = Form(...),
    latitude: float = Form(...),
    file: UploadFile = File(...),
    session: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    TokenAuthorization(session, token)
    # Menggabungkan longitude dan latitude menjadi satu string
    location = f'{longitude},{latitude}'
    new_data = MasterDataCreateSchema(
        user_id=user_id,
        description=description,
        location=location
    )
    return await CreateData(session, new_data, file)


@router.get('/master')
def get_master_data(
    user_id: Optional[int] = None,
    limit: int = 10,
    offset: int = 0,
    session: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    TokenAuthorization(session, token)
    return GetAllData(session, user_id, limit, offset)


@router.get('/master/{id}')
def get_master_data_by_id(
    id: int,
    session: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    TokenAuthorization(session, token)
    return GetDataById(session, id)
