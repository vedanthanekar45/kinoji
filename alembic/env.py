import os
import sys
from logging.config import fileConfig

from dotenv import load_dotenv
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# --- CUSTOM ADDITIONS ---
# Add the project's root directory to the Python path
# This allows Alembic to find your models file
sys.path.append('..')

# Import your models' Base object
from db.movie_models import Base

# Load the .env file
load_dotenv(dotenv_path='../.env')
# --- END CUSTOM ADDITIONS ---


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# --- CUSTOM ADDITION ---
# Get your database URL from the environment variable
db_url = os.getenv('DATABASE_URL')
# Set the sqlalchemy.url key in the config object
config.set_main_option('sqlalchemy.url', db_url)
# --- END CUSTOM ADDITION ---

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- CUSTOM ADDITION ---
# Set the target_metadata to your models' metadata
target_metadata = Base.metadata
# --- END CUSTOM ADDITION ---


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    """
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
    """Run migrations in 'online' mode.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()