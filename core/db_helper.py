from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
    AsyncSession,
)

from core.config import settings


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = True):
        self.engine = create_async_engine(url=url, echo=echo)
        self.section_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.section_factory, scopefunc=current_task
        )
        return session

    async def session_dependency(self) -> AsyncSession:
        async with self.section_factory() as sess:
            yield sess
            await sess.close()

    async def scoped_session_dependency(self) -> AsyncSession:
        session = self.get_scoped_session()
        yield session
        await session.close()


db_helper = DatabaseHelper(url=settings.db_url, echo=settings.db_echo)
