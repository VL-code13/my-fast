# migrations/env.py
"""
Конфигурация окружения Alembic для async SQLAlchemy.

Связывает Alembic с:
  1. Настройками приложения (settings.database_url из .env).
  2. Метаданными моделей (Base.metadata).
  3. Асинхронным движком SQLAlchemy.

Документация: https://alembic.sqlalchemy.org/en/latest/cookbook.html
"""

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from my_fastapi_app.config import get_settings
from my_fastapi_app.database import Base

# КРИТИЧЕСКИ ВАЖНО: импортируем все модели, чтобы они зарегистрировались
# в Base.metadata. Alembic сравнивает Base.metadata с текущим состоянием БД
# и на основе этого автогенерирует миграции. Без этого импорта Alembic
# решит, что таблиц нет, и создаст пустую миграцию.
from my_fastapi_app.items import models  # noqa: F401

# Alembic Config — объект конфигурации из alembic.ini.
config = context.config

# Настраиваем логирование согласно alembic.ini.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Подставляем URL из настроек приложения в конфиг Alembic.
settings = get_settings()
config.set_main_option("sqlalchemy.url", settings.database_url)

# Метаданные моделей — то, с чем Alembic будет сравнивать БД.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Режим offline: генерирует SQL-скрипт без подключения к БД.
    Запуск: alembic upgrade head --sql
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


def do_run_migrations(connection: Connection) -> None:
    """Общая логика запуска миграций для online-режима."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    Async-режим: подключается к БД и применяет миграции.
    NullPool — пул соединений не нужен, миграции одноразовые.
    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Запуск async-миграций через asyncio."""
    asyncio.run(run_async_migrations())


# Alembic сам определит режим по флагу --sql в командной строке.
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()