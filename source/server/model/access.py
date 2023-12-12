from pydantic import BaseModel

class AccessAddModel(BaseModel):
    username_user: str
    id_document: int
