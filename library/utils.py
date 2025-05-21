import asyncio
import os
from datetime import datetime, timedelta
from typing import Annotated
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from jose import jwt
from passlib.context import CryptContext
from library.database import SessionDep
from library.models import User

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hash the password (run sync function in a thread)
async def hash_password(password: str) -> str:
    return await asyncio.to_thread(pwd_context.hash, password)


# Verify the hashed password
async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return await asyncio.to_thread(pwd_context.verify, plain_password, hashed_password)


load_dotenv()
# Secret key to encode and decode JWT tokens
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120  # Token expiry time


# JWT token creation
async def create_access_token(data: dict,
                              expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return await asyncio.to_thread(jwt.encode, to_encode, SECRET_KEY, ALGORITHM)


security = HTTPBearer()  # just expects "Authorization: Bearer <token>"


async def get_current_user(
        session: SessionDep,
        credentials: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    token = credentials.credentials  # extract token string
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    from library.crud import get_user_by_email

    user = await get_user_by_email(session, email)
    if user is None:
        raise credentials_exception
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]
