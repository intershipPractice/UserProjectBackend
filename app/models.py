from typing import Optional
from sqlmodel import Field, SQLModel, create_engine

class Used(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    password: str

engine = create_engine("sqlite:///database.db")


SQLModel.metadata.create_all(engine)