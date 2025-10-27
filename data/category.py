import logging
from .init import conn, cursor
from model.schemas.category import CategoryBase, CategoryCreate, CategoryRead
from model.tables.category import Category

logger = logging.getLogger(__name__)

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
    logger.debug(f"Data: Executing SELECT category by name: {name}")
    qry = "SELECT id,name,description FROM categories WHERE name=:name"
    params = {"name": name}
    cursor.execute(qry, params)
    row = cursor.fetchone()
    result = row_to_schema(row) if row else None
    logger.debug(f"Data: Category {'found' if result else 'not found'}: {name}")
    return result

def get_all() -> list[CategoryRead]:
    """return all categories"""
    logger.debug("Data: Executing SELECT all categories")
    qry = "SELECT id,name,description FROM categories"
    cursor.execute(qry)
    rows = cursor.fetchall()
    result = [row_to_schema(row) for row in rows]
    logger.debug(f"Data: Retrieved {len(result)} categories from database")
    return result

def create(category: CategoryCreate) -> CategoryRead:
    logger.debug(f"Data: Inserting category: {category.name}")
    qry = "INSERT INTO categories (name, description) VALUES (:name, :description)"
    params = schema_to_dict(category)
    cursor.execute(qry, params)
    conn.commit()
    logger.debug(f"Data: Category inserted, retrieving: {category.name}")
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