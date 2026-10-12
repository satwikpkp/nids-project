# Adaptive Lightweight NIDS - Complete Deployment Guide

This guide walks you through deploying the **FastAPI Backend on Render** and the **React Dashboard on Vercel**.

---

## Part 1: Push Code to GitHub

Both Render and Vercel connect directly to your GitHub repository for continuous deployment.

1. In PowerShell, open the project directory:
   ```powershell
   cd "d:\ids project"
   git init
   git add .
   git commit -m "Complete Adaptive Lightweight NIDS with ML pipeline, Auth, and SOC Dashboard"
   ```
2. Create a new repository on [GitHub](https://github.com/new) (e.g. named `nids-project`).
3. Link and push your code:
   ```powershell
   git branch -M main
   git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/nids-project.git
   git push -u origin main
   ```

---

## Part 2: Deploy Backend to Render

1. Log in to **[Render](https://dashboard.render.com/)**.
2. Click **New +** -> **Web Service**.
3. Select **Build and deploy from a Git repository** and connect your `nids-project` repo.
4. Configure the Web Service settings:
   - **Name**: `nids-backend` (or your preferred name)
   - **Region**: Choose the closest region (e.g., Singapore, Frankfurt, Oregon)
   - **Branch**: `main`
   - **Root Directory**: *(leave blank)*
   - **Runtime**: `Python 3`
   - **Build Command**:
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command**:
     ```bash
     uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
     ```
   - **Instance Type**: `Free`
5. Under **Environment Variables**, add:
   - `PYTHON_VERSION` = `3.12.2`
   - `SECRET_KEY` = *(generate any random 32-character string)*
6. Click **Create Web Service**.
7. Once Render finishes deploying, copy your backend public URL (e.g., `https://nids-backend.onrender.com`).
   - Test it by opening `https://nids-backend.onrender.com/docs` in your browser.

---

## Part 3: Deploy Frontend to Vercel

1. Log in to **[Vercel](https://vercel.com/)**.
2. Click **Add New...** -> **Project**.
3. Import your `nids-project` repository.
4. In the project configuration screen:
   - **Framework Preset**: `Vite`
   - **Root Directory**: Click **Edit** and select `frontend` (Important!).
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Expand **Environment Variables** and add:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://<YOUR_RENDER_SERVICE_URL>/api/v1` (e.g., `https://nids-backend.onrender.com/api/v1`)
6. Click **Deploy**.
7. In ~1 minute, Vercel will provide your production URL (e.g. `https://nids-dashboard.vercel.app`).

---

## Part 4: Final Verification

1. Open your live Vercel URL.
2. Sign in using the default security credentials:
   - **Email**: `admin@soc.defense`
   - **Password**: `Admin@123456`
3. Click **Simulate Flow** on the top right to verify live classification and WebSocket telemetry streaming across Render and Vercel!
