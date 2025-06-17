from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from core.models import Base
from core.models.post import Post
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models.post import Post  # Avoid circular import issues


class User(Base):
    username: Mapped[str] = mapped_column(String(32), unique=True)

    posts: Mapped[list["Post"]] = relationship(
        back_population="user",
    )
