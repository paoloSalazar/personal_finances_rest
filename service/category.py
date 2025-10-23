from model.schemas.category import CategoryBase, CategoryCreate, CategoryRead
import data.category as data

def get_all() -> list[CategoryRead]:
    """return all categories"""
    return data.get_all()

def get_one(name: str) -> CategoryRead | None:
    """return one category by name"""
    return data.get_one(name)


## Non functional methods

def create(category: CategoryCreate) -> CategoryRead:
    return data.create(category)

def modify(category: CategoryBase) -> CategoryRead:
    return data.modify(category)

def replace(category: CategoryBase) -> CategoryRead:
    return data.replace(category)

def delete(name: str) -> bool:
    return data.delete(name)