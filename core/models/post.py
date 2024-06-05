from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import UserRelationMixin


class Post(UserRelationMixin, Base):
    _user_back_populates = "posts"
    title: Mapped[str] = mapped_column(String(100), unique=False)
    body: Mapped[str] = mapped_column(Text, default="", server_default="")

    # Тип тела поста - текст, по дефолту текст пустой.
    # Отличие default от server_default - default используется на стороне алхимии если мы создаем экземпляр,
    # server_default - будет использоваться на стороне бд если мы захотим создать пост внутри бд без алхимии
    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, title={self.title!r})"

    def __repr__(self):
        return str(self)
