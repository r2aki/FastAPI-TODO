from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.db import Base

DATABASE_TEST_URL = "sqlite+aiosqlite:///./test.db"

test_engine = create_async_engine(DATABASE_TEST_URL, echo=False)
test_sessionmaker = async_sessionmaker(test_engine, expire_on_commit=False)


async def init_test_db() -> None:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def override_get_db():
    async with test_sessionmaker() as session:
        yield session
