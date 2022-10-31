from pydantic import BaseModel

from fastapi import APIRouter, Request
from fastapi.responses import Response

import qrflow


router = APIRouter(
    prefix="/api",
    tags=["api"]
)


class Code(BaseModel):
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
def qrcode_create(message: Code):
    stream = qrflow.create_qrcode(message.message, inline=True)
    return Response(content=stream.getvalue(), media_type="application/octet-stream")

