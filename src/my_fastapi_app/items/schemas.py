"""
Pydantic-схемы для домена "items".

Эти модели описывают структуру данных для API.
Они не являются моделями БД. Это DTO (Data Transfer Object).
"""

from pydantic import BaseModel, Field


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
    pass


class ItemResponse(ItemBase):
    """
        Схема для ответа API (то, что видит клиент).
        Добавляет поля, которые генерируются на сервере.
    """
    id: int = Field(
        ...,
        description="Уникальный идентификатор элемента"
    )
