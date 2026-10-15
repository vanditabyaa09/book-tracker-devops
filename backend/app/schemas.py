from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Status = Literal["to-read", "reading", "done"]


class BookIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=120)
    status: Status = "to-read"
    rating: int | None = Field(default=None, ge=1, le=5)


class BookOut(BookIn):
    id: int
    model_config = ConfigDict(from_attributes=True)