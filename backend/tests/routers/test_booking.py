import pytest
import uuid
from sqlalchemy import select
from datetime import datetime, timedelta
from tests.conftest import create_car, create_booking, create_user
import app.models.car as car_model
import app.models.user as user_model


@pytest.mark.asyncio
async def test_create_booking(async_client, async_session_fixture):
    await create_car(async_session_fixture)
    result = await async_session_fixture.execute(select(car_model.Car.id))
    car_id = result.scalars().first()

    response = await async_client.post(
        "/booking",
        json={
            "user": {"name": "テストユーザー", "email": "test@sample.com"},
            "car_id": str(car_id),
            "start_time": (datetime.now() + timedelta(days=2)).strftime(
                "%Y-%m-%dT%H:%M:%S"
            ),
            "end_time": (datetime.now() + timedelta(days=4)).strftime(
                "%Y-%m-%dT%H:%M:%S"
            ),
            "amount": 10000,
        },
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_booking_invalid(async_client, async_session_fixture):
    await create_car(async_session_fixture)
    result = await async_session_fixture.execute(select(car_model.Car.id))
    car_id = result.scalars().first()

    # 過去の日付を指定
    past_time = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%S")
    response = await async_client.post(
        "/booking",
        json={
            "user": {"name": "テストユーザー", "email": "test@sample.com"},
            "car_id": str(car_id),
            "start_time": past_time,
            "end_time": (datetime.now() + timedelta(days=4)).strftime(
                "%Y-%m-%dT%H:%M:%S"
            ),
            "amount": 10000,
        },
    )

    assert response.status_code == 422
    response_json = response.json()
    assert (
        response_json["detail"][0]["msg"] == "Value error, 未来の日付を指定してください"
    )

    # 利用終了時間が利用開始時間より前
    start_time = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%S")
    end_time = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")
    response = await async_client.post(
        "/booking",
        json={
            "user": {"name": "テストユーザー", "email": "test@sample.com"},
            "car_id": str(car_id),
            "start_time": start_time,
            "end_time": end_time,
            "amount": 10000,
        },
    )
    assert response.status_code == 422
    response_json = response.json()
    assert (
        response_json["detail"][0]["msg"]
        == "Value error, 利用終了時間は利用開始時間より後にしてください"
    )

    # 予約時間が重複
    await create_user(async_session_fixture)
    result = await async_session_fixture.execute(select(user_model.User.id))
    user_id = result.scalars().first()
    await create_booking(async_session_fixture, car_id, user_id)
    start_time = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%S")
    end_time = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:%S")
    response = await async_client.post(
        "/booking",
        json={
            "user": {"name": "テストユーザー", "email": "test@sample.com"},
            "car_id": str(car_id),
            "start_time": start_time,
            "end_time": end_time,
            "amount": 10000,
        },
    )
    assert response.status_code == 422
    response_json = response.json()
    assert response_json["detail"] == "選択した時間帯で既に予約が入っています"
