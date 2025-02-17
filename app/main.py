from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app import settings
from app.routers.health import router as health_router
from app.routers.tron import router as tron_router

tags_metadata = [
    {"name": "tron", "description": "Информация о TRON кошельках"},
    {"name": "health", "description": "Состояние сервиса"},
]

title = 'API TRON information'
description = 'API TRON information'

app = FastAPI(debug=settings.DEBUG, openapi_tags=tags_metadata, title=title, description=description)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(tron_router, tags=['tron'])
app.include_router(health_router, tags=['health'])
