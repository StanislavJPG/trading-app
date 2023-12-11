from typing import Optional
from fastapi_users import schemas
from pydantic import Field, EmailStr


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    username: str
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):
    username: str = Field(min_length=1)
    email: str = EmailStr
    password: str = Field(min_length=5)
    role_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
