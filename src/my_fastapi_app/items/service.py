# src/my_fastapi_app/items/service.py
"""
Сервисный слой для домена "items".

Здесь находится бизнес-логика. В идеале, этот слой не должен ничего
знать о HTTP (FastAPI) и о том, как данные хранятся (SQLAlchemy).
Он оперирует абстрактными понятиями.
"""

from typing import List, Optional, Dict
from .schemas import ItemCreate, ItemResponse

# Временное in-memory хранилище. Позже мы заменим его на БД.
# Аннотация Dict[int, ItemResponse] говорит mypy, что это словарь.
_fake_db: Dict[int, ItemResponse] = {}
_last_id: int = 0


def get_item() -> List[ItemResponse]:
    """Возвращает список всех элементов."""

    return list(_fake_db.values())

def get_item(item_create: ItemCreate) -> ItemResponse:
    """
        Создаёт новый элемент.
        Генерирует ID и сохраняет в "базу".
    """
    global _last_id
    _last_id += 1
    item = ItemResponse(id=_last_id, **item_create.model_dump())
    _fake_db[item.id] = item
    return item

def delete_item(item_id: int) -> bool:
    """
        Удаляет элемент по ID.
        Возвращает True, если элемент был удалён, иначе False.
    """
    if item_id in _fake_db:
        del _fake_db[item_id]
        return True
    return False
"""
Изоляция: Сервисный слой ничего не знает о Request, Response или HTTPException. Это позволяет легко тестировать бизнес-логику в отрыве от веб-фреймворка.

Переиспользование: Эти же функции можно будет вызывать из фоновой задачи или из CLI-скрипта.
"""

