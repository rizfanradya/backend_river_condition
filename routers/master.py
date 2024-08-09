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
    file: UploadFile = File(...),
    session: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    TokenAuthorization(session, token)
    # Combine longitude and latitude into a single string
    location = f'{longitude},{latitude}'
    new_data = MasterDataCreateSchema(
        user_id=user_id,
        description=description,
        location=location
    )
    return await CreateData(session, new_data, file)

@router.get('/master', response_model=List[MasterDataResponseSchema])
def get_master_data(
    user_id: Optional[int] = None,
    limit: int = 10,
    offset: int = 0,
    session: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    TokenAuthorization(session, token)
    data = GetAllData(session, user_id, limit, offset)
    
    for item in data:
        item.thumbnail_filepath = f"/localhost:8000/thumbnails/{item.thumbnail_filepath.split('/')[-1]}"
    
    return data

@router.get('/master/{id}', response_model=MasterDataResponseSchema)
def get_master_data_by_id(
    id: int,
    session: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    TokenAuthorization(session, token)
    data = GetDataById(session, id)
    
    if isinstance(data, dict) and "error" in data:
        return data
    
    data.origin_filepath = f"/localhost:8000/origin/{data.origin_filepath.split('/')[-1]}"
    
    return data
