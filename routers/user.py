from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from schemas.user import UserSchema
from database import get_db
from typing import Optional
from cruds.user import CreateUser, GetAllUser, GetUserById, GetLogin, UpdateUser, DeleteUser, TokenAuthorization, RefreshToken

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")
router = APIRouter()


@router.post('/user')
def create_new_user(user_info: UserSchema, session: Session = Depends(get_db)):
    return CreateUser(session, user_info)


@router.post("/token")
async def user_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_db),
    client_type: str = Query(
        description="Client type web or mobile",
        default="web"),
):
    return GetLogin(session, form_data, client_type)


@router.post("/refresh_token/{refresh_token}")
async def refresh_token(refresh_token: str, client_type: str, session: Session = Depends(get_db)):
    return RefreshToken(session, refresh_token, client_type)


@router.get('/user')
def get_user(limit: int = 10, offset: int = 0, search: Optional[str] = None, session: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    TokenAuthorization(session, token)
    return GetAllUser(session, limit, offset, search)


@router.get("/user/{id}")
def get_user_byid(id: int, session: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    TokenAuthorization(session, token)
    return GetUserById(session, id)


@router.put("/user/{id}")
def update_user_info(id: int, info_update: UserSchema, session: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    TokenAuthorization(session, token)
    return UpdateUser(session, id, info_update)


@router.delete("/user/{id}")
def delete_user_info(id: int, session: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    TokenAuthorization(session, token)
    return DeleteUser(session, id)
