from pydantic import BaseModel

from fastapi import APIRouter, Request
from fastapi.responses import Response
from fastapi.encoders import jsonable_encoder

import qrflow


router = APIRouter(
    prefix="/api",
    tags=["api"]
)


class Message(BaseModel):
    message: str


@router.post(
    "/qrcode/create/",
    responses={
        200: {
            "content": {
                "image/png": {},
                "application/octet-stream": {},
            }
        }
    },
    response_class=Response,
)
async def qrcode_create(message: Message):
    stream = qrflow.create_qrcode(message.message, inline=True)
    return Response(content=stream.getvalue(), media_type="application/octet-stream")


@router.post("/qrcode/process/")
async def qrcode_process(request: Request): #message: Message):
    message = await request.form()
    return jsonable_encoder(message)
