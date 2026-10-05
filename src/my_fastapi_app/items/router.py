# src/my_fastapi_app/items/router.py
"""
HTTP-роутер для домена "items".

Здесь только HTTP-обвязка: валидация, вызов сервиса, формирование ответа.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from my_fastapi_app.database import get_db

from . import service
from .models import Item
from .schemas import ItemCreate, ItemResponse

router = APIRouter(prefix="/items", tags=["items"])

# Annotated[AsyncSession, Depends(get_db)] — современный способ объявить
# зависимость. Это делает сигнатуру читаемой и переиспользуемой.
DbSession = Annotated[AsyncSession, Depends(get_db)]


@router.get("", response_model=list[ItemResponse])
async def read_items(db: DbSession) -> list[Item]:
    """Возвращает список всех элементов."""
    return await service.get_items(db)


@router.get("/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int, db: DbSession) -> Item:
    """Возвращает элемент по ID или 404."""
    item = await service.get_item_by_id(db, item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found",
        )
    return item


@router.post(
    "",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_item(item_in: ItemCreate, db: DbSession) -> Item:
    """Создаёт новый элемент."""
    return await service.create_item(db, item_in)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, db: DbSession) -> None:
    """Удаляет элемент по ID или 404."""
    deleted = await service.delete_item(db, item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found",
        )
