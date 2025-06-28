from jwt.exceptions import InvalidTokenError
from users.schemas import UserSchema
from auth.auth import utils as auth_utils
from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    status,
)
from pydantic import BaseModel
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)

# http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/demo-auth/jwt/login/",
)
router = APIRouter(prefix="/jwt", tags=["JWT"])


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


john = UserSchema(
    username="john",
    password=auth_utils.hash_password("qwerty"),
    email="john@example.com",
)

admin = UserSchema(
    username="admin",
    password=auth_utils.hash_password("password"),
    email="admin@example.com",
)
users_db: dict[str, UserSchema] = {
    john.username: john,
    admin.username: admin,
}


def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password"
    )
    if not (user := users_db.get(username)):
        raise unauthed_exc

    if not auth_utils.validate_password(
        password=password,
        hashed_password=user.password,
    ):
        raise unauthed_exc
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not active",
        )
    return user


@router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(
    user: UserSchema = Depends(validate_auth_user),
):
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    token = auth_utils.encode_jwt(
        payload=jwt_payload,
    )
    return TokenInfo(
        access_token=token,
        token_type="bearer",
    )


def get_current_token_payload(
    # credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    token: str = Depends(oauth2_scheme),
) -> UserSchema:
    # token = credentials.credentials
    try:
        payload = auth_utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token invalid: {e}",
        )
    return payload


def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
) -> UserSchema:
    username: str | None = payload.get("sub")
    if user := users_db.get(username):
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalid (user not found)",
        )


def get_current_active_user(
    user: UserSchema = Depends(get_current_auth_user),
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User is not active",
    )


@router.get("/users/me/")
def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: UserSchema = Depends(
        get_current_active_user,
    ),
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "email": user.email,
        "active": user.active,
        "last_login_at": iat,
    }
