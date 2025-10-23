from .init import conn, cursor
from model.schemas.category import CategoryBase, CategoryCreate, CategoryRead
from model.tables.category import Category

cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL
)   
""")

def row_to_schema(row: tuple) -> CategoryRead:
    """convert a database row to a CategoryRead schema"""
    (id, name, description) = row
    return CategoryRead(id=id, name=name, description=description)

def schema_to_dict(category: CategoryBase) -> dict:
    """convert a Category schema to a dictionary"""
    return category.model_dump()

def get_one(name: str) -> CategoryRead | None:
    """return one category by name"""
    qry = "SELECT id,name,description FROM categories WHERE name=:name"
    params = {"name": name}
    cursor.execute(qry, params)
    row = cursor.fetchone()
    return row_to_schema(row) if row else None

def get_all() -> list[CategoryRead]:
    """return all categories"""
    qry = "SELECT id,name,description FROM categories"
    cursor.execute(qry)
    return [row_to_schema(row) for row in cursor.fetchall()]

def create(category: CategoryCreate) -> CategoryRead:
    qry = "INSERT INTO categories (name, description) VALUES (:name, :description)"
    params = schema_to_dict(category)
    cursor.execute(qry, params)
    conn.commit()  
    return get_one(category.name)

def modify(category: CategoryBase) -> CategoryRead:
    qry = "UPDATE categories SET description=:description WHERE name=:name"
    params = schema_to_dict(category)
    params["name_orig"] = category.name
    _ = cursor.execute(qry, params)
    conn.commit()  
    return get_one(category.name)

def replace(category: CategoryBase) -> CategoryRead:
    qry = "UPDATE categories SET name=:name, description=:description WHERE name=:name_orig"
    params = schema_to_dict(category)
    params["name_orig"] = category.name
    _ = cursor.execute(qry, params)
    conn.commit()  
    return get_one(category.name)

def delete(name: str) -> bool:
    qry = "DELETE FROM categories WHERE name=:name"
    params = {"name": name}
    res = cursor.execute(qry, params)
    conn.commit()  
    return bool(res)