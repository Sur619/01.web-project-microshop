from fastapi import Depends, HTTPException
from starlette import status

from api_v1.demo_auth.demo_jwt_auth import (
    get_current_active_user,
    get_current_auth_user,
)
from users.schemas import RoleEnum, UserSchema


def role_required(required_role: RoleEnum):
    def role_checker(current_user: UserSchema = Depends(get_current_active_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=403,
                detail=f"User does not have the required role: {required_role}",
            )
        return current_user

    return role_checker
