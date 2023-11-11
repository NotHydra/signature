from pydantic import BaseModel


class UserPageModel(BaseModel):
    count: int
    page: int


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
