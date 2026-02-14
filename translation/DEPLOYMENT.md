# ☁️ Render Deployment Checklist

Complete guide for deploying to Render cloud platform.

---

## 📋 Pre-Deployment Checklist

### 1. Code Preparation

- [ ] All training completed
- [ ] Models saved in `backend/models/`
- [ ] Models size < 500 MB total
- [ ] `requirements.txt` updated
- [ ] `Dockerfile` configured
- [ ] `.gitignore` configured
- [ ] Datasets excluded from git

### 2. Model Optimization

```python
# Optional: Compress models before deployment
import torch

# Load model
model = MarianMTModel.from_pretrained('./models/de_en_finetuned')

# Save with optimization
model.save_pretrained(
    './models/de_en_finetuned_optimized',
    safe_serialization=True  # Use safer format
)
```

### 3. Test Locally

```bash
# Build Docker image
docker build -t translation-api .

# Run container
docker run -p 10000:10000 translation-api

# Test
curl http://localhost:10000/health
```

---

## 🚀 Deployment Steps

### Step 1: Create GitHub Repository

```bash
# Initialize git
cd translation
git init

# Add files
git add .

# Commit
git commit -m "Initial commit: AI Translation System"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/translation-project.git
git branch -M main
git push -u origin main
```

**Important:** Verify datasets (`.csv` files) are NOT pushed!

---

### Step 2: Sign Up for Render

1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub
4. Authorize Render to access repositories

---

### Step 3: Create Web Service

1. **Click "New +"** → Select "Web Service"

2. **Connect Repository**
   - Select your GitHub repository
   - Click "Connect"

3. **Configure Service**

   | Setting | Value |
   |---------|-------|
   | Name | `multilingual-translation-api` |
   | Region | Oregon (or closest) |
   | Branch | `main` |
   | Root Directory | `backend` |
   | Runtime | `Python 3` |
   | Build Command | `pip install -r requirements.txt` |
   | Start Command | `uvicorn app:app --host 0.0.0.0 --port 10000` |
   | Plan | `Free` |

4. **Environment Variables** (Click "Add Environment Variable")

   ```
   PYTHON_VERSION = 3.11.0
   PORT = 10000
   ```

5. **Advanced Settings**

   ```
   Health Check Path: /health
   Auto-Deploy: Yes
   ```

6. Click **"Create Web Service"**

---

### Step 4: Monitor Deployment

You'll see build logs:

```
==> Cloning from GitHub...
==> Installing dependencies...
Collecting torch==2.1.0...
Collecting transformers==4.35.2...
✓ Successfully installed dependencies

==> Starting application...
🚀 Starting Multilingual Translation API
🔄 Loading model from ./models/de_en_finetuned...
✓ Model loaded on cpu
✓ All models loaded successfully!
🌐 API is ready to serve requests

==> Your service is live! 🎉
https://multilingual-translation-api.onrender.com
```

**Expected Time:** 10-15 minutes

---

### Step 5: Verify Deployment

```bash
# Test health endpoint
curl https://YOUR_APP_NAME.onrender.com/health

# Test translation
curl -X POST https://YOUR_APP_NAME.onrender.com/translate-text \
  -H "Content-Type: application/json" \
  -d '{"german": "Hallo Welt"}'
```

**Expected Response:**
```json
{
  "status": "healthy",
  "translation_model": true,
  "speech_model": true
}
```

---

## ⚙️ Configuration Files

### render.yaml (Optional)

Already created in `backend/render.yaml`:

```yaml
services:
  - type: web
    name: multilingual-translation-api
    env: python
    region: oregon
    plan: free
    branch: main
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn app:app --host 0.0.0.0 --port 10000"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: PORT
        value: 10000
    healthCheckPath: /health
```

### Dockerfile

Already created in `backend/Dockerfile`

---

## 🔧 Troubleshooting

### Issue 1: Build Fails - Dependency Error

```
ERROR: Could not find a version that satisfies the requirement torch==2.1.0
```

**Solution:**
```txt
# In requirements.txt, change to:
torch==2.1.0+cpu
# Or
torch>=2.0.0
```

---

### Issue 2: Models Not Found

```
FileNotFoundError: ./models/de_en_finetuned
```

**Solution:**
```bash
# Ensure models are committed to git
git add models/
git commit -m "Add trained models"
git push
```

---

### Issue 3: Out of Memory

```
Killed - Out of Memory
```

**Solution:**

1. **Reduce model size:**
   ```python
   # Use smaller Whisper model in speech_module.py
   WHISPER_MODEL_NAME = "tiny"  # Instead of "base"
   ```

2. **Optimize loading:**
   ```python
   # In app.py, lazy load models
   model = MarianMTModel.from_pretrained(
       model_path,
       low_cpu_mem_usage=True
   )
   ```

3. **Upgrade plan** (if budget allows)

---

### Issue 4: Slow Cold Starts

```
First request takes 30+ seconds
```

**Expected:** Render Free tier spins down after 15 min inactivity

**Solutions:**
- Accept cold starts (free tier limitation)
- Implement warming script (ping every 10 min)
- Upgrade to paid plan

**Warming Script:**
```python
# keep_alive.py
import requests
import time

while True:
    try:
        requests.get('https://your-app.onrender.com/health')
        print(f"Pinged at {time.ctime()}")
    except:
        pass
    time.sleep(600)  # Every 10 minutes
```

---

### Issue 5: Audio Upload Fails

```
413 Request Entity Too Large
```

**Solution:**

Render has request size limits. Add to `app.py`:

```python
from fastapi import FastAPI

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    max_age=3600,
)

# Limit request size
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB instead of 10 MB
```

---

## 📱 Update Flutter App

After successful deployment:

1. **Copy Render URL:**
   ```
   https://multilingual-translation-api.onrender.com
   ```

2. **Update `api_service.dart`:**
   ```dart
   class ApiService {
     static const String baseUrl = 
       'https://multilingual-translation-api.onrender.com';
     // ...
   }
   ```

3. **Rebuild Flutter app:**
   ```bash
   cd frontend
   flutter clean
   flutter pub get
   flutter build apk  # For Android
   ```

---

## 🔒 Security Best Practices

### 1. Environment Variables

For sensitive data:

```bash
# In Render dashboard, add:
SECRET_KEY=your-secret-key
API_KEY=your-api-key
```

Access in code:
```python
import os
SECRET_KEY = os.getenv('SECRET_KEY')
```

### 2. CORS Configuration

In production, restrict origins:

```python
# app.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-flutter-app.com",
        "http://localhost:*"  # For testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. Rate Limiting

Install:
```bash
pip install slowapi
```

Add to `app.py`:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/translate-text")
@limiter.limit("10/minute")  # Max 10 requests per minute
async def translate_text(...):
    # ...
```

---

## 📊 Monitoring

### Built-in Render Monitoring

1. **Logs:** View in Render dashboard
2. **Metrics:** CPU, Memory usage
3. **Events:** Deployment history

### Custom Logging

Add to `app.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.post("/translate-text")
async def translate_text(request: TextTranslationRequest):
    logger.info(f"Translation request: {request.german[:50]}")
    # ... rest of code
    logger.info(f"Translation completed")
```

---

## 💰 Cost Optimization (Free Tier)

### Free Tier Limits

- **750 hours/month** of runtime
- **512 MB RAM**
- **0.1 CPU**
- Spins down after 15 min inactivity

### Staying in Free Tier

✅ Accept spin-down (cold starts)  
✅ Use smaller models  
✅ Optimize memory usage  
✅ Implement caching  
✅ Compress responses

### When to Upgrade

Consider paid plan if:
- Need 24/7 uptime
- Handle high traffic
- Require more RAM/CPU
- Want faster responses

**Starter Plan:** $7/month
- No spin-down
- 512 MB RAM
- Better performance

---

## ✅ Post-Deployment Checklist

After deployment:

- [ ] Health endpoint accessible
- [ ] Text translation works
- [ ] Speech translation works
- [ ] Audio download works
- [ ] Flutter app connected
- [ ] Error handling works
- [ ] Logs are readable
- [ ] Performance acceptable
- [ ] API docs accessible (`/docs`)
- [ ] SSL certificate active (HTTPS)

---

## 🔄 Continuous Deployment

### Auto-Deploy on Git Push

Render automatically deploys when you push to `main`:

```bash
# Make changes
git add .
git commit -m "Optimize model loading"
git push

# Render automatically:
# 1. Detects push
# 2. Rebuilds application
# 3. Deploys new version
# 4. Runs health check
```

### Manual Deploy

In Render dashboard:
1. Click "Manual Deploy"
2. Select branch
3. Click "Deploy"

---

## 📈 Scaling Strategy

### Phase 1: Free Tier (Current)
- Single instance
- CPU-only inference
- Best for testing/demo

### Phase 2: Paid Tier
- Upgrade to Starter plan
- Better performance
- No cold starts

### Phase 3: Production
- Use Standard plan
- Multiple instances
- Load balancing
- GPU support (custom)

---

## 🎓 For Your Project Report

Include:

1. **Deployment URL**
   ```
   https://multilingual-translation-api.onrender.com
   ```

2. **Deployment Screenshot**
   - Render dashboard
   - Service running status
   - Build logs

3. **Performance Metrics**
   - Response times
   - Uptime
   - Request count

4. **Architecture Diagram**
   - Show cloud deployment
   - Flutter → API → Models

---

## 📞 Support

**Render Documentation:** https://render.com/docs  
**Render Community:** https://community.render.com  
**Status Page:** https://status.render.com

---

## 🎯 Quick Commands Reference

```bash
# View logs
render logs -t <service-name>

# Restart service
render service restart <service-name>

# Check status
curl https://your-app.onrender.com/health

# Test translation
curl -X POST https://your-app.onrender.com/translate-text \
  -H "Content-Type: application/json" \
  -d '{"german": "Test"}'
```

---

**Good luck with deployment! 🚀**

Remember: First deployment always takes longest. Subsequent deployments are faster!

