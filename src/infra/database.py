import os
from dotenv import load_dotenv
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

if os.path.exists('.env.local'):
    load_dotenv(dotenv_path=".env.local", override=True)
else:
    load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
POSTGRES_DB = os.getenv("POSTGRES_DB")

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()

async def get_db() -> AsyncGenerator:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            raise ConnectionRefusedError("Critical Error in Database", e)
        finally:
            await session.close()
