import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import api


# Create Application:
app = FastAPI(
    version="20221030.1",
    title="qrflow",
    description="QR-Flow Application by Jean Landercy",
    redoc_url=None
)

# Add routers:
app.include_router(api.router)


# Mounts:
app.mount("/static", StaticFiles(directory=os.getenv("APP_STATIC_ROOT", "static")), name="static")
templates = Jinja2Templates(directory=os.getenv("APP_TEMPLATE_ROOT", "templates"))


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/scanner", response_class=HTMLResponse)
async def scanner(request: Request):
    return templates.TemplateResponse("scanner.html", {"request": request})


@app.get("/qrcode", response_class=HTMLResponse)
async def qrcode(request: Request):
    return templates.TemplateResponse("qrcode.html", {"request": request})
