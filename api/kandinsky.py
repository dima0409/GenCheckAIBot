import asyncio
import json

import aiohttp


class Text2ImageAPI:
    """Асинхронный клиент для работы с API генерации изображений по тексту.

    Предоставляет методы для:
    - Получения доступных моделей
    - Запуска генерации изображений
    - Проверки статуса генерации

    Attributes:
        URL (str): Базовый URL API
        AUTH_HEADERS (dict): Заголовки авторизации
    """

    def __init__(self, url, api_key, secret_key):
        """Инициализация API клиента.

        Args:
            url: Базовый URL API сервиса
            api_key: Публичный ключ API
            secret_key: Секретный ключ API
        """
        self.URL = url
        self.AUTH_HEADERS = {
            "X-Key": f"Key {api_key}",
            "X-Secret": f"Secret {secret_key}",
        }

    async def get_model(self):
        """Получает ID первой доступной модели для генерации.

        Returns:
            ID модели в виде строки

        Raises:
            aiohttp.ClientError: В случае ошибки HTTP запроса
            ValueError: Если список моделей пуст
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.URL + "key/api/v1/models",
                headers=self.AUTH_HEADERS,
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return data[0]["id"]

    async def generate(self, prompt, model, images=1, width=1024, height=1024):
        """Запускает процесс генерации изображения на основе текстового запроса.

        Args:
            prompt: Текстовый запрос для генерации изображения(промт).
            model: Модель Kandinsky
            images (optional): Количество генерируемых изображений. Возможно 1
            width (optional): Ширина генерируемого изображения в пикселях. По умолчанию 1024.
            height (optional): Высота генерируемого изображения в пикселях. По умолчанию 1024.

        Returns:
            ID запроса на генерацию (uuid).

        Raises:
            aiohttp.ClientError: В случае ошибки HTTP запроса.
        """
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {"query": f"{prompt}"},
        }

        data = aiohttp.FormData()
        data.add_field("model_id", str(model))
        data.add_field(
            "params",
            json.dumps(params),
            content_type="application/json",
        )

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.URL + "key/api/v1/text2image/run",
                headers=self.AUTH_HEADERS,
                data=data,
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return data["uuid"]

    async def check_generation(self, request_id, attempts=10, delay=10):
        """Проверяет статус запроса на генерацию изображения.

        Args:
            request_id: ID запроса, полученный от метода `generate`.
            attempts (optional): Максимальное количество попыток проверки статуса. По умолчанию 10.
            delay (optional): Задержка в секундах между попытками проверки. По умолчанию 10.

        Returns:
            Список URL сгенерированных изображений, если статус "DONE".
            None, если по истечении `attempts` статус не "DONE".

        Raises:
            aiohttp.ClientError: В случае ошибки HTTP запроса.
        """
        while attempts > 0:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.URL + "key/api/v1/text2image/status/" + request_id,
                    headers=self.AUTH_HEADERS,
                ) as response:
                    response.raise_for_status()
                    data = await response.json()
                    if data["status"] == "DONE":
                        return data["images"]

            attempts -= 1
            await asyncio.sleep(delay)

        return None
