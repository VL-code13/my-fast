# src/my_fastapi_app/items/models.py
"""
SQLAlchemy-модели для домена "items".

Модель — это описание таблицы в БД. Каждый класс = таблица,
каждый атрибут = колонка.
"""

from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from my_fastapi_app.database import Base


class Item(Base):
    """
    Модель элемента.

    Соответствует таблице "items" в БД.
    SQLAlchemy 2.0 использует типизированный стиль с Mapped[...]:
      - Mapped[int] → колонка типа INTEGER NOT NULL
      - Mapped[str | None] → колонка типа VARCHAR NULL
    Это даёт полную типизацию для mypy и IDE.
    """

    # __tablename__ — имя таблицы в БД. Не указывать — SQLAlchemy сгенерирует
    # автоматически (например, "item"), но явное имя лучше.
    __tablename__ = "items"

    # primary_key=True → PRIMARY KEY.
    # autoincrement=True по умолчанию для Integer — БД сама назначает ID.
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # String(100) → VARCHAR(100). Ограничение длины на уровне БД.
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Float для цены. В реальных проектах с деньгами используют Numeric
    # (точная арифметика без потерь), но для обучения Float достаточен.
    price: Mapped[float] = mapped_column(Float, nullable=False)

    # server_default=func.now() → значение по умолчанию на уровне БД (CURRENT_TIMESTAMP).
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        """Строковое представление для отладки."""
        return f"<Item(id={self.id}, name={self.name!r}, price={self.price})>"
