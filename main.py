from fastapi import FastAPI
from library.database import engine
from library.models import Base
from library.endpoints.auth import router as user_router
from library.endpoints.books_crud import router as books_router
from library.endpoints.readers_crud import router as readers_router
from library.endpoints.lend_or_return import router as borrow_router

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(user_router)
app.include_router(books_router)
app.include_router(readers_router)
app.include_router(borrow_router)
