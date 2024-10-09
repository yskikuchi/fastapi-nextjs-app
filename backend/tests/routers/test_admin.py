import pytest
import app.models.admin as admin_model


@pytest.mark.asyncio
async def test_create_admin(async_client):
    response = await async_client.post(
        "/admin",
        json={"name": "admin", "email": "admin@example.com", "password": "password"},
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_admin_invalid(async_client, async_session_fixture):
    name = "admin"
    email = "admin@example.com"
    password = "password"
    admin = admin_model.Admin(name=name, email=email, password=password)
    async_session_fixture.add(admin)
    await async_session_fixture.commit()

    response = await async_client.post(
        "/admin",
        json={"name": name, "email": email, "password": password},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "このメールアドレスは既に登録されています"}
