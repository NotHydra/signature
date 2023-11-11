from pydantic import BaseModel


class AccessPageModel(BaseModel):
    count: int
    page: int


class AccessAddModel(BaseModel):
    usernameUser: str
    idDocument: int
