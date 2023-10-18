from pydantic import BaseModel


class UserModel(BaseModel):
    name: str
    username: str
    email: str
    password: str
    level: str
    isActive: bool


class UserUpdateModel(BaseModel):
    name: str
    username: str
    email: str
    level: str


class UserUpdatePasswordModel(BaseModel):
    password: str
