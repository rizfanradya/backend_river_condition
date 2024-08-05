from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends
from schemas.choice import ChoiceSchema
from sqlalchemy.orm import Session
from database import get_db
from cruds.choice import CreateChoice, GetAllChoice, GetChoiceById, UpdateChoice, DeleteChoice
from typing import Optional
from cruds.user import TokenAuthorization

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")
router = APIRouter()


@router.post('/choice')
def create_choice(choice_info: ChoiceSchema, session: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    TokenAuthorization(session, token)
    return CreateChoice(session, choice_info)


@router.get('/choice')
def get_choice(limit: int = 10, offset: int = 0, search: Optional[str] = None, session: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    TokenAuthorization(session, token)
    return GetAllChoice(session, limit, offset, search)


@router.get("/choice/{id}")
def get_choice_by_id(id: int, session: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    TokenAuthorization(session, token)
    return GetChoiceById(session, id)


@router.put("/choice/{id}")
def update_choice_info(id: int, info_update: ChoiceSchema, session: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    TokenAuthorization(session, token)
    return UpdateChoice(session, id, info_update)


@router.delete("/choice/{id}")
def delete_choice(id: int, session: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    TokenAuthorization(session, token)
    return DeleteChoice(session, id)
