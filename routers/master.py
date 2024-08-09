from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from schemas.master import MasterDataCreateSchema, MasterDataResponseSchema
from cruds.master import CreateData, GetAllData, GetDataById
from typing import Optional, List
from cruds.user import TokenAuthorization

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")
router = APIRouter()


@router.post('/master')
async def create_master_data(
    user_id: int = Form(...),
    description: str = Form(...),
    longitude: float = Form(...),
    latitude: float = Form(...),
    site_condition: str = Form(...),
    rivera_condition: str = Form(...),
    riverb_condition: str = Form(...),
    riverc_condition: str = Form(...),
    riverd_condition: str = Form(...),
    rivere_condition: str = Form(...),
    weather_condition: str = Form(...),
    file: UploadFile = File(...),
    session: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    TokenAuthorization(session, token)
    new_data = MasterDataCreateSchema(
        user_id=user_id,
        description=description,
        location=f'{longitude},{latitude}',
        site_condition=site_condition,
        rivera_condition=rivera_condition,
        riverb_condition=riverb_condition,
        riverc_condition=riverc_condition,
        riverd_condition=riverd_condition,
        rivere_condition=rivere_condition,
        weather_condition=weather_condition
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
