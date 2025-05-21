from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from library.models import User
from library.utils import hash_password


async def create_user(session: AsyncSession, user_data: dict) -> User:
    user_data['password'] = await hash_password(user_data['password'])
    user = User(**user_data)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_users(session: AsyncSession, skip: int = 0, limit: int = 10) -> list[User]:
    result = await session.execute(select(User).offset(skip).limit(limit))
    users = result.scalars().all()
    return users


async def get_user_by_email(session: AsyncSession, email: str) -> User:
    result = await session.execute(select(User).filter(User.email == email))
    user = result.scalar_one_or_none()
    return user


async def get_user_by_id(session: AsyncSession, user_id: int) -> User:
    result = await session.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    return user


async def update_user(session: AsyncSession, user_id: int, user_data: dict) -> User:
    user = await get_user_by_id(session, user_id)
    if user:
        for key, value in user_data.items():
            setattr(user, key, value)

        await session.commit()
        await session.refresh(user)
        return user
    return None


async def delete_user(session: AsyncSession, user_id: int) -> bool:
    user = await get_user_by_id(session, user_id)
    if user:
        await session.delete(user)
        await session.commit()
        return True
    return False
