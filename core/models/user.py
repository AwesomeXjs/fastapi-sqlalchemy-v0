from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from .base import Base


class User(Base):
    username: Mapped[str] = mapped_column(String(25), unique=True)
