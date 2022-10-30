import io
import os

from fastapi import FastAPI, Request
from fastapi.responses import Response, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import qrflow


app = FastAPI(
    version="20221030.1",
    title="qrflow",
    description="QR Flow Application by jlandercy"
)

app.mount("/static", StaticFiles(directory=os.getenv("APP_STATIC_ROOT", "static")), name="static")
templates = Jinja2Templates(directory=os.getenv("APP_TEMPLATE_ROOT", "templates"))


@app.get("/")
async def root():
    return {
        "name": app.title,
        "version": app.version,
        "documentation": "/docs"
    }


@app.get("/scanner/", response_class=HTMLResponse)
async def scanner(request: Request):
    return templates.TemplateResponse("scanner.html", {"request": request})


@app.get(
    "/qrcode/generate/",
    responses={
        200: {
            "content": {"image/png": {}}
        }
    },
    response_class=Response,
)
async def generate_qrcode(request: Request, message: str = "Hello world!"):
    stream = io.BytesIO()
    image = qrflow.generate_qrcode(message)
    image.save(stream)
    return Response(content=stream.getvalue(), media_type="image/png")


@app.get("/scanner/decode/")
async def scanner_decode():
    return {}
