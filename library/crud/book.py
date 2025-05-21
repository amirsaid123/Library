from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from library.models import Book


async def get_books(session: AsyncSession, skip: int = 0, limit: int = 10) -> list[Book]:
    result = await session.execute(select(Book).offset(skip).limit(limit))
    books = result.scalars().all()
    return books


async def get_book_by_id(session: AsyncSession, book_id: int) -> Book:
    result = await session.execute(select(Book).filter(Book.id == book_id))
    book = result.scalar_one_or_none()
    return book


async def create_book_db(session: AsyncSession, book_data: dict) -> Book:
    book = Book(**book_data)
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return book


async def update_book_db(session: AsyncSession, book_id: int, book_data: dict) -> Book:
    book = await get_book_by_id(session, book_id)
    if book:
        for key, value in book_data.items():
            setattr(book, key, value)

        await session.commit()
        await session.refresh(book)
        return book
    return None


async def delete_book_db(session: AsyncSession, book_id: int) -> bool:
    book = await get_book_by_id(session, book_id)
    if book:
        await session.delete(book)
        await session.commit()
        return True

    return False
