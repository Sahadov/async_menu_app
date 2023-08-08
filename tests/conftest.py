import asyncio
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import MetaData

from src.db.db_setup import get_async_session
from src.config import DB_HOST, DB_PORT, DB_USER, DB_NAME, DB_PASS
#from src import metadata
#from src.config import (DB_HOST_TEST, DB_NAME_TEST, DB_PASS_TEST, DB_PORT_TEST,
#                        DB_USER_TEST)
from src.main import app
from src.db.models import menu, submenu, dish



#DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine_test = create_async_engine(SQLALCHEMY_DATABASE_URL, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)






@pytest.fixture(scope="session")
async def prepare_engine():
    async with engine_test.begin() as conn:
        await conn.run_sync(menu.Base.metadata.create_all(bind=engine_test))
        await conn.run_sync(submenu.Base.metadata.create_all(bind=engine_test))
        await conn.run_sync(dish.Base.metadata.create_all(bind=engine_test))
    yield
    pass
    




# SETUP
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

client = TestClient(app)

@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
