import datetime

from pydantic import BaseModel


class UserModel(BaseModel):
    name: str
    username: str
    email: str
    password: str
    level: str
    isActive: bool
