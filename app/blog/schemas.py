from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel
import datetime

class BlogBase(BaseModel):
    title: str
    content: str

class BlogResponse(BaseModel):
    id: int
    createdAt: datetime
    updatedAt: datetime
    title: str
    content: str
    nickname: Optional[str]  

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True