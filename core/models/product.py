from sqlalchemy.orm import Mapped, relationship
from typing import TYPE_CHECKING

from .base import Base
from .order_product_association import order_product_association_table


if TYPE_CHECKING:
    from .order import Order


class Product(Base):
    name: Mapped[str]
    price: Mapped[int]
    description: Mapped[str]

    orders: Mapped[list["Order"]] = relationship(
        secondary=order_product_association_table, back_populates="products"
    )  # back_populates указывает откуда можно ссылаться на посты
