import logging

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from httfe.core.config import settings
from httfe.core.log import setup_logging
from httfe.routes.chat import router as chat_router
from httfe.routes.text import router as text_router
from httfe.routes.video import router as video_router

load_dotenv("../.env")

setup_logging()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(video_router, prefix="/video", tags="video")
app.include_router(chat_router, prefix="/chat", tags="chat")
app.include_router(text_router, prefix="/text", tags="text")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":

    logging.debug("config %s", settings.model_dump())
    uvicorn.run(app, host=settings.server.host, port=settings.server.port)
