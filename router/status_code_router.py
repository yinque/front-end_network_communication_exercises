from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/status_code")


@router.get("/200")
async def code_200():
    return {"message": "正常"}


@router.get("/401")
async def code_401():
    raise HTTPException(status_code=401, detail="未授权")
