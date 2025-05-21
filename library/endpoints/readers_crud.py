from fastapi import APIRouter, HTTPException
from library.crud.reader import *
from library.database import SessionDep
from library.schemas import ReaderOut, ReaderCreate, ReaderPutUpdate, ReaderPatchUpdate
from library.utils import CurrentUser

router = APIRouter(prefix="/readers", tags=["Readers"])


@router.get("/", response_model=list[ReaderOut])
async def get_readers_list(session: SessionDep, current_user: CurrentUser):
    readers = await get_readers(session)
    return readers


@router.get("/{reader_id}", response_model=ReaderOut)
async def get_reader(reader_id: int, session: SessionDep, current_user: CurrentUser):
    reader = await get_reader_by_id(session, reader_id)
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    return reader


@router.post("/create", response_model=ReaderOut)
async def create_reader(session: SessionDep, current_user: CurrentUser, reader_data: ReaderCreate):
    reader = await create_reader_db(session, reader_data.model_dump())
    return reader


@router.put("/put/{reader_id}", response_model=ReaderOut)
async def put_update_reader(reader_id: int, session: SessionDep, current_user: CurrentUser,
                            reader_data: ReaderPutUpdate):
    reader = await update_reader_db(session, reader_id, reader_data.model_dump())
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    return reader


@router.patch("/patch/{reader_id}", response_model=ReaderOut)
async def patch_update_reader(reader_id: int, session: SessionDep, current_user: CurrentUser,
                              reader_data: ReaderPatchUpdate):
    update_data = {k: v for k, v in reader_data.model_dump().items() if v is not None}
    reader = await update_reader_db(session, reader_id, update_data)
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    return reader


@router.delete("/delete/{reader_id}")
async def delete_reader(reader_id: int, session: SessionDep, current_user: CurrentUser):
    deleted = await delete_reader_db(session, reader_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Reader not found")
    return {"message": "Reader deleted successfully"}
