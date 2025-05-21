from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from library.models import Reader


async def get_readers(session: AsyncSession) -> list[Reader]:
    result = await session.execute(select(Reader))
    readers = result.scalars().all()
    return readers


async def get_reader_by_id(session: AsyncSession, reader_id: int) -> Reader:
    result = await session.execute(select(Reader).filter(Reader.id == reader_id))
    reader = result.scalar_one_or_none()
    return reader


async def create_reader_db(session: AsyncSession, reader_data: dict) -> Reader:
    reader = Reader(**reader_data)
    session.add(reader)
    await session.commit()
    await session.refresh(reader)
    return reader


async def update_reader_db(session: AsyncSession, reader_id: int, reader_data: dict) -> Reader:
    reader = await get_reader_by_id(session, reader_id)
    if reader:
        for key, value in reader_data.items():
            setattr(reader, key, value)

        await session.commit()
        await session.refresh(reader)
        return reader
    return None


async def delete_reader_db(session: AsyncSession, reader_id: int) -> bool:
    reader = await get_reader_by_id(session, reader_id)
    if reader:
        await session.delete(reader)
        await session.commit()
        return True
    return False
