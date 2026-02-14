# 📋 API Testing Guide

Quick reference for testing the translation API.

---

## 🔗 Base URLs

```
Local Development:  http://localhost:10000
Production (Render): https://your-app.onrender.com
```

---

## 🧪 Test Endpoints

### 1. Health Check

```bash
curl http://localhost:10000/health
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

### 2. Text Translation

#### Windows PowerShell:

```powershell
curl.exe -X POST http://localhost:10000/translate-text `
  -H "Content-Type: application/json" `
  -d '{\"german\": \"Guten Morgen!\"}'
```

#### Linux/Mac:

```bash
curl -X POST http://localhost:10000/translate-text \
  -H "Content-Type: application/json" \
  -d '{"german": "Guten Morgen!"}'
```

#### Python:

```python
import requests

response = requests.post(
    'http://localhost:10000/translate-text',
    json={'german': 'Guten Morgen!'}
)
print(response.json())
```

**Expected Response:**
```json
{
  "german": "Guten Morgen!",
  "english": "Good morning!",
  "marathi": "सुप्रभात!"
}
```

---

### 3. Speech Translation

#### Windows PowerShell:

```powershell
curl.exe -X POST http://localhost:10000/speech-translate `
  -F "audio_file=@C:\path\to\german_audio.mp3"
```

#### Linux/Mac:

```bash
curl -X POST http://localhost:10000/speech-translate \
  -F "audio_file=@/path/to/german_audio.mp3"
```

#### Python:

```python
import requests

with open('german_audio.mp3', 'rb') as f:
    files = {'audio_file': f}
    response = requests.post(
        'http://localhost:10000/speech-translate',
        files=files
    )
print(response.json())
```

**Expected Response:**
```json
{
  "german_text": "Guten Morgen! Wie geht es dir?",
  "english_text": "Good morning! How are you?",
  "marathi_text": "सुप्रभात! तू कसा आहेस?",
  "marathi_audio_url": "/audio/marathi_123456.mp3"
}
```

---

## 📝 Test Sentences

### Easy (Short)

| German | English | Marathi |
|--------|---------|---------|
| Hallo | Hello | नमस्कार |
| Danke | Thank you | धन्यवाद |
| Guten Morgen | Good morning | सुप्रभात |
| Wie geht's? | How are you? | कसे आहात? |

### Medium (Conversational)

```
Ich lerne Deutsch.
Das Wetter ist heute schön.
Wo ist der Bahnhof?
Ich möchte ein Glas Wasser.
```

### Hard (Complex)

```
Die deutsche Sprache ist eine der meistgesprochenen Sprachen in Europa.
Künstliche Intelligenz verändert unsere Welt.
```

---

## 🎤 Test Audio Files

### Creating Test Audio

#### Method 1: Google Translate TTS

1. Go to https://translate.google.com
2. Select German
3. Type sentence
4. Click speaker icon
5. Use browser's audio recording to save

#### Method 2: Online TTS

1. Visit https://ttsmp3.com
2. Select German language
3. Enter text
4. Download MP3

#### Method 3: Record Yourself

```python
# Using Python to create test audio
from gtts import gTTS

text = "Ich lerne Deutsch"
tts = gTTS(text=text, lang='de')
tts.save('test_german.mp3')
```

---

## 📊 Performance Testing

### Response Time Test

```python
import requests
import time

# Test text translation speed
start = time.time()
response = requests.post(
    'http://localhost:10000/translate-text',
    json={'german': 'Guten Morgen!'}
)
end = time.time()

print(f"Response time: {end - start:.2f} seconds")
print(f"Status: {response.status_code}")
print(f"Result: {response.json()}")
```

**Expected Performance:**
- Text translation: 1-3 seconds (CPU)
- Speech translation: 5-10 seconds (CPU)

---

## 🐛 Error Cases to Test

### 1. Empty Text

```bash
curl -X POST http://localhost:10000/translate-text \
  -H "Content-Type: application/json" \
  -d '{"german": ""}'
```

**Expected:** 400 Bad Request

---

### 2. Large File

```bash
# Upload file > 10 MB
curl -X POST http://localhost:10000/speech-translate \
  -F "audio_file=@large_file.mp3"
```

**Expected:** 400 Bad Request (File too large)

---

### 3. Wrong File Type

```bash
curl -X POST http://localhost:10000/speech-translate \
  -F "audio_file=@document.pdf"
```

**Expected:** 400 Bad Request (Invalid file type)

---

## 🔍 Validation Checklist

Test each scenario:

- [ ] Health check returns 200
- [ ] Simple German text translates correctly
- [ ] Complex German text translates correctly
- [ ] Audio file uploads successfully
- [ ] Marathi audio is generated
- [ ] Marathi audio can be downloaded
- [ ] Empty text returns error
- [ ] Large file returns error
- [ ] Wrong file type returns error
- [ ] API docs accessible at `/docs`

---

## 📈 Load Testing (Optional)

### Simple Load Test

```python
import requests
import concurrent.futures
import time

def translate(text):
    return requests.post(
        'http://localhost:10000/translate-text',
        json={'german': text}
    )

# Test with 10 concurrent requests
texts = ["Guten Morgen!"] * 10

start = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(translate, texts))
end = time.time()

print(f"Processed 10 requests in {end - start:.2f} seconds")
print(f"Success: {sum(1 for r in results if r.status_code == 200)}/10")
```

---

## 📱 Testing Flutter App

### With Android Emulator:

1. Start emulator
2. Start backend: `python start.py`
3. Run Flutter: `flutter run`
4. API URL should be: `http://10.0.2.2:10000`

### With Physical Device:

1. Connect device via USB
2. Enable USB debugging
3. Find computer's IP: `ipconfig` (Windows) or `ifconfig` (Linux/Mac)
4. Update API URL in `api_service.dart`: `http://192.168.1.X:10000`
5. Run: `flutter run`

**Test Scenarios:**

- [ ] Text translation works
- [ ] Can record audio
- [ ] Can upload audio file
- [ ] Translation results display
- [ ] Marathi audio plays
- [ ] Error messages show correctly
- [ ] Loading indicators work

---

## 🎓 For Demonstration

### Prepare Demo Set

Create a folder with:

1. **5 text examples** (easy to complex)
2. **3 audio files** (short, medium, long)
3. **Screenshots** of successful translations
4. **BLEU scores** from evaluation
5. **Response time** logs

### Demo Script

1. Show health check ✅
2. Translate simple text
3. Translate complex text
4. Upload audio file
5. Play Marathi output
6. Show BLEU scores
7. Demonstrate error handling

---

## 💡 Tips

✅ Test on fresh API restart for consistent results  
✅ Use Postman/Insomnia for easier API testing  
✅ Keep logs of successful tests for report  
✅ Test edge cases (empty, very long, special characters)  
✅ Document any failures and fixes

---

**Last Updated:** February 13, 2026
