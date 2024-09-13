from sqlmodel import Field, SQLModel, create_engine, Relationship
import os
from typing import Optional, List
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)
    isDeleted: bool = Field(default=False)
    email: str
    password: str
    blogs: List["Blog"] = Relationship(back_populates="author")

class Blog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)
    isDeleted: bool = Field(default=False)
    title: str
    content: str
    userId: Optional[int] = Field(default=None, foreign_key="user.id")
    author: Optional[User] = Relationship(back_populates="blogs")

DATABASE_URL = os.getenv("DATABASE_URL")

print(f"Connecting to: {DATABASE_URL}")

engine = create_engine(DATABASE_URL, echo=True)

SQLModel.metadata.create_all(engine)
