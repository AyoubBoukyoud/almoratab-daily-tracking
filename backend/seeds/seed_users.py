import asyncio
import random
import sys
import os
from datetime import date, timedelta
from sqlalchemy import select

# Add parent dir to path
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

from core.database import AsyncSessionLocal, engine
from core.security import hash_password
from models.user import User
from models.sprint import Sprint
from models.live_session import LiveSession

# Cohort users list
SEED_USERS = [
    {"full_name": "Bouchra Salil", "email": "bouchra@almoratab.ma"},
    {"full_name": "Fairouz Massaly", "email": "fairouz@almoratab.ma"},
    {"full_name": "Fatima Amgour", "email": "fatima.a@almoratab.ma"},
    {"full_name": "Fatima Zohra Belbout", "email": "fatima.z@almoratab.ma"},
    {"full_name": "Karima Faouzi", "email": "karima@almoratab.ma"},
    {"full_name": "Meriem Makoudi", "email": "meriem@almoratab.ma"},
    {"full_name": "Nadia Bouhafoura", "email": "nadia@almoratab.ma"},
]

async def seed_data():
    async with AsyncSessionLocal() as session:
        # 1. Seed Users (Admin + Test Users)
        result = await session.execute(select(User))
        existing_users = result.scalars().all()
        if not existing_users:
            print("--- SEEDING USERS ---")
            # 1. Seed Admin
            admin_email = "admin@almoratab.ma"
            admin_password = "almoratab123"
            hashed_admin_pass = hash_password(admin_password)
            admin = User(
                full_name="Admin",
                email=admin_email,
                hashed_password=hashed_admin_pass,
                role="admin"
            )
            session.add(admin)
            print(f"Seeding admin -> Email: {admin_email} | Password: {admin_password}")

            # 2. Seed Users
            for user_data in SEED_USERS:
                # Extract username from email (part before @)
                username = user_data["email"].split("@")[0]
                # Generate 3 random digits
                rand_digits = "".join(str(random.randint(0, 9)) for _ in range(3))
                plain_password = f"{username}{rand_digits}"
                hashed_pass = hash_password(plain_password)

                # Assign superUser role to specific users
                role = "user"
                if user_data["full_name"] in ["Bouchra Salil", "Fairouz Massaly"]:
                    role = "superUser"

                user = User(
                    full_name=user_data["full_name"],
                    email=user_data["email"],
                    hashed_password=hashed_pass,
                    role=role
                )
                session.add(user)
                print(f"Seeding user  -> Name: {user_data['full_name']} | Role: {role} | Email: {user_data['email']} | Password: {plain_password}")
        else:
            print(f"Database already has {len(existing_users)} users. Skipping user seeding.")

        # 3. Seed/Update Sprints (14 days each).
        # Sprints 1 & 2 run back-to-back from 2026-06-15; Sprint 3 is delayed to
        # 2026-09-21, and Sprint 4 cascades right after it.
        SPRINT1_START = date(2026, 6, 15)  # Monday
        SPRINT3_START = date(2026, 9, 21)  # Monday (delayed)
        SPRINT_START_DATES = [
            SPRINT1_START,                      # Sprint 1
            SPRINT1_START + timedelta(days=14), # Sprint 2
            SPRINT3_START,                      # Sprint 3 (delayed)
            SPRINT3_START + timedelta(days=14), # Sprint 4 (cascades after Sprint 3)
        ]
        EXPECTED_SPRINTS = len(SPRINT_START_DATES)

        result = await session.execute(select(Sprint).order_by(Sprint.sprint_number))
        existing_sprints = result.scalars().all()
        existing_by_num = {s.sprint_number: s for s in existing_sprints}

        sprint_objects = []
        for i in range(EXPECTED_SPRINTS):
            s_num = i + 1
            start = SPRINT_START_DATES[i]
            end = start + timedelta(days=13)
            is_active = (s_num == 1)

            if s_num in existing_by_num:
                # Update existing sprint if dates are wrong
                sprint = existing_by_num[s_num]
                if sprint.start_date != start or sprint.end_date != end:
                    sprint.start_date = start
                    sprint.end_date = end
                    sprint.is_active = is_active
                    print(f"Updated Sprint {s_num} -> Dates: {start} to {end} | Active: {is_active}")
                else:
                    print(f"Sprint {s_num} already correct. Skipping.")
                sprint_objects.append(sprint)
            else:
                # Create missing sprint
                sprint = Sprint(
                    sprint_number=s_num,
                    start_date=start,
                    end_date=end,
                    is_active=is_active
                )
                session.add(sprint)
                sprint_objects.append(sprint)
                print(f"Seeding Sprint {s_num} -> Dates: {start} to {end} | Active: {is_active}")

        await session.flush()  # Flush to get generated IDs for new sprints

        # 4. Seed Live Sessions (2 per sprint). Session dates are derived from the
        # sprint start date, so refresh them if the sprint was rescheduled.
        for sprint in sprint_objects:
            result = await session.execute(
                select(LiveSession).where(LiveSession.sprint_id == sprint.id)
            )
            existing_sessions = {s.session_number: s for s in result.scalars().all()}

            session1_date = sprint.start_date + timedelta(days=2)  # Wednesday
            session2_date = sprint.start_date + timedelta(days=9)  # Wednesday next week
            expected = {1: session1_date, 2: session2_date}

            for s_num, s_date in expected.items():
                if s_num in existing_sessions:
                    existing = existing_sessions[s_num]
                    if existing.session_date != s_date:
                        existing.session_date = s_date
                        print(f"Updated Live Session {s_num} for Sprint {sprint.sprint_number} -> {s_date}")
                else:
                    session.add(LiveSession(
                        sprint_id=sprint.id,
                        session_number=s_num,
                        session_date=s_date,
                        title=f"Sprint {sprint.sprint_number} - Session {s_num}"
                    ))
                    print(f"Seeding Live Session {s_num} for Sprint {sprint.sprint_number} -> {s_date}")

        await session.commit()
        print("--- SEEDING COMPLETED SUCCESSFULY ---")

if __name__ == "__main__":
    asyncio.run(seed_data())