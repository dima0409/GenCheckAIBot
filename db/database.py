import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker, AsyncSession

from db.model.images import Base, Image

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL, echo=True)


class Database:
    """Асинхронный менеджер для работы с базой данных изображений.

    Предоставляет методы для:
    - Иницилизации подключения к БД.
    - Создание таблиц.
    - Добавления записей об изображениях.
    - Управления подключениями.

    Args:
        engine: Асинхронный движок SQLAlchemy для подключения к БД.
        async_session: Фабрика асинхронных сесий для работы с БД.
    """

    def __init__(self):
        """Инициализирует подключение к БД и настраивает сессии."""
        self.engine = engine
        self.async_session = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    async def create_db(self):
        """Создает все таблицы в БД на основе модели SQLAlchemy."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def add_image(self, user_id, tag, path):
        """Добавляет запись об изображении в БД.

        Args:
            user_id (_type_): Индентификатор пользователя, загрузившего изображение.
            tag (_type_): Произвольный тег или категория изображения.
            path (_type_): Путь к файлу изображения в хранилище.
        """
        async with self.async_session() as session:
            async with session.begin():
                image = Image(user_id=user_id, tag=tag, path=path)
                session.add(image)

            await session.commit()

    async def close(self):
        await self.engine.dispose()
