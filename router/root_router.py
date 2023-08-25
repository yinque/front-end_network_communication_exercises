# 根路由，存放杂项资源
import asyncio

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from resource.text import python_is_best

router = APIRouter()


@router.get("/stream_text/{interval}")
async def stream_text(interval: float):
    async def text_gen():
        for chunk in python_is_best:
            await asyncio.sleep(interval)
            yield chunk

    return StreamingResponse(text_gen(), media_type="application/octet-stream")


@router.get("/events")
async def get_events():
    async def event_generator():
        for i in range(1, 6):
            yield f"data: Event {i}\n\n"  # 尤其注意，事件末尾要加上\n\n，否则EventSource不识别
            await asyncio.sleep(0.2)
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


