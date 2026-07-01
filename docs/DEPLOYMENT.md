# Production Deployment Staging Checklist 🚀

Follow this guide to deploy the **Chronic Patient Memory System** to production with **FastAPI on Render.com** and **React on Vercel**.

---

## ── Phase 1: Deploying the Backend on Render ─────────────────────────

Render is ideal for the FastAPI backend because it supports persistent storage disks needed to retain database entries, PDF uploads, and ChromaDB vector files.

### Step 1.1: Deploy Using Render Blueprints
1. Push your repository to GitHub.
2. Sign in to your **Render Dashboard** and click **New** → **Blueprint**.
3. Link your GitHub repository.
4. Render will read the `render.yaml` file in the root folder and automatically configure:
   - A Python Web Service.
   - A 1GB persistent disk mapped to `/var/data` to prevent data loss when the web service restarts or updates.
5. In the blueprint variables page, configure the following:
   - **`GEMINI_API_KEY`**: Paste your production Google Gemini API key.
   - **`SECRET_KEY`**: Generate a strong secret key for hashing JWTs. (Run `python -c "import secrets; print(secrets.token_hex(32))"` to generate one).

### Step 1.2: Check Deployment Health
1. Once the build completes, copy your Render Web Service URL (e.g., `https://chronic-patient-memory-system-backend.onrender.com`).
2. Visit the health check URL in your browser: `https://<your-app>.onrender.com/health`.
3. If it returns `{"status":"ok"}`, the backend is operational and databases have initialized.

---

## ── Phase 2: Deploying the Frontend on Vercel ───────────────────────

Vercel is optimized for building and serving Vite + React static assets globally.

### Step 2.1: Deploy on Vercel
1. Log in to your Vercel Dashboard and click **Add New** → **Project**.
2. Import your GitHub repository.
3. In the configure project screen:
   - **Framework Preset**: Select **Vite**.
   - **Root Directory**: Select `frontend`.
4. Expand **Environment Variables** and add:
   - **Key**: `VITE_API_BASE_URL`
   - **Value**: `https://<your-backend-render-app>.onrender.com` (Your backend Render URL without trailing slash).
5. Click **Deploy**.

---

## ── Phase 3: Securing CORS & Origin Restrictions ────────────────────

For security, the production backend should only allow CORS requests originating from your production Vercel frontend.

1. Go to your **Render Web Service Dashboard**.
2. Click **Environment** on the left menu.
3. Locate the `ALLOWED_ORIGINS` variable.
4. Replace `http://localhost:5173,http://localhost:3000` with your production Vercel URL (e.g., `https://chronic-patient-memory-system.vercel.app`).
5. Save changes. Render will automatically redeploy the backend with the new security boundaries.

---

## ── Phase 4: Scaling to PostgreSQL (Production Database) ───────────

While SQLite on a persistent disk is highly reliable, you can easily scale the backend database to PostgreSQL:

1. Create a **PostgreSQL Database** on Render (free tier or paid).
2. Copy the database's **Internal Connection URI** (e.g., `postgresql://user:password@host:port/dbname`).
3. In your Render Web Service Environment variables list:
   - Update **`DATABASE_URL`** to your PostgreSQL URI.
4. Save variables. The backend will redeploy, automatically run database initialization schemas on PostgreSQL, and boot up. **Zero backend code changes are required.**
