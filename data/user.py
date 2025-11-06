from model.schemas.user import User
from .init import (conn, cursor, get_db, IntegrityError)

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    hash TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS xusers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    hash TEXT NOT NULL
)
""")

def row_to_model(row: tuple) -> User:
    """convert a database row to a User schema"""
    (id, name, hash) = row
    return User(name=name, hash=hash)

def model_to_dict(user: User) -> dict:
    """convert a User schema to a dictionary"""
    return user.model_dump()

def get_one(name: str) -> User | None:
    """return one user by name"""
    qry = "SELECT id,name,hash FROM users WHERE name=:name"
    params = {"name": name}
    cursor.execute(qry, params)
    row = cursor.fetchone()
    result = row_to_model(row) if row else None
    return result

def get_all() -> list[User]:
    """return all users"""
    qry = "SELECT id,name,hash FROM users"
    cursor.execute(qry)
    return [row_to_model(row) for row in cursor.fetchall()]

def create(user: User, table:str = "users") -> User:
    """create a new user"""
    qry = f"INSERT INTO {table} (name, hash) VALUES (:name, :hash)"
    params = model_to_dict(user)
    cursor.execute(qry, params)
    conn.commit()
    return user

def modify(name:str, user: User) -> User:
    """modify an existing user"""
    qry = "UPDATE users SET name=:name, hash=:hash WHERE name=:name0"
    params = {
        "name": user.name,
        "hash": user.hash,
        "name0": name
    }
    cursor.execute(qry, params)
    conn.commit()
    return get_one(user.name)

def delete(name: str) -> None:
    """delete a user by name"""
    user = get_one(name)
    qry = "DELETE FROM users WHERE name=:name"
    params = {"name": name}
    cursor.execute(qry, params)
    conn.commit()
    create(user, table="xusers")

