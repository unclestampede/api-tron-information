import asyncio
import warnings
from typing import Any, Generator

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from alembic.command import upgrade
from alembic.config import Config
from app import settings
from app.db.facade import DBFacade
from tests.db_setup import create_test_db, drop_test_db


@pytest_asyncio.fixture
async def db_facade(db: AsyncSession) -> DBFacade:
    return DBFacade(session=db)


@pytest.fixture(scope="session")
def apply_migrations():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    db_url = settings.DB_URL
    db_name = settings.DB_DATABASE
    db_name_test = f"{db_name.replace('-', '_')}_test"

    asyncio.run(drop_test_db(db_url, db_name_test))
    asyncio.run(create_test_db(db_url, db_name_test))

    settings.DB_URL = settings.DB_URL.replace(db_name, db_name_test)
    config = Config("alembic.ini")
    upgrade(config, "head")
    yield
    asyncio.run(drop_test_db(db_url, db_name_test))


@pytest_asyncio.fixture()
async def db(mocker) -> Generator[Any, Any, None]:
    engine = create_async_engine(settings.DB_URL, echo=False)
    async_session = sessionmaker(engine, autoflush=False, class_=AsyncSession, autocommit=False)

    async with engine.connect() as connection:
        transaction = await connection.begin()
        async with async_session(bind=connection) as session:
            mocker.patch("sqlalchemy.orm.sessionmaker.__call__", return_value=session)
            yield session
            await session.close()
        await transaction.rollback()
        await connection.close()


@pytest_asyncio.fixture
def app(apply_migrations, db) -> FastAPI:
    from app.main import app

    return app


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncClient:
    url = f'http://{settings.APP_HOST}:{settings.APP_PORT}'
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url=url, headers={"Content-Type": "application/json"}) as client_:
            yield client_
