# 路由模板
from fastapi import APIRouter

router = APIRouter()


@router.get("/template_path")
async def template_path():
    return "Hello Template"
