from fastapi import APIRouter, HTTPException
from library.crud.book import get_books, get_book_by_id, create_book_db, update_book_db, delete_book_db
from library.database import SessionDep
from library.schemas import BookOut, BookCreate, BookPutUpdate, BookPatchUpdate
from library.utils import CurrentUser

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=list[BookOut])
async def get_books_list(session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 10):
    books = await get_books(session, skip, limit)
    return books


@router.get("/{book_id}", response_model=BookOut)
async def get_book(book_id: int, session: SessionDep, current_user: CurrentUser):
    book = await get_book_by_id(session, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("/create", response_model=BookOut)
async def create_book(session: SessionDep, current_user: CurrentUser, book_data: BookCreate):
    book = await create_book_db(session, book_data.model_dump())
    return book


@router.patch("/patch/{book_id}", response_model=BookOut)
async def patch_update_book(book_id: int, session: SessionDep, current_user: CurrentUser, book_data: BookPatchUpdate):
    update_data = {k: v for k, v in book_data.model_dump().items() if v is not None}
    book = await update_book_db(session, book_id, update_data)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/put/{book_id}", response_model=BookOut)
async def put_update_book(book_id: int, session: SessionDep, current_user: CurrentUser, book_data: BookPutUpdate):
    book = await update_book_db(session, book_id, book_data.model_dump())
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.delete("/delete/{book_id}")
async def delete_book(book_id: int, session: SessionDep, current_user: CurrentUser):
    deleted = await delete_book_db(session, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}
