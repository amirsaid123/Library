import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from library.crud import get_book_by_id
from library.database import AsyncSessionLocal
from main import app


# Yields a test client
@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


# Yields a database session
@pytest.fixture
async def db_session():
    async with AsyncSessionLocal() as session:
        yield session


# Creates a custom test user (librarian) and logs in and generates a token
@pytest.fixture
async def token(client):
    REGISTER_URL = "/auth/register/"
    LOGIN_URL = "/auth/login/"
    user_data = {
        "email": "testuser@example.com",
        "password": "testpassword123"
    }

    await client.post(REGISTER_URL, json=user_data)

    response = await client.post(LOGIN_URL, json=user_data)
    assert response.status_code == 200, f"Login failed: {response.json()}"

    token = response.json()["access_token"]
    return token


# Main test for lending and returning books (Business logics)
@pytest.mark.asyncio
class TestAPI:
    async def test_lend_book(self, client, db_session: AsyncSession, token):
        headers = {"Authorization": f"Bearer {token}"}

        book_id = 6
        reader_id = 3

        data = {"book_id": book_id, "reader_id": reader_id}

        book_before = await get_book_by_id(session=db_session, book_id=book_id)
        before_lending = book_before.copy
        print(f"Before lending: book.copy = {before_lending}")

        response = await client.post("/books/lend", json=data, headers=headers)
        print(f"Response: {response.json()}")
        assert response.status_code == 200, f"Got {response.status_code}: {response.json()}"

        await db_session.refresh(book_before)
        book_after = await get_book_by_id(session=db_session, book_id=book_id)
        after_lending = book_after.copy
        print(f"After lending: book.copy = {after_lending}")

        assert before_lending != after_lending

    async def test_return_book(self, client, db_session: AsyncSession, token):
        headers = {"Authorization": f"Bearer {token}"}

        borrow_id = 28
        reader_id = 2

        data = {"borrow_id": borrow_id, "reader_id": reader_id}

        response = await client.post("/books/return", json=data, headers=headers)
        print(f"Response: {response.json()}")
        assert response.status_code == 200, f"Got {response.status_code}: {response.json()}"


class TestBooksAPI:
    async def test_get_books(self, client, token):
        headers = {"Authorization": f"Bearer {token}"}

        response = await client.get("/books/", headers=headers)
        assert response.status_code == 200, f"Got {response.status_code}: {response.json()}"

    async def test_get_book_by_id(self, client, token):
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get("/books/1", headers=headers)
        assert response.status_code == 200, f"Got {response.status_code}: {response.json()}"

    async def test_create_book(self, client, token):
        headers = {"Authorization": f"Bearer {token}"}
        data = {
            "title": "The Lord of The Rings",
            "description": "The best book",
            "author": "J.R.R Tolkien",
            "year": 1965,
            "isbn": "9780321110",
            "copy": 15
        }
        response = await client.post("/books/create", json=data, headers=headers)
        assert response.status_code == 200, f"Got {response.status_code}: {response.json()}"

    async def test_update_patch_book(self, client, token):
        headers = {"Authorization": f"Bearer {token}"}
        data = {
            "copy": 30
        }
        response = await client.patch("/books/patch/16", json=data, headers=headers)
        assert response.status_code == 200, f"Got {response.status_code}: {response.json()}"

    async def test_update_put_book(self, client, token):
        headers = {"Authorization": f"Bearer {token}"}
        data = {
            "copy": 30
        }
        response = await client.put("/books/put/16", json=data, headers=headers)
        assert response.status_code == 200, f"Got {response.status_code}: {response.json()}"

    async def test_delete_book(self, client, token):
        headers = {"Authorization": f"Bearer {token}"}

        response = await client.delete("/books/delete/16", headers=headers)
        assert response.status_code == 200, f"Got {response.status_code}: {response.json()}"
