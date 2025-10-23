from .init import conn, cursor
from model.category import Category

cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL
)   
""")

def row_to_model(row: tuple) -> Category:
    """convert a database row to a Category model"""
    (id, name, description) = row
    return Category(id=id, name=name, description=description)

def model_to_dict(category: Category) -> dict:
    """convert a Category model to a dictionary"""
    return category.model_dump()

def get_one(name: str) -> Category | None:
    """return one category by name"""
    qry = "SELECT * FROM categories WHERE name=:name"
    params = {"name": name}
    cursor.execute(qry, params)
    return row_to_model(cursor.fetchone())

def get_all() -> list[Category]:
    """return all categories"""
    qry = "SELECT * FROM categories"
    cursor.execute(qry)
    return [row_to_model(row) for row in cursor.fetchall()]

def create(category: Category) -> Category:
    qry = "INSERT INTO categories (name, description) VALUES (:name, :description)"
    params = model_to_dict(category)
    cursor.execute(qry, params)
    return get_one(category.name)

def modify(category: Category) -> Category:
    qry = "UPDATE categories SET description=:description WHERE name=:name"
    params = model_to_dict(category)
    params["name_orig"] = category.name
    _ = cursor.execute(qry, params)
    return get_one(category.name)

def replace(category: Category) -> Category:
    qry = "UPDATE categories SET name=:name, description=:description WHERE name=:name_orig"
    params = model_to_dict(category)
    params["name_orig"] = category.name
    _ = cursor.execute(qry, params)
    return get_one(category.name)

def delete(name: str) -> bool:
    qry = "DELETE FROM categories WHERE name=:name"
    params = {"name": name}
    res = cursor.execute(qry, params)
    return bool(res)