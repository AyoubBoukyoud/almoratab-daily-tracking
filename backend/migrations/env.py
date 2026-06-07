import sys
import os
import asyncio
import socket
from logging.config import fileConfig

from sqlalchemy import pool, create_engine
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

# Add backend directory to path
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

from core.config import settings
from models import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# The DATABASE_URL is now fully processed in core/config.py
base_url = settings.DATABASE_URL

# For migrations, we switch to sync engine (psycopg2) and port 5432
# because it's much more stable with Supabase/PgBouncer.
# psycopg2 uses client-side interpolation and port 5432 is session mode.
sync_url = base_url.replace("postgresql+asyncpg://", "postgresql://")
if ":6543/" in sync_url:
    sync_url = sync_url.replace(":6543/", ":5432/")

# Overwrite sqlalchemy url with config DATABASE_URL
# Escape percent signs so ConfigParser doesn't break on URL-encoded passwords
escaped_url = sync_url.replace("%", "%%")
config.set_main_option("sqlalchemy.url", escaped_url)

# Interpret the config file for Python logging.
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


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
    We use a sync engine here to bypass asyncpg/PgBouncer issues.
    """
    connectable = create_engine(
        sync_url,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        do_run_migrations(connection)

    connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
