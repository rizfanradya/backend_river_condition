from pydantic import BaseModel


class ChoiceSchema(BaseModel):
    choice: str
