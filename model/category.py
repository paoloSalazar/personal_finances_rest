from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()
engine = create_engine('sqlite:///db/personal_finances.db')

class Category(BaseModel):
    id: int | None
    name: str
    description: str
