import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from sqlalchemy.ext.asyncio.session import AsyncSession

from db.model.images import Base
from db.model.images import Image

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL, echo=True)


class Database:
    def __init__(self):
        self.engine = engine
        self.async_session = async_sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )

    async def create_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def add_image(self, user_id, tag, path):
        async with self.async_session() as session:
            async with session.begin():
                image = Image(user_id=user_id, tag=tag, path=path)
                session.add(image)
            await session.commit()

    async def close(self):
        await self.engine.dispose()
