from fastapi import APIRouter, HTTPException
from library.crud import get_user_by_email, create_user
from library.database import SessionDep
from library.schemas import UserCreate
from library.utils import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register/")
async def register_user(session: SessionDep, user_data: UserCreate):
    user = await get_user_by_email(session, str(user_data.email))
    if user:
        raise HTTPException(
            status_code=400, detail="User with this email already exists"
        )

    new_user = await create_user(session, user_data.model_dump())
    return {"message": "User created successfully", "user": {"email": new_user.email, "id": new_user.id}}


@router.post("/login/")
async def login_user(session: SessionDep, user_data: UserCreate):
    user = await get_user_by_email(session, str(user_data.email))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not await verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    access_token = await create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
