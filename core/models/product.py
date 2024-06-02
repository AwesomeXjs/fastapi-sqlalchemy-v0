from sqlalchemy.orm import Mapped

from .base import Base


class Product(Base):
    name: Mapped[str]
    price: Mapped[int]
    description: Mapped[str]
