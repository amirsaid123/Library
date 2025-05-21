from datetime import date
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from library.models import BorrowedBook

# Counts how many books a reader has borrowed, but not yet returned.
async def count_active_borrows(session: AsyncSession, reader_id: int) -> int:
    result = await session.execute(
        select(func.count()).select_from(BorrowedBook)
        .where(BorrowedBook.reader_id == reader_id, BorrowedBook.return_date == None)
    )
    return result.scalar()

# Creates a new borrow record for a book.
async def create_borrow_record(session: AsyncSession, book_id: int, reader_id: int) -> BorrowedBook:
    borrow = BorrowedBook(
        book_id=book_id,
        reader_id=reader_id,
        borrow_date=date.today(),
    )
    session.add(borrow)
    await session.commit()
    await session.refresh(borrow)
    return borrow

# If reader borrowed a book, then decrease the number of copies by 1 else increases by 1
async def update_book_copies(session: AsyncSession, book, decrement: bool = True):
    book.copy += -1 if decrement else 1
    await session.commit()
    await session.refresh(book)

# Retrieves a borrow record by its ID.
async def get_borrow_record(session: AsyncSession, borrow_id: int) -> BorrowedBook:
    result = await session.execute(select(BorrowedBook).filter(BorrowedBook.id == borrow_id))
    borrow = result.scalar_one_or_none()
    return borrow

# Updates borrow record's return date when a book is returned
async def update_borrow_record(session: AsyncSession, borrow_id: int) -> BorrowedBook | None:
    borrow = await get_borrow_record(session, borrow_id)

    if not borrow:
        return None

    if borrow.return_date:
        return borrow

    borrow.return_date = date.today()
    await session.commit()
    await session.refresh(borrow)
    return borrow

# Checks whether a reader has already borrowed a book. If so, return True else False.
async def has_active_borrow(session: AsyncSession, reader_id: int, book_id: int) -> bool:
    stmt = select(BorrowedBook).where(
        BorrowedBook.reader_id == reader_id,
        BorrowedBook.book_id == book_id,
        BorrowedBook.return_date.is_(None)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none() is not None

# Retrieves all borrowed books by a reader.
async def get_borrowed_books_by_reader(session: AsyncSession, reader_id: int) -> list[BorrowedBook]:
    result = await session.execute(select(BorrowedBook).where(BorrowedBook.reader_id == reader_id))
    borrowed_books = result.scalars().all()
    return borrowed_books

# Retrieves all not returned books by a reader.
async def get_not_returned_books_by_reader(session: AsyncSession, reader_id: int) -> list[BorrowedBook]:
    result = await session.execute(select(BorrowedBook).where(BorrowedBook.reader_id == reader_id, BorrowedBook.return_date.is_(None)))
    borrowed_books = result.scalars().all()
    return borrowed_books
