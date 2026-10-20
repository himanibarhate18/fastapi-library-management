
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=150)
    isbn: str | None = Field(default=None, max_length=20)
    total_copies: int = Field(default=1, ge=1)


class BookUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=150)
    isbn: str | None = Field(default=None, max_length=20)
    total_copies: int = Field(ge=1)


class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    author: str
    isbn: str | None
    total_copies: int
    available_copies: int


class MemberCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    email: EmailStr


class MemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr


class BorrowRequest(BaseModel):
    book_id: int = Field(gt=0)
    member_id: int = Field(gt=0)
    due_date: datetime | None = None


class BorrowResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    book_id: int
    member_id: int
    borrow_date: datetime
    due_date: datetime | None
    return_date: datetime | None
    status: str
