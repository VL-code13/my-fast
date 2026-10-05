# src/my_fastapi_app/items/schemas.py
"""
Pydantic-схемы для домена "items".

Эти модели описывают структуру данных для API.
Они не являются моделями БД. Это DTO (Data Transfer Object).
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ItemBase(BaseModel):
    """Базовая схема с общими полями."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Название элемента",
        examples=["MacBook Pro 14"],
    )
    price: float = Field(
        ...,
        gt=0,
        description="Цена должна быть строго положительной",
        examples=[1999.99],
    )


class ItemCreate(ItemBase):
    """
    Схема для создания элемента (POST-запрос).
    Наследует все поля из ItemBase.
    """


class ItemResponse(ItemBase):
    """
    Схема для ответа API (то, что видит клиент).
    Добавляет поля, которые генерируются на сервере.
    """

    id: int = Field(..., description="Уникальный идентификатор элемента")
    created_at: datetime = Field(..., description="Дата создания (UTC)")

    # from_attributes=True — ключевая настройка для сериализации ORM-объектов.
    # Без неё FastAPI попытается прочитать поля как элементы словаря
    # (item["id"]) и упадёт с ResponseValidationError, потому что ORM-объект —
    # это не dict, а объект с атрибутами (item.id).
    model_config = ConfigDict(from_attributes=True)
