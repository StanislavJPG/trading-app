import sys
from redis import asyncio as aioredis
from fastapi import FastAPI, Depends, HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import fastapi_users, auth_backend
from src.auth.models import Role
from src.auth.schemas import UserRead, UserCreate

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from src.config import REDIS_HOST, REDIS_PORT
from src.database import get_async_session, async_session_maker
from src.tasks.router import router as router_tasks

sys.path.append('src')

from operations.router import router as router_operations
from pages.operations.router import router as router_operation_page
from pages.base.router import router as router_pages
from pages.registration.router import router as router_reg_page
from pages.auth.router import router as router_auth_page
from pages.chat.router import router as router_chat_page


app = FastAPI(
    title='Trading App',
)

app.mount("/static", StaticFiles(directory="src/static"), name="static")

origins = [
    "http://127.0.0.1:7077"
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
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf-8", decode_response=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")


async def create_role_tables(session: AsyncSession = Depends(get_async_session)):
    try:
        user_roles = ({'id': 1, 'name': 'user', 'permissions': None},
                      {'id': 2, 'name': 'admin', 'permissions': None})
        for user_role in user_roles:
            stmt = insert(Role).values(**user_role)
            await session.execute(stmt)
        await session.commit()
    except IntegrityError:
        return 'Roles already exists'


@app.on_event("startup")
async def startup_roles():
    async with async_session_maker() as session:
        await create_role_tables(session)


app.include_router(router_operation_page)
app.include_router(router_tasks)
app.include_router(router_pages)
app.include_router(router_reg_page)
app.include_router(router_auth_page)
app.include_router(router_chat_page)
app.include_router(router_operations)


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
