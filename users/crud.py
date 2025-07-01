from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from core.models import db_helper
from crud import get_user_by_username
from users.schemas import CreateUser
from auth.auth import utils as auth_utils

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/demo-auth/jwt/login/",
)


def create_user(user_in: CreateUser):
    user = user_in.model_dump()
    return {"message": "User created successfully", "user": user}


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(db_helper.session_dependency),
):
    payload = None
    try:
        payload = auth_utils.decode_jwt(token)
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid token: {e}",
        )
    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=401,
            detail="invalid token payload",
        )
    user = await get_user_by_username(db, username)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )


def get_user_by_token(db: Session, token: str): ...
