# src/my_fastapi_app/items/service.py
"""
Сервисный слой для домена "items".

Здесь бизнес-логика: работа с БД, транзакции, валидация на уровне домена.
Слой ничего не знает о HTTP.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Item
from .schemas import ItemCreate


async def get_items(db: AsyncSession) -> list[Item]:
    """
    Возвращает список всех элементов.

    Заметь: параметр db — это сессия, которую передаст FastAPI через Depends.
    Функция async, потому что db.execute — корутина.
    """
    # select(Item) — SQLAlchemy 2.0-стиль. Эквивалент SELECT * FROM items.
    # await db.execute(...) — выполняет запрос к БД.
    # result.scalars().all() — извлекает объекты Item из результата.
    result = await db.execute(select(Item).order_by(Item.id))
    return list(result.scalars().all())


async def get_item_by_id(db: AsyncSession, item_id: int) -> Item | None:
    """
    Находит элемент по ID.

    Возвращает объект Item или None, если не найден.
    """
    # db.get(Item, item_id) — оптимальный способ получить по PK.
    # SQLAlchemy сначала смотрит в identity map (кэш сессии),
    # и только потом идёт в БД. Это быстрее, чем select().where().
    return await db.get(Item, item_id)


async def create_item(db: AsyncSession, item_in: ItemCreate) -> Item:
    """
    Создаёт новый элемент.

    Транзакция:
      1. Создаём ORM-объект из Pydantic-схемы.
      2. Добавляем в сессию.
      3. Коммитим — данные идут в БД.
      4. refresh — читаем сгенерированные БД поля (id, created_at).
    """
    # model_dump() — превращает Pydantic-модель в dict.
    # ** распаковывает dict в именованные аргументы.
    item = Item(**item_in.model_dump())

    # add() — помещает объект в сессию (ещё не в БД).
    db.add(item)

    # commit() — фиксирует транзакцию. Все изменения уходят в БД.
    await db.commit()

    # refresh() — перечитывает объект из БД. Нужен, чтобы получить
    # значения, сгенерированные БД (id, created_at).
    await db.refresh(item)

    return item


async def delete_item(db: AsyncSession, item_id: int) -> bool:
    """
    Удаляет элемент по ID.

    Возвращает True, если удалён, иначе False.
    """
    item = await db.get(Item, item_id)
    if item is None:
        return False

    # await db.delete(item) — помечает объект на удаление.
    # Реальное удаление произойдёт при commit().
    await db.delete(item)
    await db.commit()
    return True
