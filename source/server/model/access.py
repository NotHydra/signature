from pydantic import BaseModel


class AccessPageModel(BaseModel):
    count: int
    page: int
