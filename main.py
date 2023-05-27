import asyncio
import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from text import js_is_best

app = FastAPI()

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许的跨域源，可以根据需求进行设置，例如 ["http://localhost", "https://example.com"]
    allow_credentials=True,  # 是否允许发送身份验证信息（cookies、HTTP认证）等
    allow_methods=["*"],  # 允许的HTTP方法，可以根据需求进行设置，例如 ["GET", "POST", "PUT", "DELETE"]
    allow_headers=["*"],  # 允许的自定义请求头，可以根据需求进行设置，例如 ["Content-Type", "Authorization"]
)

file_list = ['docs'] + os.listdir("static")
index = ""
for i in file_list:
    index += f'<a href="/{i}">{i}</a><br>'


@app.get("/")
async def read_root():
    return HTMLResponse(index)


@app.get("/stream_text/{interval}")
async def stream_text(interval: float):
    async def text_gen():
        for chunk in js_is_best:
            await asyncio.sleep(interval)
            yield chunk

    return StreamingResponse(text_gen(), media_type="application/octet-stream")


app.mount("/", StaticFiles(directory="static"), name="static")

if __name__ == '__main__':
    uvicorn.run(app)
