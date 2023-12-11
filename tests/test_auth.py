from sqlalchemy import insert
from conftest import client, async_session_maker
from src.auth.models import Role


async def test_add_role():
    async with async_session_maker() as session:
        stmt = insert(Role).values(id=10, name='admin', permissions=None)
        await session.execute(stmt)
        await session.commit()


def test_register():
    response = client.post('/auth/register', json={
        "email": "johny@mail.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "string",
        "role_id": 2
    })

    assert response.status_code == 201
