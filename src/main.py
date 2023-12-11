import sys
from redis import asyncio as aioredis
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.auth.base_config import fastapi_users, auth_backend
from src.auth.schemas import UserRead, UserCreate

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from src.tasks.router import router as router_tasks

sys.path.append('src')

from pages.operations.router import router as router_operation
from pages.base.router import router as router_pages
from pages.registration.router import router as router_reg
from pages.auth.router import router as router_auth
from pages.chat.router import router as router_chat


app = FastAPI(
    title='Trading App',
)

app.mount("/static", StaticFiles(directory="src/static"), name="static")

origins = [
    "http://127.0.0.1:8000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'PUT', 'PATCH', 'POST', 'DELETE', 'OPTIONS'],
    allow_headers=['Content-Type', 'Set-Cookie', 'Access-Control-Allow-Headers',
                   'Access-Control-Allow-Origin', 'Authorization'],
)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="cache")


app.include_router(router_operation)
app.include_router(router_tasks),
app.include_router(router_pages)
app.include_router(router_reg)
app.include_router(router_auth)
app.include_router(router_chat)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)
