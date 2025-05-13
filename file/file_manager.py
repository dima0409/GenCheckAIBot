import os
import shutil


class FileManager:
    """Класс для управления изображений с организацией по папкам.

    Позволяет созранять изображение в файловую систему:
    'base_folder/ID(Tg id пользователя)/tag/image_name.png'.

    Args:
        base_folder (str): основная папка для хранения изображений.
          По умолчанию 'images'.
    """

    def __init__(self, base_folder="images"):
        """Иницилизирует FileManager, создает базовую папку если она отстутвует.

        Args:
            base_folder (str, optional): Главная папка.
              Defaults to "images".
        """

        self.base_folder = base_folder
        if not os.path.exists(base_folder):
            os.makedirs(self.base_folder)

    async def save_image(self, id, image_name, tag):
        """Сохраняет изображение в соотвествующую папку.

        Перемешаеи изображение из исходного расположения в:
        'base_folder/ID(Tg id пользователя)/tag/image_name.png'

        Args:
            id (Integer): Уникальный id.
                        Станет именем подпапки первого уровня.
            image_name (str): Имя файла изображения.
            tag (str): Категория изображения.
                        Станет именем подпапки второго уровня.
        """
        if not os.path.exists(f"images\\{id}"):
            os.mkdir(f"images\\{id}")

        if not os.path.exists(f"images\\{id}\\{tag}"):
            os.mkdir(f"images\\{id}\\{tag}")

        src = str(os.path.join(image_name))
        dest = str(os.path.join(self.base_folder, id, tag))

        os.makedirs(os.path.dirname(dest), exist_ok=True)
        dest = str(os.path.join(self.base_folder, id, tag, image_name))

        shutil.copy(src, dest)
        os.remove(src)
