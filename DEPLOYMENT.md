# 🚀 Production Deployment Guide

This guide explains how to deploy the project using **Supabase** (Database), **Render** (Backend), and **Vercel/Netlify** (Frontend).

---

## 1. Database (Supabase)
1. Create a project at [supabase.com](https://supabase.com).
2. Go to **Project Settings > Database**.
3. Find the **Connection string** section.
4. Select **URI** and copy the string (it looks like `postgresql://postgres.[ID]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:5432/postgres`).
5. **CRUCIAL:** For SQLAlchemy (Async), change `postgresql://` to `postgresql+asyncpg://`.

---

## 2. Backend (Render)
1. Sign up at [render.com](https://render.com) and connect your GitHub.
2. Click **New > Web Service**.
3. Select your repository.
4. **Settings:**
   - **Environment:** `Python 3`
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port 10000`
5. **Environment Variables:** Add the following:
   - `DATABASE_URL`: Your Supabase URI (with `+asyncpg`)
   - `SECRET_KEY`: A long random string (e.g., `openssl rand -hex 32`)
   - `ALGORITHM`: `HS256`
   - `APP_ENV`: `production`
   - `FRONTEND_URL`: The URL of your Vercel/Netlify app (e.g., `https://almoratab.vercel.app`)

### 🛠 Running Migrations & Seeding on Render:
Once the service is live, go to the **Shell** tab on Render and run:
```bash
alembic upgrade head
python seeds/seed_users.py
```

---

## 3. Frontend (Vercel or Netlify)
### Option A: Vercel
1. Connect GitHub to [vercel.com](https://vercel.com).
2. New Project > Select Repo.
3. **Framework Preset:** `Vite`.
4. **Root Directory:** `frontend`.
5. **Environment Variables:**
   - `VITE_API_URL`: Your Render Web Service URL (e.g., `https://almoratab-api.onrender.com`)

### Option B: Netlify
1. Connect GitHub to [netlify.com](https://app.netlify.com).
2. Import from GitHub > Select Repo.
3. **Base directory:** `frontend`
4. **Build command:** `npm run build`
5. **Publish directory:** `dist`
6. **Environment Variables:**
   - `VITE_API_URL`: Your Render URL.

---

## 🔒 Security Reminders
1. **CORS:** Ensure the `FRONTEND_URL` in your Render environment variables matches your actual frontend domain exactly (no trailing slash).
2. **Secure Cookies:** Setting `APP_ENV=production` automatically enables `Secure` and `SameSite=None` flags for your JWT refresh cookies, which is required for HTTPS.

