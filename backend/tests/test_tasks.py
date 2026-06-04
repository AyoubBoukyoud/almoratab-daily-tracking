import pytest
from datetime import date, timedelta
from models.user import User
from models.sprint import Sprint
from models.task_submission import TaskSubmission
from core.security import hash_password

@pytest.mark.asyncio
async def test_submit_tasks_outside_sprint(client, db_session):
    # Setup user
    hashed = hash_password("pass123")
    user = User(
        full_name="Fatima A",
        email="fatima@almoratab.ma",
        hashed_password=hashed,
        role="user"
    )
    db_session.add(user)
    await db_session.commit()

    # Login to get token
    login_res = await client.post("/auth/login", json={
        "email": "fatima@almoratab.ma",
        "password": "pass123"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Action: Submit without active sprint in database
    response = await client.post("/tasks/submit", headers=headers, json={
        "task1_done": True,
        "task2_done": True,
        "task3_done": False
    })
    
    # Assert (no sprint covers today -> should return 400 Bad Request)
    assert response.status_code == 400
    assert "No active sprint found" in response.json()["detail"]

@pytest.mark.asyncio
async def test_submit_tasks_success(client, db_session):
    # Setup user & sprint
    hashed = hash_password("pass123")
    user = User(
        full_name="Fatima A",
        email="fatima@almoratab.ma",
        hashed_password=hashed,
        role="user"
    )
    db_session.add(user)
    
    today = date.today()
    # Force Sunday check bypass by mocking or setting start/end date around today
    # If today is Sunday, this test will fail because of the Sunday lock.
    # So we write conditional assertions or mock date.today
    sprint = Sprint(
        sprint_number=1,
        start_date=today - timedelta(days=2),
        end_date=today + timedelta(days=5),
        is_active=True
    )
    db_session.add(sprint)
    await db_session.commit()

    login_res = await client.post("/auth/login", json={
        "email": "fatima@almoratab.ma",
        "password": "pass123"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.post("/tasks/submit", headers=headers, json={
        "task1_done": True,
        "task2_done": True,
        "task3_done": False
    })

    # Assert based on day of week
    if today.weekday() == 6: # Sunday
        assert response.status_code == 403
        assert "Rest day" in response.json()["detail"]
    else:
        assert response.status_code == 200
        data = response.json()
        assert data["points_earned"] == 4
        assert data["task1_done"] is True
        assert data["task2_done"] is True
        assert data["task3_done"] is False
