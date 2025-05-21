from datetime import date
from typing import Optional
from pydantic import BaseModel
from pydantic import EmailStr


# It is used for creating a user.
class UserCreate(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


# Main pydantic model for Book
class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    year: Optional[int] = None
    isbn: Optional[str] = None
    copy: int = 1

    class Config:
        from_attributes = True


# While creating a book, it doesn't require the id.
class BookCreate(BookBase):
    pass


# While creating a book, it doesn't require the id from here, but from path parameters.
class BookPutUpdate(BookBase):
    pass


# While creating a book, it doesn't require the id from here, but from path parameters.
# It is a patch method, therefore every field is optional.
class BookPatchUpdate(BookBase):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    year: Optional[int] = None
    isbn: Optional[str] = None
    copy: Optional[int] = None


# While returning book info, it returns the id as well.
class BookOut(BookBase):
    id: int


# Main pydantic model for Reader
class ReaderBase(BaseModel):
    full_name: str
    email: EmailStr


# Just inheritances from ReaderBase because nothing changes here
class ReaderCreate(ReaderBase):
    pass


# Just inheritances from ReaderBase because nothing changes here
class ReaderPutUpdate(ReaderBase):
    pass


# Makes fields optional because it is a patch method.
class ReaderPatchUpdate(ReaderBase):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None


# It is user for returning reader info, so id field is added
class ReaderOut(ReaderBase):
    id: int


# It is used for creating borrow record
class BorrowInput(BaseModel):
    book_id: int
    reader_id: int


# Returns all data about borrow record.
class BorrowOut(BaseModel):
    id: int
    book_id: int
    reader_id: int
    borrow_date: date
    return_date: Optional[date] = None


# It is used for returning borrow record.
class ReturnInput(BaseModel):
    borrow_id: int
    reader_id: int
