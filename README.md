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
