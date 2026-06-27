# رحلة البزنس المرتب — Almoratab Daily Tracker

A full-stack application for tracking daily tasks, sprints, and points for a structured business training program.

## 🚀 Local Setup Instructions

Follow these steps to get the project running on your local machine.

### 1. Database Setup (PostgreSQL)
- Ensure you have **PostgreSQL** installed and running.
- Create a database named `almoratab`.
- Update the `backend/.env` file with your PostgreSQL credentials:
  ```env
  DATABASE_URL=postgresql+asyncpg://<user>:<password>@localhost:5432/almoratab
  ```
  *(Default is `postgres:password`)*

### 2. Backend Setup
1. Open a terminal and navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run database migrations:
   ```bash
   alembic upgrade head
   ```
5. Seed the initial data (users, sprints, sessions):
   ```bash
   python seeds/seed_users.py
   ```
6. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
   The backend will be available at `http://localhost:8000`.

### 3. Frontend Setup
1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`.

## 🔑 Default Credentials

After seeding, you can log in with:

- **Admin:** `admin@almoratab.ma` / `almoratab123`
- **Learners:** Check the output of the seed script or your `users` table for generated passwords.

## 🛠 Tech Stack
- **Frontend:** React JS, Tailwind CSS, Zustand, Framer Motion, Recharts.
- **Backend:** FastAPI, SQLAlchemy, Alembic, PostgreSQL.
- **Auth:** JWT (Access + Refresh tokens in HTTP-only cookies).

User Credentials (DEFINITIVE LIST):

  ┌──────────────────────┬───────────────────────┬──────────────┐
  │ Name                 │ Email                 │ Password     │
  ├──────────────────────┼───────────────────────┼──────────────┤
  │ Admin                │ admin@almoratab.ma    │ almoratab123 │
  │ Bouchra Salil        │ bouchra@almoratab.ma  │ bouchra308   │
  │ Fairouz Massaly      │ fairouz@almoratab.ma  │ fairouz520   │
  │ Fatima Amgour        │ fatima.a@almoratab.ma │ fatima.a860  │
  │ Fatima Zohra Belbout │ fatima.z@almoratab.ma │ fatima.z039  │
  │ Karima Faouzi        │ karima@almoratab.ma   │ karima298    │
  │ Meriem Makoudi       │ meriem@almoratab.ma   │ meriem336    │
  │ Nadia Bouhafoura     │ nadia@almoratab.ma    │ nadia414     │
  └──────────────────────┴───────────────────────┴──────────────┘
- 1) Présence au premier live = 8 pts chacune
  INSERT INTO live_attendance
    (id, user_id, live_session_id, validated_by, points_awarded, validated_at)
  SELECT
    gen_random_uuid(),
    p.id,
    ls.id,
    adm.id,
    8,
    now()
  FROM users p
  CROSS JOIN (SELECT id FROM users WHERE email = 'admin@almoratab.ma' LIMIT 1) adm
  CROSS JOIN (
    SELECT ls.id
    FROM live_sessions ls
    JOIN sprints s ON s.id = ls.sprint_id
    WHERE s.sprint_number = 1 AND ls.session_number = 1
    LIMIT 1
  ) ls
  WHERE p.email IN (
    'bouchra@almoratab.ma','fairouz@almoratab.ma','fatima.a@almoratab.ma',
    'fatima.z@almoratab.ma','karima@almoratab.ma','meriem@almoratab.ma','nadia@almoratab.ma'
  )
  ON CONFLICT (user_id, live_session_id) DO NOTHING;


  -- 2) 6 jours de tâches (15→20 juin), 7 pts/jour
  --    Bouchra : task3 non faite le 16/06 (=> 4 pts ce jour-là)
  INSERT INTO task_submissions
    (id, user_id, sprint_id, submission_date, task1_done, task2_done, task3_done, points_earned, submitted_at)
  SELECT
    gen_random_uuid(),
    p.id,
    s.id,
    d::date,
    true,                                                                    -- task1 (2 pts)
    true,                                                                    -- task2 (2 pts)
    NOT (p.email = 'bouchra@almoratab.ma' AND d::date = '2026-06-16'),       -- task3 (3 pts) sauf Bouchra le 16
    CASE WHEN p.email = 'bouchra@almoratab.ma' AND d::date = '2026-06-16'
         THEN 4 ELSE 7 END,
    now()
  FROM users p
  CROSS JOIN (SELECT id FROM sprints WHERE sprint_number = 1 LIMIT 1) s
  CROSS JOIN generate_series('2026-06-15'::date, '2026-06-20'::date, '1 day') d
  WHERE p.email IN (
    'bouchra@almoratab.ma','fairouz@almoratab.ma','fatima.a@almoratab.ma',
    'fatima.z@almoratab.ma','karima@almoratab.ma','meriem@almoratab.ma','nadia@almoratab.ma'
  )
  ON CONFLICT (user_id, submission_date) DO NOTHING;

  Totals this produces:
  - 6 participantes : 8 (live) + 6 × 7 = 50 pts
  - Bouchra Salil : 8 (live) + 5 × 7 + 1 × 4 = 47 pts

  Quick check after running:
  SELECT u.full_name,
         (SELECT COALESCE(SUM(points_awarded),0) FROM live_attendance la WHERE la.user_id = u.id) +
         (SELECT COALESCE(SUM(points_earned),0)  FROM task_submissions ts WHERE ts.user_id = u.id) AS total
  FROM users u
  WHERE u.role <> 'admin'
  ORDER BY total DESC;
