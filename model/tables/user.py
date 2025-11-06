from sqlalchemy import Column, Integer, String
from ..database import Base
from sqlalchemy import Column, Integer, String, DateTime, func

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(50), nullable=False, unique=True)
    hash = Column(String(100), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
