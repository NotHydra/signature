from pydantic import BaseModel


class AccessPageModel(BaseModel):
    count: int
    page: int


class AccessAddModel(BaseModel):
    username_user: str
    id_document: int
