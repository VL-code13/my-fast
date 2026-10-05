# src/my_fastapi_app/items/router.py
"""
HTTP-роутер для домена "items".

Здесь описываются эндпоинты (пути, методы, статус-коды).
Логика вынесена в сервисный слой.
"""

from fastapi import APIRouter, HTTPException, status

from . import service
from .schemas import ItemCreate, ItemResponse

# Создаём роутер для нашего домена.
# prefix="/items" — все пути будут начинаться с /items.
# tags=["items"] — группировка в Swagger UI.
router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=list[ItemResponse])
async def read_items():
    """
    Возвращает список всех элементов.
    """
    return service.get_items()


@router.get("/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int):
    """
    Возвращает элемент по его ID.
    Если элемента нет — возвращает 404.
    """
    item = service.get_item_by_id(item_id)
    if item is None:
        # Важно: используем HTTPException, а не возвращаем dict с кодом ошибки.
        # FastAPI сам сформирует корректный JSON-ответ.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found",
        )
    return item


@router.post(
    "/",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_item(item_in: ItemCreate):
    """
    Создаёт новый элемент.
    Возвращает созданный элемент со статусом 201.
    """
    return service.create_item(item_in)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    """
    Удаляет элемент по ID.
    При успехе возвращает 204 No Content.
    """
    deleted = service.delete_item(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found",
        )
    # Для 204 не нужно возвращать тело ответа — FastAPI это знает.
    """response_model: FastAPI автоматически сериализует ответ согласно этой модели. Это гарантирует, что клиент не получит "лишние" поля (например, password).

status_code: Мы явно указываем 201 Created для POST и 204 No Content для DELETE. Это следование стандартам REST.

HTTPException: Правильный способ возвращать ошибки. FastAPI перехватит его и сформирует стандартизированный JSON {"detail": "..."}."""