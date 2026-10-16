from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas
from .database import get_db

router = APIRouter(prefix="/api/books", tags=["books"])

DbSession = Annotated[Session, Depends(get_db)]


def _get_or_404(db: Session, book_id: int) -> models.Book:
    book = db.get(models.Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.get("", response_model=list[schemas.BookOut])
def list_books(db: DbSession):
    return db.query(models.Book).order_by(models.Book.id).all()


@router.get("/{book_id}", response_model=schemas.BookOut)
def get_book(book_id: int, db: DbSession):
    return _get_or_404(db, book_id)


@router.post("", response_model=schemas.BookOut, status_code=201)
def create_book(payload: schemas.BookIn, db: DbSession):
    book = models.Book(**payload.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@router.put("/{book_id}", response_model=schemas.BookOut)
def update_book(book_id: int, payload: schemas.BookIn, db: DbSession):
    book = _get_or_404(db, book_id)
    for field, value in payload.model_dump().items():
        setattr(book, field, value)
    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, db: DbSession):
    db.delete(_get_or_404(db, book_id))
    db.commit()