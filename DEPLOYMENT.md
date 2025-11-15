# Employee Task Management - Render Deployment Guide

## Backend Deployment (FastAPI)

### Step 1: Push to GitHub
1. Create a new GitHub repository
2. Push your code:
```bash
cd "C:\Users\Nithishkumar\Desktop\ProU"
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Step 2: Deploy Backend on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:

**Settings:**
- **Name:** `employee-task-api` (or any name)
- **Region:** Choose closest to you
- **Branch:** `main`
- **Root Directory:** `backend`
- **Runtime:** `Python 3`
- **Build Command:** `chmod +x build.sh && ./build.sh`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Environment Variables:**
Click "Advanced" and add:
- Key: `PYTHON_VERSION`, Value: `3.11.0`
- Key: `MONGODB_URI`, Value: `mongodb+srv://pugazhandhik26_db_user:uBK178tMc2B9tHYc@cluster0.viwykuy.mongodb.net/?retryWrites=true&w=majority`
- Key: `DATABASE_NAME`, Value: `employee_task_db`

5. Click **"Create Web Service"**
6. Wait for deployment (5-10 minutes)
7. Your API will be available at: `https://employee-task-api.onrender.com`

### Step 3: Update CORS in Backend

After deployment, note your frontend URL and update CORS settings if needed.

---

## Frontend Deployment (Static Site)

### Option A: Deploy on Render (Static Site)

1. In Render Dashboard, click **"New +"** → **"Static Site"**
2. Connect the same GitHub repository
3. Configure:

**Settings:**
- **Name:** `employee-task-frontend`
- **Branch:** `main`
- **Root Directory:** `frontend`
- **Build Command:** (leave empty)
- **Publish Directory:** `.`

4. Click **"Create Static Site"**
5. Your frontend will be at: `https://employee-task-frontend.onrender.com`

### Option B: Deploy on Netlify (Easier for static sites)

1. Go to [Netlify](https://www.netlify.com/)
2. Drag & drop your `frontend` folder
3. Site will be live instantly

### Option C: Deploy on Vercel

1. Go to [Vercel](https://vercel.com/)
2. Import your GitHub repository
3. Set **Root Directory:** `frontend`
4. Deploy

---

## Step 4: Update Frontend API URL

After backend is deployed, update the frontend to use the deployed API:

**In `frontend/app.js`, change:**
```javascript
const API_URL = 'https://employee-task-api.onrender.com';  // Replace with your actual Render URL
```

Then redeploy the frontend.

---

## Step 5: Seed Initial Data (Optional)

After backend is deployed, you can seed data by:

1. **SSH into Render:**
   - In Render Dashboard → Your service → Shell tab
   - Run: `python seed_data.py`

2. **OR uncomment the seed line in `build.sh`:**
   - This will reset data on every deployment

---

## Environment Variables (Optional)

For better security, update `backend/app/config.py` to use environment variables:

```python
import os
from motor.motor_asyncio import AsyncIOMotorClient
from functools import lru_cache


class Settings:
    MONGODB_URI: str = os.getenv(
        "MONGODB_URI",
        "mongodb+srv://pugazhandhik26_db_user:uBK178tMc2B9tHYc@cluster0.viwykuy.mongodb.net/?retryWrites=true&w=majority"
    )
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "employee_task_db")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()


def get_database():
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    return client[settings.DATABASE_NAME]
```

---

## Quick Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Backend deployed on Render
- [ ] Environment variables configured
- [ ] Backend URL noted (e.g., `https://employee-task-api.onrender.com`)
- [ ] Frontend `app.js` updated with backend URL
- [ ] Frontend deployed (Render/Netlify/Vercel)
- [ ] CORS configured to allow frontend domain
- [ ] Test all CRUD operations
- [ ] Seed initial data (optional)

---

## Free Tier Notes

**Render Free Tier:**
- Services spin down after 15 minutes of inactivity
- First request after inactivity takes ~30 seconds (cold start)
- Upgrade to paid plan for always-on service

**MongoDB Atlas:**
- Free tier: 512 MB storage
- Sufficient for development/small projects

---

## Troubleshooting

**CORS Errors:**
Update `backend/main.py` to include your frontend URL:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://employee-task-frontend.onrender.com"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Backend not starting:**
- Check logs in Render Dashboard
- Verify environment variables
- Ensure `requirements.txt` is correct

**Database connection fails:**
- Verify MongoDB Atlas allows connections from anywhere (0.0.0.0/0)
- Check MongoDB credentials

---

Your app is now live! 🚀
