from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from core.models import Base
from core.models.post import Post
from typing import TYPE_CHECKING

from core.models.profile import Profile

if TYPE_CHECKING:
    from core.models.post import Post
    from core.models.profile import Profile


class User(Base):
    username: Mapped[str] = mapped_column(String(32), unique=True)

    posts: Mapped[list["Post"]] = relationship(
        back_population="user",
    )
    profile: Mapped["Profile"] = relationship(back_populates="user")
