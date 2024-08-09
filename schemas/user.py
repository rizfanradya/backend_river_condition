from pydantic import BaseModel


class UserSchema(BaseModel):
    role: str
    username: str
    password: str
    first_name: str
    last_name: str
    is_active: bool
