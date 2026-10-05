"""
Точка входа в FastAPI-приложение.

Официальная документация FastAPI: https://fastapi.tiangolo.com/
Официальная документация Pydantic: https://docs.pydantic.dev/
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field

# Создаём экземпляр приложения FastAPI.
# Параметры title, description, version попадают в OpenAPI-схему
# и отображаются в автоматической документации (Swagger UI / ReDoc).
app = FastAPI(
    title="My FastAPI",
    description="Учебный проект для освоения FastAPI на  UV",
    version="0.1.0",
)


class Item(BaseModel):
    """
    Pydantic-модель элемента.

    Pydantic v2 автоматически:
      1. Проверяет типы полей при получении запроса.
      2. Возвращает 422 Unprocessable Entity с деталями ошибки при несоответствии.
      3. Генерирует JSON Schema для OpenAPI-документации.
      4. Сериализует ответ обратно в JSON.

    Field(...) — обязательное поле (многоточие = отсутствие значения по умолчанию).
    Field(None) — опциональное поле со значением по умолчанию None.
    """

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Название элемента",
    )
    price: float = Field(
        ...,
        gt=0,
        description="Цена должна быть строго положительной",
    )


@app.get("/")
async def root() -> dict[str, str]:
    """
    GET / — корневой эндпоинт.

    Возвращает приветственное сообщение в формате JSON.
    FastAPI автоматически сериализует dict в JSON-ответ.
    """
    return {"message": "Hello, FastAPI with UV!"}


@app.post("/items")
async def create_item(item: Item) -> Item:
    """
    POST /items — создание элемента.

    Параметр `item: Item` автоматически:
      - Извлекается из тела запроса (JSON).
      - Валидируется через Pydantic.
      - Передаётся в функцию как объект Item.

    Если данные невалидны — FastAPI возвращает 422 с деталями ошибки.
    Ответ сериализуется обратно в JSON согласно схеме Item.
    """
    return item
