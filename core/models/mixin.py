from sqlalchemy.orm import declared_attr, mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User  # Avoid circular import issues


class UserRelationMixin:
    _user_id_unique: bool = False
    _user_back_populates: str | None = None
    _user_id_nullable: bool = False

    @declared_attr
    def user_id(self) -> Mapped[int]:
        return mapped_column(
            ForeignKey("users.id"),
            unique=self._user_id_unique,
            nullable=self._user_id_nullable,
        )

    @declared_attr
    def user(self) -> Mapped["User"]:
        return relationship(
            back_populates=self._user_back_populates,
        )
