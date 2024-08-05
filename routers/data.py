from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends
from schemas.data import DataSchema
from sqlalchemy.orm import Session
from database import get_db
from cruds.data import CreateData, GetAllData, GetDataById, UpdateData, DeleteData
from typing import Optional
from cruds.user import TokenAuthorization

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")
router = APIRouter()


@router.post('/data')
def create_data(data_info: DataSchema, session: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    TokenAuthorization(session, token)
    return CreateData(session, data_info)


@router.get('/data')
def get_data(limit: int = 10, offset: int = 0, search: Optional[str] = None, session: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    TokenAuthorization(session, token)
    return GetAllData(session, limit, offset, search)


@router.get("/data/{id}")
def get_data_by_id(id: int, session: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    TokenAuthorization(session, token)
    return GetDataById(session, id)


@router.put("/data/{id}")
def update_data_info(id: int, info_update: DataSchema, session: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    TokenAuthorization(session, token)
    return UpdateData(session, id, info_update)


@router.delete("/data/{id}")
def delete_data(id: int, session: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    TokenAuthorization(session, token)
    return DeleteData(session, id)
