import json
import time

import aiohttp


class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    async def get_model(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS) as resp:
                data = await resp.json()

        return data[0]['id']

    async def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        async with aiohttp.ClientSession() as session:
            url = self.URL + 'key/api/v1/text2image/run'
            async with session.post(url, headers=self.AUTH_HEADERS) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data['uuid']

    async def check_generation(self, request_id, attempts=10, delay=10):
        data = ""
        while attempts > 0:
            async with aiohttp.ClientSession() as session:
                url = self.URL + 'key/api/v1/text2image/status/' + request_id
                async with session.get(url, headers=self.AUTH_HEADERS) as resp:
                    if resp.status == 200:
                        data = resp.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)
