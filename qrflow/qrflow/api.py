from enum import Enum
from pydantic import BaseModel

from fastapi import APIRouter, Request
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder

import qrflow


router = APIRouter(
    prefix="/api",
    tags=["api"]
)


class Message(BaseModel):
    message: str = "Sample Payload"


class Payload(BaseModel):
    message: str
    payload: str


@router.post("/qrcode/create")
async def qrcode_create(request: Message):
    stream = qrflow.render_qrcode(request.message, inline=True)
    return {
        "message": request.message,
        "payload": stream.getvalue().decode()
    }


@router.post("/qrcode/process")
async def qrcode_process(request: Request):
    context = (await request.json()).get("result", {})
    return {
        "context": context,
        "result": {}
    }
