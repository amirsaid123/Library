from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from library.config import DBConfig
from library.models import Reader, Book
import asyncio
import random
from faker import Faker

DATABASE_URL = DBConfig.DB_URL

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

fake = Faker()

async def seed_data():
    async with AsyncSessionLocal() as session:
        readers = [
            Reader(full_name=fake.name(), email=fake.unique.email())
            for _ in range(10)
        ]

        books = [
            Book(
                title=fake.sentence(nb_words=3),
                description=fake.text(max_nb_chars=200),
                author=fake.name(),
                year=random.randint(1900, 2023),
                isbn=fake.unique.isbn13(),
                copy=random.randint(1, 5)
            )
            for _ in range(10)
        ]

        session.add_all(readers + books)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(seed_data())
