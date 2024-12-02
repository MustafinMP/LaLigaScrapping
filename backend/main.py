import asyncio
import time
from threading import Thread

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

import db_session
from routers.matches import router as match_router
from routers.goals import router as goals_router
from routers.players import router as player_router
from routers.pages import router as pages_router
from services import scrapper

app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount('/static', StaticFiles(directory='../frontend/static', html=False))

app.include_router(match_router, prefix='/api')
app.include_router(goals_router, prefix='/api')
app.include_router(player_router, prefix='/api')
app.include_router(pages_router, prefix='')


if __name__ == '__main__':
    db_session.init_app()
    scrap = Thread(target=asyncio.run, args=[scrapper.Scrapper.scrap_all_gameweeks()], daemon=True)
    scrap.start()
    uvicorn.run('main:app')
