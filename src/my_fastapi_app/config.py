# src/my_fastapi_app/config.py
"""
Конфигурация приложения.

Все настройки читаются из переменных окружения или .env-файла.
Это требование 12-factor app (https://12factor.net/config) —
секреты и настройки НЕ хранятся в коде.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Настройки приложения.

    Pydantic-settings автоматически:
      1. Читает переменные окружения (например, DATABASE_URL).
      2. Читает .env-файл, если он есть.
      3. Валидирует типы.
      4. Приводит к верхнему регистру ключи в .env для сопоставления.

    Пример .env:
        DATABASE_URL=sqlite+aiosqlite:///./app.db
        DEBUG=true
    """

    database_url: str = "sqlite+aiosqlite:///./app.db"

    # Режим отладки. В продакшене — False.
    debug: bool = False

    # Название приложения (отображается в документации).
    app_name: str = "My FastAPI App"

    # model_config — настройка самого класса Settings.
    # env_file=".env" — путь к файлу переменных окружения.
    # env_file_encoding — кодировка.
    # extra="ignore" — игнорировать незнакомые переменные в .env (иначе упадёт).
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# lru_cache — кэширует результат функции.
# Без него на каждый вызов Settings() создавался бы новый объект,
# заново читающий .env. С кэшем — настройки читаются один раз при старте.
# Это стандартный паттерн для get_settings в FastAPI.
@lru_cache
def get_settings() -> Settings:
    """
    Возвращает единственный экземпляр настроек.
    Используется как зависимость (Depends) в FastAPI.
    """
    return Settings()
