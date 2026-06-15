# رحلة البزنس المرتب — Full Stack Web App
## Complete Project Plan & Technical Specification

> **Stack:** React JS · FastAPI · PostgreSQL · JWT Auth  
> **Training period:** 5 sprints × 12 active days = 60 training days  
> **Point target:** 400 points per learner  
> **Rest day:** Sunday (task submission locked)

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Tech Stack & Justification](#2-tech-stack--justification)
3. [System Architecture](#3-system-architecture)
4. [Points & Sprint System](#4-points--sprint-system)
5. [Users & Roles](#5-users--roles)
6. [Database Schema](#6-database-schema)
7. [Backend — FastAPI](#7-backend--fastapi)
8. [Frontend — React JS](#8-frontend--react-js)
9. [User Dashboard — Detailed Spec](#9-user-dashboard--detailed-spec)
10. [Admin Control Panel — Detailed Spec](#10-admin-control-panel--detailed-spec)
11. [Authentication Flow](#11-authentication-flow)
12. [API Endpoints Reference](#12-api-endpoints-reference)
13. [Project Folder Structure](#13-project-folder-structure)
14. [Development Phases & Milestones](#14-development-phases--milestones)
15. [UI/UX Design System](#15-uiux-design-system)
16. [Business Logic Rules](#16-business-logic-rules)
17. [Deployment Plan](#17-deployment-plan)

---

## 1. Project Overview

**رحلة البزنس المرتب** ("The Organized Business Journey") is a full-stack web application designed to track daily task completion, monitor progress, and award points to participants throughout a structured business training program.

The platform replaces the existing static HTML/Google Sheets setup with a proper authenticated, database-backed web application that gives each learner a personalized, interactive experience and gives the admin full real-time visibility into cohort performance.

### Core Concept

- **7 learners** follow a 5-sprint training program (each sprint = 2 weeks, 6 active days + 1 rest day = 12 active days per sprint).
- Each active day (Monday–Saturday), learners check off **3 daily tasks** worth **2 points each** = 6 pts/day.
- Each sprint also has **2 live sessions** where the admin validates attendance: **4 pts each** = 8 pts/sprint from lives.
- Total per sprint: **72 pts (tasks) + 8 pts (lives) = 80 pts**.
- Grand total across 5 sprints: **400 points**.
- The app tracks everything in real time, enforces Sunday locks, and gives the admin tools to manage live attendance validation.

### Key Goals

- Replace manual tracking with a reliable, persistent system
- Give each learner a motivating, gamified dashboard
- Give the admin a full visibility panel with per-user analytics
- Enforce business rules (Sunday lock, one submission per day, live validation by admin only)
- Maintain the existing Almoratab brand identity (dark teal + gold palette, Arabic title, logo)

---

## 2. Tech Stack & Justification

### Frontend

| Technology | Version | Purpose |
|---|---|---|
| React JS | 18+ | Component-based SPA framework |
| React Router | v6 | Client-side routing with protected routes |
| Zustand | latest | Lightweight global state (auth token, user info) |
| Axios | latest | HTTP client with JWT interceptor |
| Framer Motion | latest | Animated points circle, task card transitions |
| Recharts | latest | Admin charts — daily progress line chart |
| Tailwind CSS | v3 | Utility-first styling aligned with brand tokens |
| React Hot Toast | latest | Submission feedback notifications |

### Backend

| Technology | Version | Purpose |
|---|---|---|
| Python | 3.11+ | Language |
| FastAPI | latest | Async REST API framework |
| SQLAlchemy | 2.x | ORM with async support |
| Alembic | latest | Database migrations |
| Pydantic | v2 | Request/response validation and serialization |
| python-jose | latest | JWT encoding/decoding |
| passlib + bcrypt | latest | Password hashing |
| Uvicorn | latest | ASGI server |

### Database

| Technology | Version | Purpose |
|---|---|---|
| PostgreSQL | 16 | Primary relational database |
| asyncpg | latest | Async PostgreSQL driver |

### Infrastructure & Dev Tools

| Tool | Purpose |
|---|---|
| Docker + Docker Compose | Local dev environment (app + db) |
| python-dotenv | Environment variable management |
| CORS middleware | Allow React frontend to call the API |
| Pytest + httpx | Backend testing |
| Vite | React dev server and build tool |

---

## 3. System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT (Browser)                      │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                    React SPA (Vite)                   │   │
│  │                                                       │   │
│  │   ┌─────────────┐      ┌──────────────────────────┐  │   │
│  │   │ User Routes  │      │    Admin Routes          │  │   │
│  │   │ /dashboard   │      │    /admin                │  │   │
│  │   │ /login       │      │    /admin/users/:id      │  │   │
│  │   └─────────────┘      └──────────────────────────┘  │   │
│  │                                                       │   │
│  │   Zustand Store: { user, token, role }                │   │
│  │   Axios Instance: Bearer token auto-attached          │   │
│  └────────────────────────┬──────────────────────────────┘  │
└───────────────────────────┼──────────────────────────────────┘
                             │ HTTPS/REST (JSON)
                             │
┌───────────────────────────▼──────────────────────────────────┐
│                     FastAPI Backend                           │
│                                                               │
│   ┌────────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│   │ /auth      │  │ /tasks   │  │ /admin   │  │ /users   │  │
│   │ POST login │  │ POST sub.│  │ GET users│  │ GET me   │  │
│   │ POST signup│  │ GET today│  │ POST live│  │          │  │
│   └────────────┘  └──────────┘  └──────────┘  └──────────┘  │
│                                                               │
│   JWT Middleware → Role Guard → Service Layer → SQLAlchemy    │
└───────────────────────────┬───────────────────────────────────┘
                             │ asyncpg
                             │
┌───────────────────────────▼───────────────────────────────────┐
│                       PostgreSQL 16                           │
│                                                               │
│   users · sprints · task_submissions · live_sessions ·        │
│   live_attendance                                             │
└───────────────────────────────────────────────────────────────┘
```

---

## 4. Points & Sprint System

### Sprint Structure

Each sprint covers **2 calendar weeks** with **6 active days** per week and **Sunday as a forced rest day**:

```
Week 1:  Mon Tue Wed Thu Fri Sat [SUN-OFF]
Week 2:  Mon Tue Wed Thu Fri Sat [SUN-OFF]
                                  ↓
          12 active task days per sprint
```

### Points Breakdown

```
Per day:
  Task 1 — Daily          → 2 pts
  Task 2 — Sport          → 2 pts
  Task 3 — Project contrib → 2 pts
  ─────────────────────────────────
  Total per active day    = 6 pts

Per sprint (12 days):
  Task points  = 12 × 6   = 72 pts
  Live session 1           =  4 pts  (admin validates)
  Live session 2           =  4 pts  (admin validates)
  ─────────────────────────────────
  Sprint total             = 80 pts

Grand total (5 sprints):
  5 × 80 = 400 pts  ← target score
```

### Sprint Calendar Table

| Sprint | Start Date | End Date | Active Days | Max Task Pts | Max Live Pts | Sprint Max |
|--------|-----------|---------|------------|-------------|-------------|------------|
| Sprint 1 | TBD | TBD + 13 | 12 | 72 | 8 | 80 |
| Sprint 2 | TBD | TBD + 13 | 12 | 72 | 8 | 80 |
| Sprint 3 | TBD | TBD + 13 | 12 | 72 | 8 | 80 |
| Sprint 4 | TBD | TBD + 13 | 12 | 72 | 8 | 80 |
| Sprint 5 | TBD | TBD + 13 | 12 | 72 | 8 | 80 |
| **TOTAL** | | | **60** | **360** | **40** | **400** |

> **Note:** Sprint start dates are configured by the admin in the database before the program begins. The system uses these dates to determine which sprint is currently active and whether a given day is eligible for task submission.

### Sunday Lock Logic

The backend checks the day of week on every `POST /tasks/submit` call:

```python
from datetime import date

def is_submission_allowed(submission_date: date) -> bool:
    # Sunday = weekday 6 in Python
    if submission_date.weekday() == 6:
        return False
    return True
```

This is enforced **server-side** — the frontend also hides the submit button on Sundays, but the backend will reject any attempt regardless.

---

## 5. Users & Roles

### Registered Users

| # | Full Name | Role | Email (suggested) | Default Password |
|---|-----------|------|------------------|-----------------|
| 1 | Bouchra Salil | user | bouchra@almoratab.ma | Change on first login |
| 2 | Fairouz Massaly | user | fairouz@almoratab.ma | Change on first login |
| 3 | Fatima Amgour | user | fatima.a@almoratab.ma | Change on first login |
| 4 | Fatima Zohra Belbout | user | fatima.z@almoratab.ma | Change on first login |
| 5 | Karima Faouzi | user | karima@almoratab.ma | Change on first login |
| 6 | Meriem Makoudi | user | meriem@almoratab.ma | Change on first login |
| 7 | Nadia Bouhafoura | user | nadia@almoratab.ma | Change on first login |
| — | Admin | admin | admin@almoratab.ma | Secure password |

> **Note on signup:** Because the user list is fixed and known in advance, users are **seeded directly into the database** at deployment. The sign-up endpoint exists for future cohorts, but for this cohort users receive their credentials from the admin and must change their password on first login.

### Role Permissions Matrix

| Feature | User | Admin |
|---------|------|-------|
| Login / logout | ✅ | ✅ |
| View own dashboard | ✅ | ✅ |
| Submit daily tasks (Mon–Sat) | ✅ | ✅ |
| View own points and progress | ✅ | ✅ |
| View own task history | ✅ | ✅ |
| View other users' data | ❌ | ✅ |
| Validate live attendance | ❌ | ✅ |
| Access admin panel | ❌ | ✅ |
| View leaderboard | ❌ | ✅ |
| View per-user progress chart | ❌ | ✅ |
| Create/manage sprints | ❌ | ✅ |

---

## 6. Database Schema

### Table: `users`

```sql
CREATE TABLE users (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name   VARCHAR(100) NOT NULL,
    email       VARCHAR(150) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role        VARCHAR(20) NOT NULL DEFAULT 'user',  -- 'user' | 'admin'
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Table: `sprints`

```sql
CREATE TABLE sprints (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sprint_number   INTEGER NOT NULL UNIQUE,  -- 1, 2, 3...
    start_date      DATE NOT NULL,
    end_date        DATE NOT NULL,
    is_active       BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    CONSTRAINT sprint_number_positive CHECK (sprint_number >= 1),
    CONSTRAINT valid_dates CHECK (end_date > start_date)
);
```

### Table: `task_submissions`

```sql
CREATE TABLE task_submissions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    sprint_id       UUID NOT NULL REFERENCES sprints(id) ON DELETE CASCADE,
    submission_date DATE NOT NULL,
    task1_done      BOOLEAN NOT NULL DEFAULT FALSE,   -- Daily
    task2_done      BOOLEAN NOT NULL DEFAULT FALSE,   -- Sport
    task3_done      BOOLEAN NOT NULL DEFAULT FALSE,   -- Project contribution
    points_earned   INTEGER NOT NULL DEFAULT 0,        -- 0, 2, 4, or 6
    submitted_at    TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- One submission per user per day
    CONSTRAINT unique_submission UNIQUE (user_id, submission_date),
    -- Points must match tasks done
    CONSTRAINT valid_points CHECK (
        points_earned = (task1_done::int + task2_done::int + task3_done::int) * 2
    )
);
```

### Table: `live_sessions`

```sql
CREATE TABLE live_sessions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sprint_id       UUID NOT NULL REFERENCES sprints(id) ON DELETE CASCADE,
    session_number  INTEGER NOT NULL,   -- 1 or 2 within the sprint
    session_date    DATE,
    title           VARCHAR(200),
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    CONSTRAINT session_number_range CHECK (session_number BETWEEN 1 AND 2),
    CONSTRAINT unique_session UNIQUE (sprint_id, session_number)
);
```

### Table: `live_attendance`

```sql
CREATE TABLE live_attendance (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    live_session_id UUID NOT NULL REFERENCES live_sessions(id) ON DELETE CASCADE,
    validated_by    UUID NOT NULL REFERENCES users(id),   -- must be admin
    validated_at    TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    points_awarded  INTEGER NOT NULL DEFAULT 4,

    -- Prevent double-validation for same user + session
    CONSTRAINT unique_attendance UNIQUE (user_id, live_session_id)
);
```

### Entity Relationship Diagram (ERD)

```
users (1) ────────────── (N) task_submissions
  │                             │
  │                          sprint_id
  │                             │
  │                         sprints (1) ─── (N) live_sessions
  │                                                  │
  └──── (N) live_attendance ──────────────────── (1)┘
           validated_by → users.id (admin)
```

### Key Indexes

```sql
-- Fast lookup of user's submissions
CREATE INDEX idx_submissions_user_date ON task_submissions(user_id, submission_date);

-- Fast admin dashboard queries
CREATE INDEX idx_submissions_sprint ON task_submissions(sprint_id);

-- Fast attendance lookups
CREATE INDEX idx_attendance_user ON live_attendance(user_id);
CREATE INDEX idx_attendance_session ON live_attendance(live_session_id);
```

---

## 7. Backend — FastAPI

### Project Structure

```
backend/
├── main.py                    # FastAPI app init, CORS, router registration
├── .env                       # Environment variables (never commit)
├── .env.example               # Template for env vars
├── requirements.txt
│
├── core/
│   ├── config.py              # Settings via pydantic-settings
│   ├── database.py            # Async SQLAlchemy engine + session factory
│   └── security.py            # JWT creation/verification, password hashing
│
├── models/                    # SQLAlchemy ORM models
│   ├── user.py
│   ├── sprint.py
│   ├── task_submission.py
│   ├── live_session.py
│   └── live_attendance.py
│
├── schemas/                   # Pydantic request/response schemas
│   ├── auth.py                # LoginRequest, TokenResponse
│   ├── user.py                # UserOut, UserCreate
│   ├── task.py                # TaskSubmitRequest, TaskSubmissionOut
│   ├── sprint.py              # SprintOut
│   ├── live.py                # LiveSessionOut, AttendanceValidate
│   └── admin.py               # UserProgressOut, LeaderboardEntry
│
├── routers/                   # Route handlers
│   ├── auth.py                # POST /auth/login, POST /auth/register
│   ├── tasks.py               # POST /tasks/submit, GET /tasks/today, GET /tasks/history
│   ├── users.py               # GET /users/me, GET /users/me/stats
│   ├── sprints.py             # GET /sprints/current, GET /sprints/
│   └── admin.py               # Admin-only endpoints
│
├── services/                  # Business logic
│   ├── points_service.py      # Calculate and aggregate points
│   ├── sprint_service.py      # Determine current sprint, active day check
│   └── auth_service.py        # User auth logic
│
├── dependencies/
│   └── auth.py                # get_current_user, require_admin deps
│
├── migrations/                # Alembic migration files
│   ├── env.py
│   └── versions/
│       └── 001_initial_schema.py
│
└── tests/
    ├── conftest.py
    ├── test_auth.py
    ├── test_tasks.py
    └── test_admin.py
```

### Environment Variables (`.env`)

```env
# Database
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/almoratab

# JWT
SECRET_KEY=your-very-long-random-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# App
APP_ENV=development
FRONTEND_URL=http://localhost:5173
```

### JWT Token Strategy

The app uses **two tokens**:

- **Access token** — short-lived (60 minutes), sent with every API request in the `Authorization: Bearer <token>` header.
- **Refresh token** — long-lived (7 days), stored in an HTTP-only cookie. Used to obtain a new access token silently when it expires.

```python
# core/security.py

from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(user_id: str, role: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": user_id, "role": role, "exp": expire, "type": "access"}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
```

### Role-Based Dependency Injection

```python
# dependencies/auth.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ..core.security import decode_token
from ..services.auth_service import get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def require_admin(current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user
```

### Points Calculation Service

```python
# services/points_service.py

async def get_user_total_points(db, user_id: str) -> int:
    """Sum all task points + live attendance points for a user."""
    task_pts = await db.scalar(
        select(func.sum(TaskSubmission.points_earned))
        .where(TaskSubmission.user_id == user_id)
    ) or 0

    live_pts = await db.scalar(
        select(func.sum(LiveAttendance.points_awarded))
        .where(LiveAttendance.user_id == user_id)
    ) or 0

    return task_pts + live_pts


async def get_user_sprint_stats(db, user_id: str, sprint_id: str) -> dict:
    """Returns task points, live points, and max possible for one sprint."""
    task_pts = await db.scalar(
        select(func.sum(TaskSubmission.points_earned))
        .where(TaskSubmission.user_id == user_id)
        .where(TaskSubmission.sprint_id == sprint_id)
    ) or 0

    live_pts = await db.scalar(
        select(func.sum(LiveAttendance.points_awarded))
        .join(LiveSession)
        .where(LiveAttendance.user_id == user_id)
        .where(LiveSession.sprint_id == sprint_id)
    ) or 0

    return {
        "task_points": task_pts,
        "live_points": live_pts,
        "total": task_pts + live_pts,
        "max_task_points": 72,
        "max_live_points": 8,
        "max_total": 80
    }
```

---

## 8. Frontend — React JS

### Project Structure

```
frontend/
├── index.html
├── vite.config.js
├── tailwind.config.js
├── package.json
│
└── src/
    ├── main.jsx               # React root, QueryClient, Router
    ├── App.jsx                # Route definitions
    │
    ├── api/
    │   ├── client.js          # Axios instance with JWT interceptor
    │   ├── auth.js            # login(), register(), logout()
    │   ├── tasks.js           # submitTasks(), getTodayStatus(), getHistory()
    │   ├── users.js           # getMe(), getMyStats()
    │   └── admin.js           # getUsers(), validateAttendance(), getUserDetail()
    │
    ├── store/
    │   └── authStore.js       # Zustand: user, token, role, setAuth, clearAuth
    │
    ├── hooks/
    │   ├── useAuth.js         # Auth helpers + redirect logic
    │   ├── useTasks.js        # Today's task state + submit handler
    │   └── usePoints.js       # Fetch and format points data
    │
    ├── components/
    │   ├── layout/
    │   │   ├── UserLayout.jsx     # Wrapper for user pages (header, nav)
    │   │   └── AdminLayout.jsx    # Wrapper for admin pages
    │   │
    │   ├── ui/
    │   │   ├── PointsRing.jsx     # Animated SVG radial progress circle
    │   │   ├── TaskCard.jsx       # Single task checkbox card
    │   │   ├── SprintBar.jsx      # Horizontal sprint progress bar
    │   │   ├── UserProgressRow.jsx # Admin table row with mini progress bar
    │   │   ├── ProgressChart.jsx  # Recharts line chart for admin detail
    │   │   └── Toast.jsx          # Notification toasts
    │   │
    │   └── auth/
    │       └── ProtectedRoute.jsx # Redirects if not logged in or wrong role
    │
    └── pages/
        ├── Login.jsx              # Login form
        ├── UserDashboard.jsx      # Main user page
        └── admin/
            ├── AdminPanel.jsx     # Users table + leaderboard
            └── UserDetail.jsx     # Per-user progress drilldown
```

### Axios Client with JWT Auto-Attach

```javascript
// api/client.js
import axios from 'axios';
import { useAuthStore } from '../store/authStore';

const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' }
});

// Attach JWT to every request
client.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Handle 401 — clear auth and redirect to login
client.interceptors.response.use(
  (res) => res,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().clearAuth();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default client;
```

### Zustand Auth Store

```javascript
// store/authStore.js
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const useAuthStore = create(
  persist(
    (set) => ({
      user: null,
      token: null,
      role: null,
      setAuth: (user, token) => set({ user, token, role: user.role }),
      clearAuth: () => set({ user: null, token: null, role: null })
    }),
    { name: 'almoratab-auth' }
  )
);
```

### Protected Route Component

```jsx
// components/auth/ProtectedRoute.jsx
import { Navigate } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';

export function ProtectedRoute({ children, requiredRole }) {
  const { token, role } = useAuthStore();

  if (!token) return <Navigate to="/login" replace />;
  if (requiredRole && role !== requiredRole) return <Navigate to="/dashboard" replace />;

  return children;
}
```

### App Routing

```jsx
// App.jsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ProtectedRoute } from './components/auth/ProtectedRoute';
import Login from './pages/Login';
import UserDashboard from './pages/UserDashboard';
import AdminPanel from './pages/admin/AdminPanel';
import UserDetail from './pages/admin/UserDetail';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={
          <ProtectedRoute><UserDashboard /></ProtectedRoute>
        } />
        <Route path="/admin" element={
          <ProtectedRoute requiredRole="admin"><AdminPanel /></ProtectedRoute>
        } />
        <Route path="/admin/users/:userId" element={
          <ProtectedRoute requiredRole="admin"><UserDetail /></ProtectedRoute>
        } />
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
```

---

## 9. User Dashboard — Detailed Spec

### Layout Structure

```
┌──────────────────────────────────────────────────────────┐
│  HEADER                                                   │
│  [Logo]  رحلة البزنس المرتب          Bonjour, Bouchra 👋 │
│          ─────────────────────────────────────────────   │
└──────────────────────────────────────────────────────────┘
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │           POINTS CIRCLE (center stage)              │ │
│  │                                                     │ │
│  │         ╭───────────────────╮                       │ │
│  │        ╱                     ╲                      │ │
│  │       │    240 / 400 pts      │                     │ │
│  │       │    ████████░░░        │                     │ │
│  │        ╲                     ╱                      │ │
│  │         ╰───────────────────╯                       │ │
│  │              Sprint 3 · Day 6                       │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  TODAY'S TASKS   (disabled on Sunday / if done)     │ │
│  │  ┌──────────────────┐  ✅ Task 1 — Daily            │ │
│  │  │                  │  ✅ Task 2 — Sport             │ │
│  │  │   3 checkboxes   │  ⬜ Task 3 — Project Contrib   │ │
│  │  │                  │                               │ │
│  │  └──────────────────┘                               │ │
│  │                    [ Submit my day →  ]             │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  SPRINT PROGRESS                                    │ │
│  │  Sprint 1 ████████████████████ 80/80  ✅            │ │
│  │  Sprint 2 ████████████████░░░░ 64/80               │ │
│  │  Sprint 3 ████████░░░░░░░░░░░░ 36/80  ← CURRENT    │ │
│  │  Sprint 4 ░░░░░░░░░░░░░░░░░░░░  0/80               │ │
│  │  Sprint 5 ░░░░░░░░░░░░░░░░░░░░  0/80               │ │
│  └─────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘
```

### Points Ring Component — Detailed Spec

The `PointsRing` component is the centerpiece of the user dashboard. It uses an SVG circle with a `stroke-dasharray` technique animated by Framer Motion.

```jsx
// components/ui/PointsRing.jsx
import { motion } from 'framer-motion';

const RADIUS = 90;
const CIRCUMFERENCE = 2 * Math.PI * RADIUS; // ≈ 565.5

export function PointsRing({ current, max = 400, sprintInfo }) {
  const percentage = current / max;
  const strokeDashoffset = CIRCUMFERENCE * (1 - percentage);

  return (
    <div className="flex flex-col items-center py-8">
      <svg width="220" height="220" viewBox="0 0 220 220">
        {/* Background track */}
        <circle
          cx="110" cy="110" r={RADIUS}
          fill="none"
          stroke="#1A4D4A"
          strokeWidth="14"
        />
        {/* Animated progress arc */}
        <motion.circle
          cx="110" cy="110" r={RADIUS}
          fill="none"
          stroke="#C9982A"
          strokeWidth="14"
          strokeLinecap="round"
          strokeDasharray={CIRCUMFERENCE}
          initial={{ strokeDashoffset: CIRCUMFERENCE }}
          animate={{ strokeDashoffset }}
          transition={{ duration: 1.4, ease: "easeOut" }}
          style={{ transform: 'rotate(-90deg)', transformOrigin: '110px 110px' }}
        />
        {/* Center text */}
        <text x="110" y="100" textAnchor="middle"
          className="font-bold" fontSize="36" fill="#C9982A">
          {current}
        </text>
        <text x="110" y="124" textAnchor="middle"
          fontSize="14" fill="#6B8280">
          / {max} pts
        </text>
      </svg>
      <p className="text-teal-700 text-sm mt-2">
        {sprintInfo.name} · Day {sprintInfo.currentDay}
      </p>
    </div>
  );
}
```

### Task Card Component

Each task renders as an interactive card with a checkbox. On submit, all three are sent together as a single API call (partial submission is not allowed — a user either submits all 3 or none):

```jsx
// components/ui/TaskCard.jsx
export function TaskCard({ taskNumber, label, emoji, checked, onChange, disabled }) {
  return (
    <div
      className={`
        flex items-center gap-4 p-4 rounded-xl border cursor-pointer
        transition-all duration-200
        ${checked
          ? 'bg-teal-50 border-teal-400 shadow-sm'
          : 'bg-white border-gray-200 hover:border-teal-300'}
        ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
      `}
      onClick={() => !disabled && onChange(!checked)}
    >
      <span className="text-2xl">{emoji}</span>
      <div className="flex-1">
        <p className="text-sm font-medium text-gray-800">Task {taskNumber}</p>
        <p className="text-base font-semibold text-gray-900">{label}</p>
      </div>
      <div className={`
        w-6 h-6 rounded-full border-2 flex items-center justify-center
        ${checked ? 'bg-teal-600 border-teal-600' : 'border-gray-300'}
      `}>
        {checked && <span className="text-white text-xs">✓</span>}
      </div>
    </div>
  );
}
```

### Task Submission Logic

```jsx
// From UserDashboard.jsx

const [tasks, setTasks] = useState({ task1: false, task2: false, task3: false });
const [submitted, setSubmitted] = useState(false);
const [isLoading, setIsLoading] = useState(false);

const isSunday = new Date().getDay() === 0;
const isDisabled = isSunday || submitted;

const handleSubmit = async () => {
  if (!tasks.task1 && !tasks.task2 && !tasks.task3) {
    toast.error("Please complete at least one task before submitting.");
    return;
  }
  setIsLoading(true);
  try {
    const response = await submitTasks(tasks);
    setSubmitted(true);
    toast.success(`✅ +${response.points_earned} points earned today!`);
    refetchPoints(); // Update the points ring
  } catch (error) {
    if (error.response?.status === 409) {
      toast.error("You've already submitted today.");
    } else {
      toast.error("Submission failed. Please try again.");
    }
  } finally {
    setIsLoading(false);
  }
};
```

---

## 10. Admin Control Panel — Detailed Spec

### Layout Structure

```
┌──────────────────────────────────────────────────────────┐
│  ADMIN HEADER                                            │
│  [Logo]  رحلة البزنس المرتب          Admin Panel  ⚙️    │
└──────────────────────────────────────────────────────────┘

  📊 LEADERBOARD — Sprint 3 in progress
  ──────────────────────────────────────────────────────────
  Rank  Name                  Points  Progress         Action
  ─────────────────────────────────────────────────────────
  🥇 1  Fatima Zohra Belbout  240/400 ████████████░░   Details →
  🥈 2  Meriem Makoudi        220/400 ███████████░░░   Details →
  🥉 3  Karima Faouzi         210/400 ██████████░░░░   Details →
       4  Bouchra Salil        200/400 ██████████░░░░   Details →
       5  Nadia Bouhafoura     192/400 █████████░░░░░   Details →
       6  Fairouz Massaly      180/400 █████████░░░░░   Details →
       7  Fatima Amgour        160/400 ████████░░░░░░   Details →

  🎥 LIVE SESSIONS — Validate Attendance
  ──────────────────────────────────────────────────────────
  Sprint 3 · Live 1 (Week 1)
  ┌──────────────────────────────────────────────────────┐
  │  Bouchra Salil       ✅ Validated  +4 pts            │
  │  Fairouz Massaly     [ Validate +4 pts ]             │
  │  Fatima Amgour       ✅ Validated  +4 pts            │
  │  ...                                                 │
  └──────────────────────────────────────────────────────┘
```

### User Detail Page

```
  ← Back to Admin Panel

  👤 Fatima Zohra Belbout         Total: 240 / 400 pts
  ─────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────┐
  │  PROGRESS CHART (Recharts LineChart)                │
  │                                                     │
  │  400 ┤                               ·········      │
  │  300 ┤                    ···········               │
  │  200 ┤          ··········                          │
  │  100 ┤  ·········                                   │
  │    0 ┼──────────────────────────────────────────→   │
  │      Day 1              Day 30             Day 60   │
  └─────────────────────────────────────────────────────┘

  SPRINT BREAKDOWN
  ┌────────┬──────────┬──────────┬──────────┬──────────┐
  │ Sprint │ Task Pts │ Live Pts │  Total   │  / Max   │
  ├────────┼──────────┼──────────┼──────────┼──────────┤
  │   1    │    72    │    8     │   80     │  80/80   │
  │   2    │    66    │    8     │   74     │  80/80   │
  │   3    │    72    │    4     │   76     │  80/80   │
  │   4    │    —     │    —     │   10     │  80/80   │
  │   5    │    —     │    —     │   —      │  80/80   │
  └────────┴──────────┴──────────┴──────────┴──────────┘

  TASK HISTORY (last 30 days)
  ┌──────────┬──────────┬────────┬───────┬─────────────┐
  │  Date    │  Daily   │ Sport  │ Proj  │  Points     │
  ├──────────┼──────────┼────────┼───────┼─────────────┤
  │ Mon 2/6  │   ✅    │   ✅   │  ✅   │  +6 pts     │
  │ Tue 3/6  │   ✅    │   ✅   │  ✅   │  +6 pts     │
  │ Wed 4/6  │   ✅    │   ❌   │  ✅   │  +4 pts     │
  └──────────┴──────────┴────────┴───────┴─────────────┘
```

### Admin Panel — Key Components

**Leaderboard Table**

```jsx
// Sorted by total_points descending, rank computed client-side
function LeaderboardTable({ users }) {
  const sorted = [...users].sort((a, b) => b.total_points - a.total_points);

  return (
    <table>
      <thead>
        <tr>
          <th>Rank</th><th>Name</th><th>Points</th>
          <th>Progress</th><th>Action</th>
        </tr>
      </thead>
      <tbody>
        {sorted.map((user, index) => (
          <tr key={user.id}>
            <td>{getRankIcon(index + 1)}</td>
            <td>{user.full_name}</td>
            <td>{user.total_points} / 400</td>
            <td>
              <div className="progress-bar-track">
                <div
                  className="progress-bar-fill"
                  style={{ width: `${(user.total_points / 400) * 100}%` }}
                />
              </div>
            </td>
            <td>
              <Link to={`/admin/users/${user.id}`}>Details →</Link>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

**Progress Chart (Recharts)**

```jsx
// components/ui/ProgressChart.jsx
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from 'recharts';

export function ProgressChart({ data }) {
  // data: [{ date: "2026-06-02", cumulative_points: 6 }, ...]
  return (
    <ResponsiveContainer width="100%" height={280}>
      <LineChart data={data} margin={{ top: 10, right: 20, bottom: 10, left: 10 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#D4C5A0" />
        <XAxis dataKey="date" tick={{ fontSize: 11 }} />
        <YAxis domain={[0, 400]} tick={{ fontSize: 11 }} />
        <Tooltip
          formatter={(value) => [`${value} pts`, 'Cumulative Points']}
          labelStyle={{ color: '#1C2B2A' }}
        />
        <Line
          type="monotone"
          dataKey="cumulative_points"
          stroke="#C9982A"
          strokeWidth={2}
          dot={{ r: 3, fill: '#C9982A' }}
          activeDot={{ r: 5 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

---

## 11. Authentication Flow

### Login Flow

```
1. User enters email + password on /login

2. Frontend POST /auth/login { email, password }

3. Backend:
   a. Look up user by email
   b. Verify password hash with bcrypt
   c. If valid → create access token + refresh token
   d. Return: { access_token, token_type, user: { id, name, role } }
   e. Refresh token set as HTTP-only cookie

4. Frontend:
   a. Store access_token + user in Zustand (persisted to localStorage)
   b. Redirect based on role:
      - role == "admin"  → /admin
      - role == "user"   → /dashboard
```

### Token Refresh Flow

```
1. Axios interceptor catches 401 response

2. Frontend POST /auth/refresh (cookie automatically included)

3. Backend validates refresh token from cookie
   → Returns new access_token

4. Interceptor retries the original request with new token

5. If refresh also fails → clearAuth() + redirect to /login
```

### Logout Flow

```
1. User clicks logout

2. Frontend POST /auth/logout
   → Backend clears the refresh token cookie

3. Frontend calls clearAuth()
   → Removes token + user from Zustand + localStorage

4. Redirect to /login
```

---

## 12. API Endpoints Reference

### Auth

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/auth/login` | None | Login → returns JWT |
| POST | `/auth/register` | None | Register new user (admin controlled) |
| POST | `/auth/refresh` | Cookie | Refresh access token |
| POST | `/auth/logout` | Bearer | Clear refresh cookie |

### User (logged-in user)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/users/me` | Bearer | Get current user profile |
| GET | `/users/me/stats` | Bearer | Total points, sprint breakdown, rank |

### Tasks

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/tasks/submit` | Bearer user | Submit today's 3 tasks |
| GET | `/tasks/today` | Bearer user | Check if already submitted today |
| GET | `/tasks/history` | Bearer user | Full task history for current user |
| GET | `/tasks/history?sprint_id=...` | Bearer user | History filtered by sprint |

**POST `/tasks/submit` Request Body:**

```json
{
  "task1_done": true,
  "task2_done": true,
  "task3_done": false
}
```

**Response:**

```json
{
  "id": "uuid",
  "submission_date": "2026-06-04",
  "task1_done": true,
  "task2_done": true,
  "task3_done": false,
  "points_earned": 4,
  "submitted_at": "2026-06-04T09:32:11Z"
}
```

### Sprints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/sprints/` | Bearer | List all 5 sprints |
| GET | `/sprints/current` | Bearer | Get currently active sprint |

### Admin

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/admin/users` | Bearer admin | All users with total points |
| GET | `/admin/users/{user_id}` | Bearer admin | User profile + stats |
| GET | `/admin/users/{user_id}/history` | Bearer admin | Full task history for any user |
| GET | `/admin/users/{user_id}/chart` | Bearer admin | Daily cumulative points data for chart |
| GET | `/admin/leaderboard` | Bearer admin | Users sorted by points |
| GET | `/admin/live-sessions` | Bearer admin | All live sessions across sprints |
| POST | `/admin/live-sessions/{session_id}/validate/{user_id}` | Bearer admin | Validate a user's live attendance |

---

## 13. Project Folder Structure

### Full Monorepo Layout

```
almoratab/
├── README.md
├── docker-compose.yml
├── .gitignore
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env.example
│   ├── main.py
│   ├── alembic.ini
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── sprint.py
│   │   ├── task_submission.py
│   │   ├── live_session.py
│   │   └── live_attendance.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── task.py
│   │   ├── sprint.py
│   │   ├── live.py
│   │   └── admin.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── tasks.py
│   │   ├── users.py
│   │   ├── sprints.py
│   │   └── admin.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── points_service.py
│   │   └── sprint_service.py
│   │
│   ├── dependencies/
│   │   ├── __init__.py
│   │   └── auth.py
│   │
│   ├── migrations/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   │       └── 001_initial_schema.py
│   │
│   ├── seeds/
│   │   └── seed_users.py      # Seeds the 7 learners + admin
│   │
│   └── tests/
│       ├── conftest.py
│       ├── test_auth.py
│       ├── test_tasks.py
│       └── test_admin.py
│
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── index.html
│   │
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── index.css             # Tailwind base + custom brand tokens
│       │
│       ├── api/
│       │   ├── client.js
│       │   ├── auth.js
│       │   ├── tasks.js
│       │   ├── users.js
│       │   └── admin.js
│       │
│       ├── store/
│       │   └── authStore.js
│       │
│       ├── hooks/
│       │   ├── useAuth.js
│       │   ├── useTasks.js
│       │   └── usePoints.js
│       │
│       ├── assets/
│       │   └── almoratab-logo.jpg   # From existing project
│       │
│       ├── components/
│       │   ├── layout/
│       │   │   ├── UserLayout.jsx
│       │   │   └── AdminLayout.jsx
│       │   ├── ui/
│       │   │   ├── PointsRing.jsx
│       │   │   ├── TaskCard.jsx
│       │   │   ├── SprintBar.jsx
│       │   │   ├── UserProgressRow.jsx
│       │   │   ├── ProgressChart.jsx
│       │   │   └── LiveValidationRow.jsx
│       │   └── auth/
│       │       └── ProtectedRoute.jsx
│       │
│       └── pages/
│           ├── Login.jsx
│           ├── UserDashboard.jsx
│           └── admin/
│               ├── AdminPanel.jsx
│               └── UserDetail.jsx
│
└── nginx/
    └── nginx.conf               # Reverse proxy config for production
```

### Docker Compose (Development)

```yaml
# docker-compose.yml
version: '3.9'

services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: almoratab
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql+asyncpg://postgres:password@postgres:5432/almoratab
      SECRET_KEY: dev-secret-key-change-in-production
    depends_on:
      - postgres
    volumes:
      - ./backend:/app
    command: uvicorn main:app --reload --host 0.0.0.0 --port 8000

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    environment:
      VITE_API_URL: http://localhost:8000
    volumes:
      - ./frontend:/app
    command: npm run dev -- --host

volumes:
  postgres_data:
```

---

## 14. Development Phases & Milestones

### Phase 1 — Project Setup & Infrastructure (Days 1–2)

**Goal:** Working development environment with database connected.

Tasks:
- Initialize GitHub repository with monorepo structure
- Set up `docker-compose.yml` with PostgreSQL + backend + frontend services
- Initialize FastAPI project: `main.py`, CORS config, health check endpoint
- Initialize React project with Vite + Tailwind CSS
- Write all SQLAlchemy models
- Write and run the first Alembic migration (all 5 tables)
- Verify DB connection and table creation

**Milestone:** `GET /health` returns `{"status": "ok"}`. All tables visible in database.

---

### Phase 2 — Authentication System (Days 3–4)

**Goal:** Users can log in, receive a JWT, and hit protected endpoints.

Tasks:
- Implement `POST /auth/login` with bcrypt verification + JWT generation
- Implement `POST /auth/register` (admin-accessible only)
- Implement JWT middleware + `get_current_user` dependency
- Implement `require_admin` dependency
- Write `seed_users.py` to populate the 7 learners + admin
- Build Login page in React with form validation
- Connect to API, store JWT in Zustand
- Implement `ProtectedRoute` component with role checking
- Test: correct user reaches `/dashboard`, admin reaches `/admin`, others blocked

**Milestone:** All 7 users + admin can log in. Wrong credentials fail gracefully. Role-based routing works.

---

### Phase 3 — Task Submission Engine (Days 5–7)

**Goal:** Users can submit daily tasks and earn points. Business rules enforced.

Tasks:
- Implement `POST /tasks/submit` with:
  - Sunday lock (server-side day check)
  - One submission per user per day (UNIQUE constraint + 409 response)
  - Points calculation (sum of done tasks × 2)
- Implement `GET /tasks/today` to check if current user submitted today
- Implement `GET /tasks/history` for personal history
- Implement `GET /sprints/current` to identify active sprint
- Write `points_service.py` with total + per-sprint aggregation
- Implement `GET /users/me/stats` returning full points breakdown
- Write backend unit tests for all task logic

**Milestone:** A user submits tasks Monday–Saturday, blocked Sunday. Points accumulate correctly. Duplicate submission on same day returns 409.

---

### Phase 4 — User Dashboard UI (Days 8–11)

**Goal:** Beautiful, interactive user-facing dashboard matching the brand.

Tasks:
- Build `UserLayout` with header: logo, Arabic title "رحلة البزنس المرتب", "Hello [Name]" greeting
- Build `PointsRing` component with Framer Motion animation
- Build `TaskCard` component (3 cards: Daily / Sport / Contribution)
- Build submission flow: check if already submitted today → show done state or allow submission
- Build `SprintBar` component showing all 5 sprints with points earned vs max
- Apply Almoratab color system: teal `#1A4D4A` + gold `#C9982A` + cream `#FAF6EE`
- Implement Sunday lock UI (disabled state + message "Rest day — see you Monday!")
- Responsive layout (mobile-first)

**Milestone:** Full user journey works end-to-end. Points ring animates. Tasks can be submitted once. Sprint bars show real data.

---

### Phase 5 — Admin Control Panel (Days 12–15)

**Goal:** Admin has full visibility and can validate live attendance.

Tasks:
- Build `AdminPanel` page with leaderboard table sorted by points
- Build per-row mini progress bar (points/400)
- Build "Details →" links to per-user pages
- Build `UserDetail` page:
  - Sprint breakdown table (task pts, live pts, total, max)
  - Task history table (date × 3 tasks)
  - `ProgressChart` (Recharts LineChart) showing cumulative points over time
- Implement live session management:
  - `GET /admin/live-sessions` showing all sessions per sprint
  - `POST /admin/live-sessions/{session_id}/validate/{user_id}` to award 4 pts
  - Show validated state (green tick) vs not validated (button)
  - Prevent double-validation (409 response handled gracefully)

**Milestone:** Admin can view all users ranked by points. Clicking any user shows full analytics. Live attendance validation updates points in real time.

---

### Phase 6 — Polish, Testing & Deployment (Days 16–18)

**Goal:** Production-ready, tested, deployed application.

Tasks:
- Loading skeletons for all data-fetching states
- Error boundary + graceful error messages
- Toast notifications (success / error / info) with React Hot Toast
- Form validation feedback on login page
- Final design review: typography, spacing, responsiveness on mobile
- Write remaining backend tests (auth, tasks, admin endpoints)
- Environment variables audit (.env vs .env.example)
- Set up production Docker build (multi-stage builds)
- Deploy backend to Railway (or VPS with Docker)
- Deploy frontend to Vercel (or same VPS with Nginx)
- Configure production CORS, HTTPS, environment variables
- Smoke test all endpoints in production

**Milestone:** App is live, accessible via URL, all 7 users can log in and use it.

---

## 15. UI/UX Design System

The design is a direct evolution of the existing HTML project's visual identity.

### Color Tokens

```css
:root {
  --gold:        #C9982A;   /* Primary accent — points, highlights */
  --gold-light:  #E8BE5A;   /* Lighter gold for hover states */
  --gold-pale:   #F5EDD4;   /* Gold tint backgrounds */
  --teal:        #1A4D4A;   /* Dark teal — headers, primary dark */
  --teal-mid:    #246460;   /* Medium teal — secondary elements */
  --teal-light:  #2E7D79;   /* Light teal — hover, active states */
  --cream:       #FAF6EE;   /* Page background */
  --dark:        #0F2A28;   /* Near-black headers */
  --text:        #1C2B2A;   /* Body text */
  --muted:       #6B8280;   /* Secondary text */
  --border:      #D4C5A0;   /* Borders and dividers */
  --white:       #FFFFFF;
  --success:     #2E7D79;
  --error:       #B84040;
}
```

### Typography

```css
/* Headings */
font-family: 'Playfair Display', serif;     /* Brand title */
font-family: 'Cairo', sans-serif;           /* Arabic text */

/* Body */
font-family: 'Lato', 'Cairo', sans-serif;   /* All UI text */

/* Font sizes */
--text-xs:   11px;
--text-sm:   13px;
--text-base: 15px;
--text-lg:   18px;
--text-xl:   24px;
--text-2xl:  32px;
--text-hero: clamp(28px, 6vw, 48px);
```

### Component Visual Identity

| Component | Background | Border | Accent |
|-----------|-----------|--------|--------|
| Page header | Dark teal → teal gradient | None | Gold logo ring |
| Card | White | 1px `--border` | Gold left strip on active |
| Task card (checked) | Teal-50 | 1px teal | Gold checkmark |
| Task card (unchecked) | White | 1px gray | — |
| Submit button | Gold | None | White text, shadow on hover |
| Points ring track | Dark teal | — | — |
| Points ring fill | Gold | — | Animated |
| Sprint bar track | Gray-200 | — | — |
| Sprint bar fill | Teal → teal-light gradient | — | — |
| Admin table header | Teal-800 | — | Gold text |
| Progress bar (admin) | Gold | None | — |

---

## 16. Business Logic Rules

These rules are enforced **server-side** in the FastAPI backend. Frontend also implements them for UX, but the backend is the source of truth.

### Task Submission Rules

1. **Sunday lock:** Any submission on a Sunday (weekday == 6) → `403 Forbidden` with message `"Rest day — submissions are not allowed on Sundays."`
2. **One submission per day:** Each `(user_id, submission_date)` pair must be unique → `409 Conflict` with message `"You have already submitted tasks for today."`
3. **Must be within active sprint:** Submission date must fall within a sprint's `start_date` to `end_date` → `400 Bad Request` if no active sprint found for that date.
4. **Points are auto-calculated:** The backend calculates points from `(task1_done + task2_done + task3_done) * 2`. The client does not send points.
5. **Partial submission allowed:** A user can submit with 1, 2, or all 3 tasks done (earning 2, 4, or 6 pts). They cannot resubmit the same day to add more.

### Live Attendance Rules

1. **Admin-only:** Only users with `role == "admin"` can call the validate endpoint.
2. **One validation per user per session:** The `UNIQUE (user_id, live_session_id)` constraint prevents double-awarding → `409 Conflict`.
3. **Points are fixed:** Live attendance always awards exactly **4 points**. This is set by the backend, not the client.
4. **Session must exist:** Validation requires a valid `live_session_id` that exists in the database.

### Point Aggregation Rules

1. `total_points = SUM(task_submissions.points_earned) + SUM(live_attendance.points_awarded)` for a given user.
2. Points can never exceed 400 (the backend doesn't cap this, but the sprint and live structure mathematically prevents exceeding it if rules are followed).
3. The leaderboard is always sorted descending by `total_points`, ties broken alphabetically by name.

---

## 17. Deployment Plan

### Production Environment

| Service | Platform | Notes |
|---------|----------|-------|
| Frontend | Vercel | Auto-deploy from `main` branch |
| Backend | Railway | Docker container, always-on |
| Database | Railway PostgreSQL | Managed, backups enabled |
| Media/Static | Served by Vite build | Logo bundled in React app |

### Environment Variables (Production)

```env
# Backend (Railway)
DATABASE_URL=postgresql+asyncpg://...   # Railway provides this
SECRET_KEY=<64-char random string>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
FRONTEND_URL=https://almoratab.vercel.app
APP_ENV=production

# Frontend (Vercel)
VITE_API_URL=https://almoratab-backend.railway.app
```

### First Deployment Checklist

- [ ] PostgreSQL provisioned on Railway
- [ ] `DATABASE_URL` added to Railway backend env vars
- [ ] `alembic upgrade head` run in Railway backend (applies all migrations)
- [ ] `python seeds/seed_users.py` run to create 7 learners + admin
- [ ] Sprint dates configured in `sprints` table for the real training calendar
- [ ] Live session dates and titles configured in `live_sessions` table
- [ ] Frontend `VITE_API_URL` pointing to production backend
- [ ] CORS backend allowing `https://almoratab.vercel.app`
- [ ] HTTPS confirmed on both frontend and backend URLs
- [ ] Admin login tested in production
- [ ] All 7 users can log in with seeded credentials
- [ ] Task submission tested end-to-end in production
- [ ] Sunday lock confirmed working in production timezone

---

*Plan version 1.0 — رحلة البزنس المرتب*  
*Ready to build. Start with Phase 1.*
