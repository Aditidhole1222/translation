# 🚀 Quick Start Guide

## Absolute Beginner's Guide to Running This Project

### 📋 Prerequisites Checklist

- [ ] Python 3.11 installed ([Download](https://www.python.org/downloads/))
- [ ] Git installed ([Download](https://git-scm.com/downloads))
- [ ] Flutter installed (for mobile app) ([Install Guide](https://flutter.dev/docs/get-started/install))
- [ ] 10 GB free disk space
- [ ] Good internet connection (for downloading models)

---

## ⚡ 5-Minute Setup (Windows)

### Step 1: Download the Project

```powershell
# Navigate to desired location
cd C:\Users\YourName\Documents

# If you have the code, navigate to it
cd translation\backend
```

### Step 2: Install Python Dependencies

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Expected time:** 5-10 minutes

### Step 3: Get Datasets

Place these files in the `backend` folder:
- `german_to_english_120k_dataset.csv`
- `english_to_marathi_120k_dataset.csv`

**Note:** You should have these datasets for your B.Tech project.

### Step 4: Train Models (IMPORTANT!)

```powershell
# Train German to English (takes 8-12 hours on CPU)
python train_de_en.py

# Train English to Marathi (takes 8-12 hours on CPU)
python train_en_mr.py
```

☕ **Tip:** Run overnight! Training on CPU takes time.

### Step 5: Run the API

```powershell
# Quick start
python start.py

# OR manually
uvicorn app:app --host 0.0.0.0 --port 10000 --reload
```

### Step 6: Test the API

Open browser: http://localhost:10000/docs

Try the interactive API!

---

## 📱 Running Flutter App

### Step 1: Setup

```powershell
cd ..\frontend
flutter pub get
```

### Step 2: Update API URL

Edit `lib/services/api_service.dart`:

```dart
// For Android Emulator
static const String baseUrl = 'http://10.0.2.2:10000';

// For iOS Simulator
static const String baseUrl = 'http://localhost:10000';

// For Physical Device (replace with your computer's IP)
static const String baseUrl = 'http://192.168.1.100:10000';
```

**Find your IP:**
```powershell
ipconfig
# Look for IPv4 Address
```

### Step 3: Run App

```powershell
# Check connected devices
flutter devices

# Run on Android
flutter run

# Run on specific device
flutter run -d android
```

---

## 🧪 Testing the System

### Test 1: Text Translation

```powershell
curl -X POST http://localhost:10000/translate-text ^
  -H "Content-Type: application/json" ^
  -d "{\"german\": \"Ich lerne Deutsch.\"}"
```

**Expected Response:**
```json
{
  "german": "Ich lerne Deutsch.",
  "english": "I am learning German.",
  "marathi": "मी जर्मन शिकत आहे."
}
```

### Test 2: Speech Translation

1. Prepare a short German audio file (mp3, wav)
2. Open http://localhost:10000/docs
3. Click `/speech-translate`
4. Click "Try it out"
5. Upload your audio file
6. Click "Execute"

---

## ⚠️ Common First-Time Issues

### Issue 1: `command not found: python`

**Solution:**
```powershell
# Use python3 instead
python3 --version

# Or add Python to PATH
```

### Issue 2: `No module named 'torch'`

**Solution:**
```powershell
# Ensure virtual environment is activated
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue 3: Models not found

**Solution:**
```
You MUST train the models first!
python train_de_en.py
python train_en_mr.py
```

### Issue 4: Port 10000 already in use

**Solution:**
```powershell
# Use different port
uvicorn app:app --host 0.0.0.0 --port 8000

# Update Flutter app URL accordingly
```

---

## 🎯 What to Do Next?

### For Testing:
1. ✅ Test text translation with different German sentences
2. ✅ Record your own German audio
3. ✅ Test speech translation
4. ✅ Run evaluation script

### For Presentation:
1. ✅ Prepare demo German audio samples
2. ✅ Screenshot the results
3. ✅ Note the BLEU scores
4. ✅ Document any improvements made

### For Deployment:
1. ✅ Create GitHub repository
2. ✅ Push code (without datasets!)
3. ✅ Deploy to Render
4. ✅ Update Flutter app with production URL

---

## 📊 Checking Training Progress

While training, you'll see:

```
Epoch 1/3: 100%|████████| 12000/12000 [2:15:30<00:00]
Evaluation: 100%|█████████| 3000/3000 [0:15:20<00:00]
BLEU Score: 38.5
Saving checkpoint...
```

**Good signs:**
- ✅ BLEU score increases each epoch
- ✅ Loss decreases
- ✅ No error messages

**Bad signs:**
- ❌ BLEU score decreases
- ❌ Out of memory errors
- ❌ NaN loss values

---

## 💾 Saving Your Work

```powershell
# Create git repository
git init
git add .
git commit -m "Initial commit: B.Tech translation project"

# Push to GitHub
git remote add origin https://github.com/yourusername/translation-project.git
git push -u origin main
```

**Important:** Check `.gitignore` to ensure datasets aren't committed!

---

## 🆘 Getting Help

If stuck:

1. **Check error message carefully**
2. **Read README.md troubleshooting section**
3. **Search error on Google/StackOverflow**
4. **Check model files exist** in `models/` folder
5. **Verify all dependencies installed**

---

## ✅ Project Checklist

Before final submission:

- [ ] Both models trained and saved
- [ ] API runs without errors
- [ ] Flutter app connects to API
- [ ] Tested with German audio samples
- [ ] BLEU scores calculated
- [ ] Screenshots taken
- [ ] Code documented
- [ ] README updated with your info
- [ ] Deployed to Render (optional)
- [ ] Presentation prepared

---

## 🎓 For Your Report

Include:

1. **Architecture diagram** (from README)
2. **BLEU scores** (from evaluation)
3. **Sample translations** (screenshot from API)
4. **Training logs** (epoch results)
5. **Flutter app screenshots**
6. **Deployment URL** (if deployed)

---

## 🚀 Pro Tips

💡 **Training:** Use Google Colab with GPU for faster training (2-3 hours instead of 20!)

💡 **Testing:** Create a folder with 10-15 German audio samples for demos

💡 **Presentation:** Prepare both successful and failed examples to show understanding

💡 **Documentation:** Keep a log of BLEU scores and training times

💡 **Deployment:** Deploy at least 2 days before submission to handle issues

---

**Good luck with your B.Tech project! 🎓**
