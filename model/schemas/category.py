from pydantic import BaseModel

class CategoryBase(BaseModel):
    id: int | None = None
    name: str
    description: str

class CategoryCreate(CategoryBase):
    id: int | None = None
    
class CategoryRead(CategoryBase):
    id: int | None = None

    class Config:
        from_attributes = True