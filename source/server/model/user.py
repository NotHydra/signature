from pydantic import BaseModel


class UserModel(BaseModel):
    name: str
    username: str
    email: str
    password: str = None
    level: str
    isActive: bool
