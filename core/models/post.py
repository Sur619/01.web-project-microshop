from core.models import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Text, ForeignKey
from typing import TYPE_CHECKING

from .mixin import UserRelationMixin

if TYPE_CHECKING:
    from .user import User  # Avoid circular import issues


class Post(UserRelationMixin, Base):
    _user_back_populates = "posts"

    title: Mapped[str] = mapped_column(String(100), unique=False)
    body: Mapped[str] = mapped_column(Text, default="", server_default="")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.title}"

    def __repr__(self):
        return str(self)
