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
    message: str


class Payload(BaseModel):
    message: str
    payload: str


@router.post("/qrcode/create")
async def qrcode_create(message: Message):
    stream = qrflow.render_qrcode(message.message, inline=True)
    return {
        "message": message.message,
        "payload": stream.getvalue().decode()
    }


@router.post("/qrcode/process")
async def qrcode_process(message: Message):
    return message
