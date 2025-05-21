from fastapi import APIRouter, HTTPException
from library.crud import get_reader_by_id
from library.crud.book import get_book_by_id
from library.crud.borrow import *
from library.database import SessionDep
from library.schemas import BorrowOut, BorrowInput, ReturnInput
from library.utils import CurrentUser

router = APIRouter(prefix="/books", tags=["Borrowing"])


@router.post("/lend", response_model=BorrowOut)
async def lend_book(data: BorrowInput, session: SessionDep, current_user: CurrentUser):
    book = await get_book_by_id(session, data.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    reader = await get_reader_by_id(session, data.reader_id)
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")

    if book.copy < 1:
        raise HTTPException(status_code=400, detail="No available copies")

    active_borrows = await count_active_borrows(session, data.reader_id)
    if active_borrows >= 3:
        raise HTTPException(status_code=400, detail="Reader has reached the borrow limit (3 books)")

    already_borrowed = await has_active_borrow(session, data.reader_id, data.book_id)
    if already_borrowed:
        raise HTTPException(status_code=400, detail="Reader already borrowed this book and has not returned it")

    await update_book_copies(session, book, decrement=True)
    borrow_record = await create_borrow_record(session, data.book_id, data.reader_id)

    return borrow_record


@router.post("/return", response_model=BorrowOut)
async def return_book(data: ReturnInput, session: SessionDep, current_user: CurrentUser):
    borrow = await get_borrow_record(session, data.borrow_id)
    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow record not found")

    if borrow.return_date is not None:
        raise HTTPException(status_code=400, detail="Book already returned")

    if borrow.reader_id != data.reader_id:
        raise HTTPException(status_code=403, detail="This book was not borrowed by this reader")

    book = await get_book_by_id(session, borrow.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    await update_borrow_record(session, borrow.id)

    await update_book_copies(session, book, decrement=False)

    await session.refresh(borrow)
    return borrow


@router.get("/borrows/{reader_id}", response_model=list[BorrowOut])
async def get_borrows_by_reader(reader_id: int, session: SessionDep, current_user: CurrentUser):
    borrows = await get_borrowed_books_by_reader(session, reader_id)
    if not borrows:
        raise HTTPException(status_code=404, detail="Reader has no borrowed books")
    return borrows


@router.get("/borrows/notreturn/{reader_id}", response_model=list[BorrowOut])
async def get_borrows_by_reader(reader_id: int, session: SessionDep, current_user: CurrentUser):
    borrows = await get_not_returned_books_by_reader(session, reader_id)
    if not borrows:
        raise HTTPException(status_code=404, detail="Reader has no borrowed books")
    return borrows
