# My Daily Finances REST API
## File Structure

personal_finances_rest
├── README.md
├── api.rest
├── data
│   ├── __init__.py
│   ├── category.py
│   └── init.py
├── db
│   └── personal_finances.db
├── fake
│   ├── __init__.py
│   └── category.py
├── main.py
├── model
│   ├── __init__.py
│   └── category.py
├── pyproject.toml
├── requirements.txt
├── service
│   ├── __init__.py
│   └── category.py
├── test
│   ├── __init__.py
│   └── unit
│       └── service
│           └── test_category.py
└── web
    ├── __init__.py
    └── category.py

* main.py is the main file in which the start of the project is setup
* web folder: rest api end points
* service: project logic 
* model: database models
* data: database setup

## Migrations
Using alembic to add migrations feature

* include alembic to requirements file
```python
fastapi
uvicorn
pydantic
pytest
alembic
```
* Init migrations 
```bash
$ alembic init migrations
```
This is going to generate migrations/ directory
* Edit the _migrations/env.py_ file 
```python
from logging.config import fileConfig
import os

from sqlalchemy import engine_from_config, create_engine
from sqlalchemy import pool

from alembic import context

# Import your models and Base
from model.tables.category import Category
from model.database import Base

# this is the Alembic Config object
config = context.config

# Get database URL from config
DB_URL = config.get_main_option("sqlalchemy.url")
DB_PATH = DB_URL.replace("sqlite:///", "")
DB_DIR = os.path.dirname(DB_PATH)

# Create database directory if it doesn't exist
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

# Create database if it doesn't exist
if not os.path.exists(DB_PATH):
    engine = create_engine(DB_URL)
    Base.metadata.create_all(engine)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )


    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            render_as_batch=("sqlite" in str(connectable.dialect.name))
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```
* update model folder
model/
├── __init__.py
├── database.py
├── schemas/
│   ├── __init__.py
│   └── category.py
└── tables/
    ├── __init__.py
    └── category.py
schemas contains the pydantic models
```python
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
```
tables contains the necesary conf for database tables
```python
from sqlalchemy import Column, Integer, String
from ..database import Base
from sqlalchemy import Column, Integer, String, DateTime, func

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(280), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
```
### Commands to run migrations
```bash
$ alembic revision --autogenerate -m "add created_at and updated_at fields
$ alembic upgrade head
```

### Issues
unable to run alter queries
Fix: edit migrations/env.py
```python
context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            render_as_batch=("sqlite" in str(connectable.dialect.name))
        )
```


Deleted migrations/versions folder
If you deleted the migrations/versions folder, you have three concise recovery options:

Restore from VCS or backup (recommended if available)
```bash
# restore the folder from the last commit
git checkout -- migrations/versions
```
Recreate a baseline revision (if you don't have old migration files)
```bash
# create a new migration script reflecting current models
alembic revision --autogenerate -m "recreate migrations"

# if the DB already contains the current schema, mark it as up-to-date
alembic stamp head
```
Recreate and apply migrations from scratch (if starting fresh)
```bash
alembic revision --autogenerate -m "initial"
alembic upgrade head
```

## Changing database to use postgres
how can I setup a docker container with postgres empty server.
In the future I would like to change the database implementation to use postgres

I've created the Docker setup for PostgreSQL. Here's what you need to do:

Files Created:
Dockerfile - Uses PostgreSQL 15 Alpine image with your database configuration
docker-compose.yml - Orchestrates the PostgreSQL container with persistent storage
.env.example - Example environment variables for database connection

```bash
# Build and start the PostgreSQL container
docker-compose up -d

# Check if it's running
docker-compose ps

# View logs
docker-compose logs postgres

# Connect to PostgreSQL (from host)
psql -h localhost -p 5432 -U finance_user -d personal_finances
```

## Security and authentication
Generate ssl files
```bash
$ openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 -subj "/CN=localhost"

```
This creates:

* ssl/key.pem - Your private key
* ssl/cert.pem - Your certificate

then include files at starting fastapi
```python
import uvicorn

uvicorn.run(
    "main:app",
    host="0.0.0.0",
    port=8000,
    ssl_keyfile="ssl/key.pem",      # Private key
    ssl_certfile="ssl//cert.pem",     # Certificate
)   
```