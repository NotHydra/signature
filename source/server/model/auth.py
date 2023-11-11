from pydantic import BaseModel


class AuthLoginModel(BaseModel):
    username: str
    password: str
