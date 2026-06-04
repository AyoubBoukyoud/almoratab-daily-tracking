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
        # Check if users already exist
        result = await session.execute(select(User))
        existing_users = result.scalars().all()
        if existing_users:
            print("Database already seeded with users. Skipping.")
            return

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
        seeded_users = []
        for user_data in SEED_USERS:
            # Extract username from email (part before @)
            username = user_data["email"].split("@")[0]
            # Generate 3 random digits
            rand_digits = "".join(str(random.randint(0, 9)) for _ in range(3))
            plain_password = f"{username}{rand_digits}"
            hashed_pass = hash_password(plain_password)

            user = User(
                full_name=user_data["full_name"],
                email=user_data["email"],
                hashed_password=hashed_pass,
                role="user"
            )
            session.add(user)
            seeded_users.append(user)
            print(f"Seeding user  -> Name: {user_data['full_name']} | Email: {user_data['email']} | Password: {plain_password}")

        # 3. Seed Sprints (5 sprints of 14 days each, Monday-Sunday)
        # We base Sprint 3 around today (2026-06-04 is a Thursday in week 1 of Sprint 3 starting Monday 2026-06-01)
        sprint3_start = date(2026, 6, 1) # Monday
        sprint_ranges = [
            (1, sprint3_start - timedelta(days=28), sprint3_start - timedelta(days=15)), # Sprint 1
            (2, sprint3_start - timedelta(days=14), sprint3_start - timedelta(days=1)),  # Sprint 2
            (3, sprint3_start, sprint3_start + timedelta(days=13)),                     # Sprint 3 (Active)
            (4, sprint3_start + timedelta(days=14), sprint3_start + timedelta(days=27)), # Sprint 4
            (5, sprint3_start + timedelta(days=28), sprint3_start + timedelta(days=41)), # Sprint 5
        ]

        print("--- SEEDING SPRINTS ---")
        sprint_objects = []
        for s_num, start, end in sprint_ranges:
            # Sprint 3 is active
            is_active = (s_num == 3)
            sprint = Sprint(
                sprint_number=s_num,
                start_date=start,
                end_date=end,
                is_active=is_active
            )
            session.add(sprint)
            sprint_objects.append(sprint)
            print(f"Seeding Sprint {s_num} -> Dates: {start} to {end} | Active: {is_active}")

        await session.flush() # Flush to get generated IDs

        # 4. Seed Live Sessions (2 per sprint)
        print("--- SEEDING LIVE SESSIONS ---")
        for sprint in sprint_objects:
            # Session 1 in week 1 (e.g. Wednesday)
            session1_date = sprint.start_date + timedelta(days=2) # Wednesday
            session1 = LiveSession(
                sprint_id=sprint.id,
                session_number=1,
                session_date=session1_date,
                title=f"Sprint {sprint.sprint_number} - Session 1"
            )
            
            # Session 2 in week 2 (e.g. Wednesday)
            session2_date = sprint.start_date + timedelta(days=9) # Wednesday next week
            session2 = LiveSession(
                sprint_id=sprint.id,
                session_number=2,
                session_date=session2_date,
                title=f"Sprint {sprint.sprint_number} - Session 2"
            )
            
            session.add(session1)
            session.add(session2)
            print(f"Seeding Live Sessions for Sprint {sprint.sprint_number} (Dates: {session1_date}, {session2_date})")

        await session.commit()
        print("--- SEEDING COMPLETED SUCCESSFULY ---")

if __name__ == "__main__":
    asyncio.run(seed_data())
