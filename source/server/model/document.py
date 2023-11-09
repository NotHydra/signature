from pydantic import BaseModel


class DocumentPageModel(BaseModel):
    count: int
    page: int
