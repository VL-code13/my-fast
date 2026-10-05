# src/my_fastapi_app/main.py
"""
Точка входа в FastAPI-приложение.

Этот файл — «сборочный цех»: создаём приложение и подключаем роутеры.
Никакой бизнес-логики, моделей и эндпоинтов здесь быть не должно.
"""

from fastapi import FastAPI

from my_fastapi_app.config import get_settings
from my_fastapi_app.items.router import router as items_router

# Настройки читаются один раз при старте.
settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Учебный проект для освоения FastAPI на uv",
    version="0.3.0",
    debug=settings.debug,
)

# Подключаем роутер домена items.
# Все эндпоинты из items/router.py становятся частью приложения.
app.include_router(items_router)


@app.get("/")
async def root() -> dict[str, str]:
    """Health check — корневой эндпоинт."""
    return {"message": "Hello, FastAPI with SQLAlchemy!"}
