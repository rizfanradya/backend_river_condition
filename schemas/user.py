from pydantic import BaseModel


class UserSchema(BaseModel):
    role_id: int
    username: str
    password: str
    first_name: str
    last_name: str
    is_active: bool
