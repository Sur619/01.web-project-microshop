from fastapi import APIRouter

from users import crud
from users.schemas import CreateUser

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/")
def create_user(user: CreateUser):
    return crud.create_user(user_in=user)
