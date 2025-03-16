import asyncio
import json

import aiohttp


class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            "X-Key": f"Key {api_key}",
            "X-Secret": f"Secret {secret_key}",
        }

    async def get_model(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.URL + "key/api/v1/models", headers=self.AUTH_HEADERS
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return data[0]["id"]

    async def generate(self, prompt, model, images=1, width=1024, height=1024):
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
            "params", json.dumps(params), content_type="application/json"
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
