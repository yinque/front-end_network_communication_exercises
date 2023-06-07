import asyncio


async def event_generator():
    for i in range(1, 6):
        yield f"data: Event {i}\n\n"
        await asyncio.sleep(0.2)
    yield "data: [DONE]"


async def main():
    e = event_generator()
    async for event in e:
        print(event)


# 使用asyncio.run来运行异步函数
asyncio.run(main())
