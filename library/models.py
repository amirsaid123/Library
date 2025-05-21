from datetime import date
from sqlalchemy import String, BIGINT, Integer, text, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)


class Reader(Base):
    __tablename__ = "readers"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)

    borrowed_books = relationship("BorrowedBook", back_populates="reader", passive_deletes=True)


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    author: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=True)
    isbn: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=True)
    copy: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("1"))

    borrowed_books = relationship("BorrowedBook", back_populates="book", passive_deletes=True)


class BorrowedBook(Base):
    __tablename__ = "borrowed_books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    reader_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("readers.id", ondelete="CASCADE"), nullable=False)
    borrow_date: Mapped[date] = mapped_column(Date, nullable=False)
    return_date: Mapped[date] = mapped_column(Date, nullable=True)

    book = relationship("Book", back_populates="borrowed_books")
    reader = relationship("Reader", back_populates="borrowed_books")
