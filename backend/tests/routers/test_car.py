import pytest
from tests.conftest import create_admin_and_login, create_car
from sqlalchemy.sql import select
import app.models.car as car_model


@pytest.mark.asyncio
async def test_get_car(async_client):
    access_token = await create_admin_and_login(async_client)
    response = await async_client.post(
        "/cars",
        headers={"Authorization": "Bearer {token}".format(token=access_token)},
        json={
            "name": "車両A",
            "capacity": 6,
            "car_number": "品川 あ 12-34",
            "price_for_initial_twelve_hours": 10000,
            "price_per_additional_six_hours": 5000,
        },
    )
    assert response.status_code == 200
    response_obj = response.json()

    response = await async_client.get("/cars")
    assert response.status_code == 200
    response_obj = response.json()
    assert len(response_obj) == 1
    assert response_obj[0]["name"] == "車両A"
    assert response_obj[0]["capacity"] == 6


@pytest.mark.asyncio
async def test_update_car(async_client, async_session_fixture):
    access_token = await create_admin_and_login(async_client)

    await create_car(async_session_fixture)
    result = await async_session_fixture.execute(select(car_model.Car.id))
    car_id = result.scalars().first()
    response = await async_client.patch(
        f"/cars/{car_id}",
        headers={"Authorization": "Bearer {token}".format(token=access_token)},
        json={
            "name": "変更された名前",
            "capacity": 6,
            "car_number": "品川 あ 12-34",
            "price_for_initial_twelve_hours": 10000,
            "price_per_additional_six_hours": 5000,
        },
    )

    assert response.status_code == 200

    result = await async_session_fixture.execute(
        select(car_model.Car).filter_by(id=car_id)
    )
    car = result.scalars().first()
    assert car.name == "変更された名前"
