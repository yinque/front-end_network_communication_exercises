import asyncio
import logging
import unittest

import httpx

URL = "http://127.0.0.1:8000/stream_text/0.02"

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(message)s')


class TestController(unittest.TestCase):
    def setUp(self):
        # 在每个测试方法之前运行的设置代码
        pass

    def tearDown(self):
        # 在每个测试方法之后运行的清理代码
        pass

    def test1_print(self):
        """
        普通请求打印
        :return:
        """
        response = httpx.get(URL)
        print(response)
        print(response.text)

    def test2_stream_print(self):
        """
        生成器打印，事实证明也是流式读取的，而不是解析完才打印
        :return:
        """
        with httpx.stream('GET', URL) as response:
            for chunk in response.iter_bytes():
                chunk = chunk.decode('utf-8')
                print(chunk)

    def test3_async_print(self):
        """
        异步流式打印
        :return:
        """

        async def async_print():
            async with httpx.AsyncClient() as client:
                async with client.stream('GET', URL) as response:
                    async for chunk in response.aiter_bytes():
                        chunk = chunk.decode('utf-8')
                        print(chunk)

        asyncio.run(async_print())


if __name__ == '__main__':
    unittest.main()
