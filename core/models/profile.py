from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base
from typing import TYPE_CHECKING

from .mixin import UserRelationMixin

if TYPE_CHECKING:
    from .user import User  # Avoid circular import issues


class Profile(UserRelationMixin, Base):
    _user_id_unique: bool = True
    _user_back_populates: str | None = "profile"

    first_name: Mapped[str | None] = mapped_column(String(40))
    last_name: Mapped[str | None] = mapped_column(String(40))
    bio: Mapped[str | None] = mapped_column(String(200))

    user_id: Mapped[int] = mapped_column(foreignkey="users.id", unique=True)
