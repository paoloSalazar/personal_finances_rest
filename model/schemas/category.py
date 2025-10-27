from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str
    description: str

class CategoryCreate(CategoryBase):
    pass
    
class CategoryRead(CategoryBase):
    id: int | None = None

    class Config:
        from_attributes = True