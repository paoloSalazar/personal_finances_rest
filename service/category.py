from model.category import Category
import data.category as data

def get_all() -> list[Category]:
    """return all categories"""
    return data.get_all()

def get_one(name: str) -> Category | None:
    """return one category by name"""
    return data.get_one(name)


## Non functional methods

def create(category: Category) -> Category:
    return data.create(category)

def modify(category: Category) -> Category:
    return data.modify(category)

def replace(category: Category) -> Category:
    return data.replace(category)

def delete(name: str) -> bool:
    return data.delete(name)