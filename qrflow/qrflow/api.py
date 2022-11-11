import collections
import json
from enum import Enum
from pydantic import BaseModel

from fastapi import APIRouter, Request
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder

# DGC/CST:
import re
import zlib
import base45
import cbor2


import main
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



def decode(ticket):
    b45data = re.sub("HC\d:", "", ticket)
    zlibdata = base45.b45decode(b45data)
    cbordata = zlib.decompress(zlibdata)
    decoded = cbor2.loads(cbordata)
    payload = cbor2.loads(decoded.value[2])
    return payload


@router.post("/qrcode/process")
async def qrcode_process(request: Request):
    try:
        context = await request.json()
    except json.decoder.JSONDecodeError:
        raise main.GenericException("JSON body is expected")
    context = context.get("result", {})
    result = dict()
    if context["text"].startswith("HC"):
        result["dgc"] = decode(context["text"])
    print(result)
    return {
        "context": context,
        "result": result
    }



