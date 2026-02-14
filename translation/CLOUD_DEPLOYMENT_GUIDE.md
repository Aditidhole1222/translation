# Deployment to Render.com - FREE Forever!

## Why Render instead of Ngrok Free?

✅ **Permanent URL** - Never changes: `https://yourapp.onrender.com`
✅ **Always Online** - Runs 24/7, no manual start needed
✅ **One-time APK** - Build once, works forever
✅ **FREE** - Completely free tier available
❌ **Downside** - First request takes 30-50 seconds if idle (wakes from sleep)

---

## Step 1: Prepare Backend for Deployment

Create `backend/requirements.txt`:

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
transformers>=4.40.0
sentencepiece
openai-whisper
gtts
python-multipart
SpeechRecognition
torch --index-url https://download.pytorch.org/whl/cpu
```

**Note:** Using CPU-only PyTorch for free tier compatibility

---

## Step 2: Create Start Script

Create `backend/start.sh`:

```bash
#!/bin/bash
export KMP_DUPLICATE_LIB_OK=TRUE
uvicorn app:app --host 0.0.0.0 --port $PORT
```

---

## Step 3: Deploy to Render

1. **Push to GitHub:**
   ```powershell
   cd C:\Users\mohit\translation\backend
   git init
   git add .
   git commit -m "Backend deployment"
   git remote add origin https://github.com/YOUR-USERNAME/translation-backend.git
   git push -u origin main
   ```

2. **Create Render Account:**
   - Go to: https://render.com/register
   - Sign up with GitHub

3. **Create Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Select `translation-backend` repo
   - Fill in:
     * **Name:** `translation-api`
     * **Region:** Choose closest to India (Singapore)
     * **Branch:** `main`
     * **Root Directory:** Leave blank (or `backend` if repo has both)
     * **Runtime:** `Python 3`
     * **Build Command:** `pip install -r requirements.txt`
     * **Start Command:** `bash start.sh`
     * **Plan:** `Free`

4. **Add Environment Variables:**
   - Click "Environment" tab
   - Add: `KMP_DUPLICATE_LIB_OK` = `TRUE`

5. **Deploy:**
   - Click "Create Web Service"
   - Wait 15-20 minutes for first deployment
   - Your URL: `https://translation-api.onrender.com`

---

## Step 4: Update Flutter App ONCE

Edit `frontend/lib/services/api_service.dart`:

```dart
static const String baseUrl = 'https://translation-api.onrender.com';
```

Build APK **ONE TIME**:
```powershell
cd frontend
flutter build apk --release
```

**Share this APK - it works FOREVER!** No more rebuilding! 🎉

---

## Step 5: Upload Your Models to Render

Your fine-tuned models are ~200MB. Free tier has limited storage, so options:

**Option A: Include in Git (if < 500MB total)**
- Add models to git: `git add models/`
- Push to GitHub
- Render will download them

**Option B: Use Cloud Storage (Recommended)**
- Upload models to Google Drive
- Get direct download links
- Backend downloads on startup:

```python
# In app.py startup
import requests
import zipfile

def download_models():
    if not os.path.exists('./models/de_en_finetuned_10k'):
        print("Downloading models...")
        # Download from Google Drive or Dropbox
        # Extract to ./models/
```

---

## Render.com Free Tier Details

**What's Included:**
- 750 hours/month (plenty for 24/7)
- 512MB RAM (enough for CPU inference)
- Auto-sleep after 15 mins inactivity
- HTTPS enabled by default

**Limitations:**
- Sleeps after 15 min idle → first request takes 30-50 sec to wake
- CPU-only (no GPU)
- 512MB RAM (works fine for your models)

**Perfect for:**
- B.Tech project demos
- Small user base (< 100 users)
- Portfolio/resume projects

---

## Alternative: Railway.app

Similar to Render, also has free tier:
- https://railway.app
- $5 free credit per month
- Better performance than Render free
- Setup similar to above

---

## Comparison Table

| Feature | Free Ngrok | Paid Ngrok | Render Free | Railway |
|---------|-----------|-----------|-------------|---------|
| Cost | FREE | $8/mo | FREE | $5 credit |
| Permanent URL | ❌ | ✅ | ✅ | ✅ |
| Manual Start | ✅ Yes | ⚠️ Sometimes | ❌ No | ❌ No |
| Always Online | ❌ | ✅ | ✅ | ✅ |
| Cold Start | N/A | Fast | 30-50s | ~10s |
| Rebuild APK | Every time | Once | Once | Once |

---

## My Recommendation for B.Tech Project

**Use Render.com (Free)** because:

1. ✅ **Zero cost** - Important for students
2. ✅ **Permanent URL** - Build APK once
3. ✅ **Professional** - Better for project report/resume
4. ✅ **Always accessible** - Examiners can test anytime
5. ⚠️ **Sleep delay** acceptable for academic project

**Setup time:** 30-45 minutes (one-time)
**Maintenance:** ZERO - runs automatically

---

## For Immediate Testing (Today)

If you need to demo RIGHT NOW:

**Option: Same WiFi Network**

1. Find your PC's local IP:
   ```powershell
   ipconfig
   # Look for IPv4 Address: 192.168.x.x
   ```

2. Update app:
   ```dart
   static const String baseUrl = 'http://192.168.x.x:10000';
   ```

3. Build APK:
   ```powershell
   flutter build apk --release
   ```

**Limitation:** Only works when phone and PC on SAME WiFi.

---

## What I Suggest You Do

**Today:** Use WiFi method for testing (5 minutes)
**This Week:** Deploy to Render for permanent solution (45 minutes)

Would you like me to help you deploy to Render.com right now?
