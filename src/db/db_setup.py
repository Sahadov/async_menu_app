from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

# SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
# SQLALCHEMY_DATABASE_URL = 'postgresql+asyncpg://postgres:159753@localhost:5432/restaurant'
SQLALCHEMY_DATABASE_URL = 'postgresql+asyncpg://postgres:postgres@db:2121/resto'


Base = declarative_base()


engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
