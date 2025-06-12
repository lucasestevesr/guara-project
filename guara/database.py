from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from guara.settings import Settings

settings = Settings()
engine = create_async_engine(settings.DATABASE_URL)


def get_session():  # pragma: no cover
    with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
