from pydantic import BaseModel


class AuthLoginModel(BaseModel):
    username: str
    password: str


class AuthRegisterModel(BaseModel):
    name: str
    username: str
    email: str
    password: str
