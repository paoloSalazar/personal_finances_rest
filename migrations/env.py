from logging.config import fileConfig
import os

from sqlalchemy import engine_from_config, create_engine
from sqlalchemy import pool

from alembic import context

# Import your models and Base
from model.tables.category import Category
from model.tables.daily_finance import DailyFinance
from model.tables.user import User
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