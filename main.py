
from datetime import datetime, timezone

from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import models
import schemas
from database import Base, engine, get_db

# Ensure the tables are available when the application starts.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management System",
    description="API for managing books, members, and borrowing records.",
    version="1.0.0",
)


@app.get("/")
def home():
    return {"message": "Library Management System API is running!"}


# -------------------- BOOKS --------------------

@app.get("/books", response_model=list[schemas.BookResponse])
def get_books(db: Session = Depends(get_db)):
    return db.scalars(select(models.Book).order_by(models.Book.id)).all()


@app.get("/books/{book_id}", response_model=schemas.BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(models.Book, book_id)

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@app.post(
    "/books",
    response_model=schemas.BookResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_book(data: schemas.BookCreate, db: Session = Depends(get_db)):
    book = models.Book(
        title=data.title,
        author=data.author,
        isbn=data.isbn,
        total_copies=data.total_copies,
        available_copies=data.total_copies,
    )

    db.add(book)

    try:
        db.commit()
        db.refresh(book)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A book with this ISBN already exists",
        )

    return book


@app.put("/books/{book_id}", response_model=schemas.BookResponse)
def update_book(
    book_id: int,
    data: schemas.BookUpdate,
    db: Session = Depends(get_db),
):
    book = db.get(models.Book, book_id)

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    borrowed_copies = book.total_copies - book.available_copies

    if data.total_copies < borrowed_copies:
        raise HTTPException(
            status_code=400,
            detail="Total copies cannot be less than the number currently borrowed",
        )

    book.title = data.title
    book.author = data.author
    book.isbn = data.isbn
    book.total_copies = data.total_copies
    book.available_copies = data.total_copies - borrowed_copies

    try:
        db.commit()
        db.refresh(book)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A book with this ISBN already exists",
        )

    return book


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(models.Book, book_id)

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    records = db.scalars(
        select(models.BorrowRecord).where(
            models.BorrowRecord.book_id == book_id
        )
    ).all()

    if records:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete a book with borrowing history",
        )

    db.delete(book)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# -------------------- MEMBERS --------------------

@app.get("/members", response_model=list[schemas.MemberResponse])
def get_members(db: Session = Depends(get_db)):
    return db.scalars(
        select(models.Member).order_by(models.Member.id)
    ).all()


@app.get("/members/{member_id}", response_model=schemas.MemberResponse)
def get_member(member_id: int, db: Session = Depends(get_db)):
    member = db.get(models.Member, member_id)

    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")

    return member


@app.post(
    "/members",
    response_model=schemas.MemberResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_member(data: schemas.MemberCreate, db: Session = Depends(get_db)):
    member = models.Member(name=data.name, email=str(data.email))
    db.add(member)

    try:
        db.commit()
        db.refresh(member)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A member with this email already exists",
        )

    return member


# -------------------- BORROWING --------------------

@app.post(
    "/borrow",
    response_model=schemas.BorrowResponse,
    status_code=status.HTTP_201_CREATED,
)
def borrow_book(data: schemas.BorrowRequest, db: Session = Depends(get_db)):
    book = db.get(models.Book, data.book_id)

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    member = db.get(models.Member, data.member_id)

    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")

    if book.available_copies <= 0:
        raise HTTPException(
            status_code=400,
            detail="No copies of this book are currently available",
        )

    if data.due_date is not None:
        if data.due_date.tzinfo is not None:
            due_date = data.due_date.astimezone(timezone.utc).replace(tzinfo=None)
        else:
            due_date = data.due_date

        if due_date <= datetime.utcnow():
            raise HTTPException(
                status_code=422,
                detail="Due date must be in the future",
            )
    else:
        due_date = None

    book.available_copies -= 1

    record = models.BorrowRecord(
        book_id=data.book_id,
        member_id=data.member_id,
        due_date=due_date,
        status="borrowed",
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


@app.post(
    "/return/{record_id}",
    response_model=schemas.BorrowResponse,
)
def return_book(record_id: int, db: Session = Depends(get_db)):
    record = db.get(models.BorrowRecord, record_id)

    if record is None:
        raise HTTPException(
            status_code=404,
            detail="Borrowing record not found",
        )

    if record.status == "returned":
        raise HTTPException(
            status_code=400,
            detail="This book has already been returned",
        )

    book = db.get(models.Book, record.book_id)

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book associated with this record was not found",
        )

    record.status = "returned"
    record.return_date = datetime.utcnow()
    book.available_copies += 1

    db.commit()
    db.refresh(record)

    return record


@app.get(
    "/borrow-records",
    response_model=list[schemas.BorrowResponse],
)
def get_borrow_records(db: Session = Depends(get_db)):
    return db.scalars(
        select(models.BorrowRecord).order_by(
            models.BorrowRecord.id.desc()
        )
    ).all()
