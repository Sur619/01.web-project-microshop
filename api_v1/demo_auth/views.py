import secrets
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials


router = APIRouter(prefix="/demo-auth", tags=["Demo Auth"])

security = HTTPBasic()


@router.get("/basic-auth/")
async def demo_basic_auth(
    credentials: Annotated[
        HTTPBasicCredentials,
        Depends(security),
    ],
):
    return {"credentials": credentials.username, "password": credentials.password}


username_to_password = {
    "admin": "admin",
}


def get_auth_username(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    anauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Basic"},
    )
    correct_password = username_to_password.get(credentials.username)
    if correct_password is None:
        raise anauthed_exc

    if credentials.username not in username_to_password:
        raise anauthed_exc

    if not secrets.compare_digest(
        credentials.password.encode("utf-8"),
        correct_password.encode("utf-8"),
    ):
        raise anauthed_exc

    return credentials.username


@router.get("/basic-auth-username/")
def demo_basic_auth_username(
    auth_username: str = Depends(get_auth_username),
):
    return {"username": auth_username}
