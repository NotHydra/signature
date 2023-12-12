from pydantic import BaseModel


class UserAddModel(BaseModel):
    name: str
    username: str
    email: str
    password: str
    role: str
    is_active: bool


class UserChangeModel(BaseModel):
    name: str
    username: str
    email: str
    role: str


class UserChangePasswordModel(BaseModel):
    password: str
