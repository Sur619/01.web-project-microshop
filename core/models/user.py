from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum as SQLAlchemyEnum
from core.models import Base
from core.models.post import Post
from typing import TYPE_CHECKING

from core.models.profile import Profile
from users.schemas import RoleEnum

if TYPE_CHECKING:
    from core.models.post import Post
    from core.models.profile import Profile


class User(Base):
    username: Mapped[str] = mapped_column(String(32), unique=True)

    posts: Mapped[list["Post"]] = relationship(
        back_populates="user",
    )
    profile: Mapped["Profile"] = relationship(back_populates="user")
    role: Mapped["RoleEnum"] = mapped_column(
        SQLAlchemyEnum(RoleEnum),
        server_default=RoleEnum.user,
        default=RoleEnum.user,
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.username!r})"

    def __repr__(self):
        return str(self)
