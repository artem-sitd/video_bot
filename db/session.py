from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from contextlib import asynccontextmanager
from config import settings

engine = create_async_engine(
    settings.DATABASE_URL_async,
    echo=False,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


@asynccontextmanager
async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session


# синхронная сессия для load_json.py первиное заполнение тестовыми данными
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

sync_engine = create_engine(
    settings.DATABASE_URL_sync,
    echo=False,
)

SessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False,
    class_=Session,
)


def get_sync_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
