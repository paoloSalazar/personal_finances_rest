from model.category import Category

_categories = [
    Category(id=1, name="Food", description="Expenses for food and groceries"),
    Category(id=2, name="Transport", description="Expenses for transportation"),
    Category(id=3, name="Entertainment", description="Expenses for entertainment and leisure"),
]

def get_all() -> list[Category]:
    """return all categories"""
    return _categories

def get_one(name: str) -> Category | None:
    """return one category by name"""
    for category in _categories:
        if category.name == name:
            return category
    return None

## Non functional methods

def create(category: Category) -> Category:
    return category

def modify(category: Category) -> Category:
    return category

def replace(category: Category) -> Category:
    return category

def delete(name: str) -> bool:
    return None
