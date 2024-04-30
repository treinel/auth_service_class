from config.db import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    name = Column(String)
    password = Column(String)
    role = Column(String)
    cel = Column(String)
    