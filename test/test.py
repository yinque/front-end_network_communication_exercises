import asyncio

import httpx

URL = "http://127.0.0.1:8000/stream_text/0.02"


async def async_print():
    async with httpx.AsyncClient() as client:
        async with client.stream('GET', URL) as response:
            async for chunk in response.aiter_bytes():
                chunk = chunk.decode('utf-8')
                print(chunk)


asyncio.run(async_print())