import pytest


@pytest.mark.asyncio
async def test_get_car(async_client):
    access_token = await create_admin_and_login(async_client)
    response = await async_client.post(
        "/cars",
        headers={"Authorization": "Bearer {token}".format(token=access_token)},
        json={"name": "車両A", "capacity": 6, "car_number": "品川 あ 12-34"},
    )
    assert response.status_code == 200
    response_obj = response.json()

    response = await async_client.get("/cars")
    assert response.status_code == 200
    response_obj = response.json()
    assert len(response_obj) == 1
    assert response_obj[0]["name"] == "車両A"
    assert response_obj[0]["capacity"] == 6


async def create_admin_and_login(async_client):
    name = "admin"
    email = "admin@example.com"
    password = "password"
    await async_client.post(
        "/admin",
        json={"name": name, "email": email, "password": password},
    )
    login_response = await async_client.post(
        "/admin/login", data={"username": email, "password": password}
    )
    print("ログインレスポンス", login_response)
    return login_response.json()["access_token"]
