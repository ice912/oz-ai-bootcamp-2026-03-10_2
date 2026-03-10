from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

DATABASE_URL = "sqlite+aiosqlite:///./db.sqlite"

engine = create_async_engine(DATABASE_URL)

AsyncSessionFactory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

async def get_session():
    session = AsynSessionFactory()
    try:
        yield session
    finally:
        await session.close()

