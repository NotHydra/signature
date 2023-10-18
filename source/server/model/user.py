from pydantic import BaseModel


class UserPageModel(BaseModel):
    count: int
    page: int


class UserModel(BaseModel):
    name: str
    username: str
    email: str
    password: str
    role: str
    isActive: bool


class UserUpdateModel(BaseModel):
    name: str
    username: str
    email: str
    role: str


class UserUpdatePasswordModel(BaseModel):
    password: str
