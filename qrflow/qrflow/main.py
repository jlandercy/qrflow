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
    description="QR-Flow Application by Jean Landercy"
)

app.mount("/static", StaticFiles(directory=os.getenv("APP_STATIC_ROOT", "static")), name="static")
templates = Jinja2Templates(directory=os.getenv("APP_TEMPLATE_ROOT", "templates"))


# @app.get("/")
# async def root():
#     return {
#         "name": app.title,
#         "version": app.version,
#         "documentation": "/docs/"
#     }

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/scanner/", response_class=HTMLResponse)
async def scanner(request: Request):
    return templates.TemplateResponse("scanner.html", {"request": request})


@app.get("/qrcode/", response_class=HTMLResponse)
async def qrcode(request: Request):
    return templates.TemplateResponse("qrcode.html", {"request": request})


@app.get(
    "/qrcode/create/",
    responses={
        200: {
            "content": {"image/png": {}}
        }
    },
    response_class=Response,
)
async def qrcode_create(request: Request, message: str = "Hello world!"):
    stream = io.BytesIO()
    image = qrflow.create_qrcode(message)
    image.save(stream)
    return Response(content=stream.getvalue(), media_type="image/png")
