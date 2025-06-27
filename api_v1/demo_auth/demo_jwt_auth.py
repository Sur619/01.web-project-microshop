from users.schemas import UserSchema
from auth.auth import utils as auth_utils

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
