from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base



class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(30))
    password = Column(String(30))
    created = Column(DateTime, default=datetime.now())
    updated = Column(DateTime, default=datetime.now(), onupdate=datetime.now())