import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许的跨域源，可以根据需求进行设置，例如 ["http://localhost", "https://example.com"]
    allow_credentials=True,  # 是否允许发送身份验证信息（cookies、HTTP认证）等
    allow_methods=["*"],  # 允许的HTTP方法，可以根据需求进行设置，例如 ["GET", "POST", "PUT", "DELETE"]
    allow_headers=["*"],  # 允许的自定义请求头，可以根据需求进行设置，例如 ["Content-Type", "Authorization"]
)

# make index
def list_files_in_directory(directory_path):
    file_list = []
    for filename in os.listdir(directory_path):
        filepath = os.path.join(directory_path, filename)
        if os.path.isfile(filepath) and filename.endswith(".html"):
            file_list.append(filename)
    return file_list

file_list = ['docs'] + list_files_in_directory("static")
index = ""
for i in file_list:
    index += f'''\
    <a href="/{i}" target="_blank">{i}</a><br>
    '''


@app.get("/")
async def read_root():
    return HTMLResponse(index)

# router dynamic import
import importlib
router_folder = "./router"
def is_router_file(filename):
    is_file = os.path.isfile(os.path.join(router_folder, filename))
    is_py = filename.endswith('.py')
    return is_file and is_py
file_list = [i for i in os.listdir(router_folder) if is_router_file(i)]
try:
    for filename in file_list:
        router = importlib.import_module("router." + filename.replace('.py', '')).router
        app.include_router(router)
except:
    raise Exception("导入了不干净的东西，请参照模板编写要导入的路由")

app.mount("/", StaticFiles(directory="static"), name="static")

if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, reload=True)
