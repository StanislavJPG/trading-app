from httpx import AsyncClient


async def test_add_specific_operations(ac: AsyncClient):
    response = await ac.post('/operations', json={
        "id": 8,
        "quantity": "12",
        "figi": "string_CODE",
        "instrument_type": "bond",
        "date": "2023-12-01T14:33:56.52",
        "type": "Виплата купонів"
    })

    assert response.status_code == 200


async def test_get_specific_operations(ac: AsyncClient):
    response = await ac.get('/operations', params={
        'operation_type': 'Виплата купонів'
    })

    assert response.status_code == 200
    assert response.json()['status'] == 'success'

