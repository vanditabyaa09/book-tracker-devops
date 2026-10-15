from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    author: Mapped[str] = mapped_column(String(120))
    status: Mapped[str] = mapped_column(String(20), default="to-read")
    rating: Mapped[int | None] = mapped_column(nullable=True)