from typing import Optional
from sqlmodel import Field, SQLModel, create_engine
import os

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    password: str

DATABASE_URL = os.getenv("DATABASE_URL")

print(f"Connecting to: {DATABASE_URL}")

engine = create_engine(DATABASE_URL, echo=True)

SQLModel.metadata.create_all(engine)