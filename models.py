
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    author = Column(String(150), nullable=False)
    isbn = Column(String(20), unique=True, nullable=True)
    total_copies = Column(Integer, nullable=False, default=1)
    available_copies = Column(Integer, nullable=False, default=1)


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    email = Column(String(255), unique=True, nullable=False)


class BorrowRecord(Base):
    __tablename__ = "borrow_records"

    id = Column(Integer, primary_key=True, index=True)

    book_id = Column(
        Integer,
        ForeignKey("books.id"),
        nullable=False,
    )
    member_id = Column(
        Integer,
        ForeignKey("members.id"),
        nullable=False,
    )

    borrow_date = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    due_date = Column(DateTime, nullable=True)
    return_date = Column(DateTime, nullable=True)
    status = Column(String(20), nullable=False, default="borrowed")
