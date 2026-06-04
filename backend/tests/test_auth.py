import pytest
from models.user import User
from core.security import hash_password

@pytest.mark.asyncio
async def test_login_success(client, db_session):
    # Setup: Create a test user
    hashed = hash_password("testpassword")
    user = User(
        full_name="Test User",
        email="test@almoratab.ma",
        hashed_password=hashed,
        role="user"
    )
    db_session.add(user)
    await db_session.commit()

    # Action: Attempt login
    response = await client.post("/auth/login", json={
        "email": "test@almoratab.ma",
        "password": "testpassword"
    })

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "test@almoratab.ma"
    assert data["user"]["role"] == "user"

@pytest.mark.asyncio
async def test_login_invalid_credentials(client, db_session):
    response = await client.post("/auth/login", json={
        "email": "wrong@almoratab.ma",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
