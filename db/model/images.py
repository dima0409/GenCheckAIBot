from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Image(Base):
    """Модель SQLAlchemy для хранения информации об изображениях.

    Соотвествует таблице 'images' в БД и содержит:
    - ID записи.
    - ID пользователя.
    - Тег/категорию изображения.
    - Путь к изображению.

    Args:
        id (int): Первичный ключ, автоинкрементируемый.
        user_id (int): Telegram ID пользователя.
        tag (str): Категория изображения (AI/Real).
        path (str): Путь к изображению.
    """

    __tablename__ = "images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    tag = Column(String)
    path = Column(String)
