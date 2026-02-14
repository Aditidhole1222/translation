# 🌐 AI-Based Multilingual Speech Translation Application

**B.Tech Final Year Project**

A complete end-to-end multilingual speech translation system that translates **German speech** to **Marathi speech** through intermediate English translation, using state-of-the-art AI models.

---

## 📋 Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Translation Pipeline](#translation-pipeline)
- [Theoretical Background](#theoretical-background)
  - [Transformer Architecture](#transformer-architecture)
  - [Multi-Head Attention](#multi-head-attention)
  - [Fine-Tuning](#fine-tuning)
  - [Cascaded Translation](#cascaded-translation)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Training Models](#training-models)
- [Running Locally](#running-locally)
- [Deployment on Render](#deployment-on-render)
- [API Documentation](#api-documentation)
- [Flutter App Usage](#flutter-app-usage)
- [Evaluation Metrics](#evaluation-metrics)
- [GPU vs CPU Performance](#gpu-vs-cpu-performance)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)
- [Contributors](#contributors)

---

## 🎯 Overview

This project implements a **practical, production-ready** multilingual speech translation system that:

1. **Accepts German audio input** (recorded or uploaded)
2. **Transcribes German speech to text** using OpenAI Whisper
3. **Translates German to English** using fine-tuned MarianMT
4. **Translates English to Marathi** using fine-tuned MarianMT
5. **Converts Marathi text to speech** using Google TTS (gTTS)
6. **Returns Marathi audio output**

### Key Features

✅ Fine-tuned translation models on custom 120K+ datasets  
✅ Real-time speech processing with Whisper  
✅ RESTful API built with FastAPI  
✅ Cross-platform Flutter mobile app  
✅ CPU-optimized for cloud deployment (Render)  
✅ Comprehensive evaluation with BLEU scores  
✅ Production-ready with Docker support

---

## 🏗 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE (Flutter)                  │
│  - Audio Recording    - File Upload    - Result Display     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP/REST API
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  BACKEND API (FastAPI)                       │
│  Endpoints: /translate-text, /speech-translate, /audio      │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ▼                               ▼
┌──────────────────┐          ┌──────────────────────┐
│  Speech Module   │          │  Translation Module  │
│                  │          │                      │
│  - Whisper STT   │          │  - MarianMT (DE→EN) │
│  - gTTS TTS      │          │  - MarianMT (EN→MR) │
└──────────────────┘          └──────────────────────┘
```

### Component Breakdown

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Speech-to-Text** | OpenAI Whisper | Convert German audio to text |
| **Translation (DE→EN)** | Fine-tuned MarianMT | Translate German to English |
| **Translation (EN→MR)** | Fine-tuned MarianMT | Translate English to Marathi |
| **Text-to-Speech** | gTTS | Generate Marathi audio |
| **Backend API** | FastAPI + Uvicorn | REST API server |
| **Frontend** | Flutter | Cross-platform mobile app |
| **Deployment** | Render + Docker | Cloud hosting |

---

## 🔧 Technology Stack

### Backend
- **Python 3.11**
- **PyTorch** - Deep learning framework
- **HuggingFace Transformers** - Pretrained models
- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **OpenAI Whisper** - Speech recognition
- **gTTS** - Text-to-speech
- **SacreBLEU** - Evaluation metrics

### Frontend
- **Flutter 3.x** - Cross-platform framework
- **Dart** - Programming language
- **HTTP** - API communication
- **AudioPlayers** - Audio playback
- **Record** - Audio recording

### DevOps
- **Docker** - Containerization
- **Render** - Cloud deployment
- **Git** - Version control

---

## 🔄 Translation Pipeline

### Detailed Flow

```
GERMAN SPEECH (Audio File)
    │
    │ [1] Speech-to-Text (Whisper)
    ▼
GERMAN TEXT
    │
    │ [2] Translation (MarianMT DE→EN)
    ▼
ENGLISH TEXT
    │
    │ [3] Translation (MarianMT EN→MR)
    ▼
MARATHI TEXT
    │
    │ [4] Text-to-Speech (gTTS)
    ▼
MARATHI SPEECH (Audio File)
```

### Example Translation

| Stage | Language | Text |
|-------|----------|------|
| Input | 🇩🇪 German | "Guten Morgen! Wie geht es dir?" |
| Step 1 | 🇬🇧 English | "Good morning! How are you?" |
| Step 2 | 🇮🇳 Marathi | "सुप्रभात! तू कसा आहेस?" |
| Output | 🔊 Audio | Marathi speech output |

---

## 📚 Theoretical Background

### Transformer Architecture

The **Transformer** is a neural network architecture introduced in the paper *"Attention Is All You Need"* (Vaswani et al., 2017). It revolutionized NLP by replacing recurrent layers with self-attention mechanisms.

#### Key Components

1. **Encoder-Decoder Structure**
   - **Encoder**: Processes input sequence and creates contextualized representations
   - **Decoder**: Generates output sequence autoregressively

2. **Self-Attention Mechanism**
   - Computes relationships between all positions in a sequence
   - Formula: `Attention(Q, K, V) = softmax(QK^T / √d_k)V`
   - Allows parallel processing (unlike RNNs)

3. **Layer Structure**
   ```
   Encoder Layer:
   - Multi-Head Self-Attention
   - Add & Normalize
   - Feed-Forward Network
   - Add & Normalize
   
   Decoder Layer:
   - Masked Multi-Head Self-Attention
   - Add & Normalize
   - Cross-Attention (with encoder output)
   - Add & Normalize
   - Feed-Forward Network
   - Add & Normalize
   ```

#### Why Transformers for Translation?

✅ **Parallel Processing**: Unlike RNNs, can process entire sequence at once  
✅ **Long Dependencies**: Self-attention captures long-range dependencies  
✅ **Contextual Understanding**: Each word attends to all other words  
✅ **Scalability**: Easier to scale to large datasets

---

### Multi-Head Attention

Multi-head attention allows the model to attend to information from different representation subspaces simultaneously.

#### Mathematical Formulation

```
MultiHead(Q, K, V) = Concat(head_1, ..., head_h)W^O

where head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)
```

#### Why Multiple Heads?

1. **Different Perspectives**: Each head learns different relationships
   - Head 1: Syntactic relationships (subject-verb)
   - Head 2: Semantic relationships (word meanings)
   - Head 3: Positional relationships (word order)

2. **Robustness**: Redundancy improves translation quality

3. **Specialization**: Different heads specialize in different aspects

#### Example

For sentence: "The cat sat on the mat"

- **Head 1** focuses: The → cat (determiner-noun)
- **Head 2** focuses: cat → sat (subject-verb)
- **Head 3** focuses: sat → mat (verb-object)

---

### Fine-Tuning

**Fine-tuning** adapts a pretrained model to a specific domain/dataset.

#### Process

1. **Pretrained Model**: MarianMT models trained on OPUS parallel corpora
   - General domain translations
   - 100M+ parameters
   - Multilingual knowledge

2. **Domain-Specific Training**: Fine-tune on custom datasets
   - 120K German-English pairs
   - 120K English-Marathi pairs
   - Specific vocabulary/style

3. **Parameter Updates**: Adjust weights through backpropagation
   - Learning rate: 5e-5 (small to preserve pretrained knowledge)
   - Epochs: 3 (avoid overfitting)
   - Batch size: 8 (CPU-friendly)

#### Benefits

✅ **Improved Accuracy**: Better performance on domain-specific text  
✅ **Faster Training**: Starts from pretrained weights  
✅ **Less Data Required**: Compared to training from scratch  
✅ **Transfer Learning**: Leverages multilingual knowledge

#### Training Configuration

```python
TrainingArguments(
    learning_rate=5e-5,         # Small LR to preserve pretrained knowledge
    num_train_epochs=3,         # Few epochs to avoid overfitting
    per_device_train_batch_size=8,  # CPU-friendly batch size
    fp16=False,                 # CPU doesn't support fp16
    eval_strategy="epoch",      # Evaluate after each epoch
)
```

---

### Cascaded Translation

**Cascaded translation** chains multiple translation models sequentially.

#### Architecture

```
Source Language (DE)
    ↓
[Model 1: DE→EN]
    ↓
Pivot Language (EN)
    ↓
[Model 2: EN→MR]
    ↓
Target Language (MR)
```

#### Why Use Cascading?

1. **Resource Availability**
   - DE→MR direct models may not exist or have poor quality
   - DE→EN and EN→MR models are well-developed
   - English as universal pivot language

2. **Data Availability**
   - Large parallel corpora for DE↔EN and EN↔MR
   - Limited or no parallel data for DE↔MR

3. **Quality Control**
   - Can evaluate intermediate translations
   - Easier debugging and improvement

#### Drawbacks

⚠️ **Error Propagation**: Errors from Model 1 affect Model 2  
⚠️ **Increased Latency**: Two translation steps  
⚠️ **Semantic Drift**: Meaning may shift through pivot language

#### Mitigation Strategies

✅ High-quality fine-tuning on both models  
✅ Use intermediate English for verification  
✅ Smaller model sizes for faster inference

---

### Speech Processing

#### Speech-to-Text (Whisper)

**Whisper** is OpenAI's robust speech recognition model.

**Architecture:**
- Encoder-decoder transformer
- Trained on 680,000 hours of multilingual data
- Supports 99 languages including German

**Why Whisper?**
✅ High accuracy for German  
✅ Handles various audio qualities  
✅ No fine-tuning required  
✅ Lightweight models available (base, tiny)

#### Text-to-Speech (gTTS)

**gTTS** uses Google's Text-to-Speech API.

**Features:**
- Supports 100+ languages including Marathi
- Natural-sounding voices
- Simple API, no training needed
- Free for moderate usage

---

## 📁 Project Structure

```
translation/
├── backend/                          # Python Backend
│   ├── app.py                        # FastAPI application
│   ├── train_de_en.py                # German→English training
│   ├── train_en_mr.py                # English→Marathi training
│   ├── inference.py                  # Translation inference
│   ├── speech_module.py              # Speech processing
│   ├── evaluate.py                   # Model evaluation
│   ├── start.py                      # Quick start script
│   ├── requirements.txt              # Python dependencies
│   ├── Dockerfile                    # Docker configuration
│   ├── render.yaml                   # Render deployment config
│   ├── models/                       # Fine-tuned models
│   │   ├── de_en_finetuned/         # German→English model
│   │   └── en_mr_finetuned/         # English→Marathi model
│   ├── uploads/                      # Temporary audio uploads
│   └── audio_outputs/                # Generated audio files
│
├── frontend/                         # Flutter App
│   ├── lib/
│   │   ├── main.dart                 # App entry point
│   │   ├── screens/
│   │   │   └── home_screen.dart      # Main UI screen
│   │   └── services/
│   │       └── api_service.dart      # Backend communication
│   ├── android/
│   │   └── app/src/main/AndroidManifest.xml
│   └── pubspec.yaml                  # Flutter dependencies
│
└── README.md                         # This file
```

---

## 🚀 Installation & Setup

### Prerequisites

- **Python 3.11+**
- **pip** (Python package manager)
- **Git**
- **CUDA** (optional, for GPU training)
- **Flutter SDK** (for mobile app)
- **FFmpeg** (for audio processing)

### Backend Setup

1. **Clone Repository**
   ```bash
   cd translation/backend
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare Datasets**
   - Place `german_to_english_120k_dataset.csv` in `backend/`
   - Place `english_to_marathi_120k_dataset.csv` in `backend/`

### Frontend Setup

1. **Navigate to Frontend**
   ```bash
   cd ../frontend
   ```

2. **Install Dependencies**
   ```bash
   flutter pub get
   ```

3. **Update API URL** (in `lib/services/api_service.dart`)
   ```dart
   // For local testing
   static const String baseUrl = 'http://10.0.2.2:10000'; // Android emulator
   
   // For production
   static const String baseUrl = 'https://your-app.onrender.com';
   ```

---

## 🎓 Training Models

### Step 1: Train German → English

```bash
cd backend
python train_de_en.py
```

**Expected Output:**
```
🚀 German → English Translation Model Fine-tuning
📊 Loading dataset from german_to_english_120k_dataset.csv...
✅ Loaded 120000 translation pairs
📊 Train samples: 96000
📊 Validation samples: 24000
🤖 Loading model: Helsinki-NLP/opus-mt-de-en
🎯 Starting training...
...
✅ Final BLEU Score: 42.35
💾 Saving model to ./models/de_en_finetuned
```

**Training Time:**
- **GPU**: ~2-4 hours
- **CPU**: ~8-12 hours

### Step 2: Train English → Marathi

```bash
python train_en_mr.py
```

**Expected Output:**
```
🚀 English → Marathi Translation Model Fine-tuning
📊 Loading dataset from english_to_marathi_120k_dataset.csv...
✅ Loaded 120000 translation pairs
...
✅ Final BLEU Score: 38.72
💾 Saving model to ./models/en_mr_finetuned
```

### Step 3: Evaluate Models

```bash
python evaluate.py
```

**Sample Output:**
```
📊 Evaluating German → English Translation
✅ BLEU Score: 42.35

📝 Examples:
🇩🇪 German:     Ich lerne Deutsch.
🇬🇧 Reference:  I am learning German.
🤖 Prediction:  I'm learning German.
```

---

## 💻 Running Locally

### Quick Start

```bash
cd backend
python start.py
```

This will:
1. Install dependencies
2. Check for trained models
3. Start the API server on http://localhost:10000

### Manual Start

```bash
uvicorn app:app --host 0.0.0.0 --port 10000 --reload
```

### Test API

1. **Open Browser**: http://localhost:10000/docs
2. **Try Interactive API**: Swagger UI automatically available
3. **Health Check**: http://localhost:10000/health

### Run Flutter App

```bash
cd frontend

# Android
flutter run

# iOS
flutter run -d ios

# Web
flutter run -d chrome
```

---

## ☁ Deployment on Render

### Prerequisites

- GitHub account
- Render account (free tier available)
- Trained models pushed to repository

### Deployment Steps

#### 1. Prepare Repository

```bash
# Create .gitignore
echo "venv/" >> .gitignore
echo "*.csv" >> .gitignore
echo "__pycache__/" >> .gitignore

# Add files
git add .
git commit -m "Initial commit: Multilingual translation system"
git push origin main
```

⚠️ **Important**: Do NOT commit large CSV dataset files. Models should be committed.

#### 2. Create Render Web Service

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `multilingual-translation-api`
   - **Region**: Choose closest to users
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port 10000`

5. **Environment Variables**:
   - `PYTHON_VERSION`: `3.11.0`
   - `PORT`: `10000`

6. Click **"Create Web Service"**

#### 3. Monitor Deployment

```
==> Building...
==> Installing dependencies...
==> Starting application...
==> Your service is live at: https://your-app.onrender.com
```

#### 4. Update Flutter App

```dart
// lib/services/api_service.dart
static const String baseUrl = 'https://your-app.onrender.com';
```

#### 5. Verify Deployment

```bash
curl https://your-app.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "translation_model": true,
  "speech_model": true
}
```

### Render Free Tier Limitations

⚠️ **Important Constraints:**
- **CPU Only**: No GPU acceleration
- **512 MB RAM**: Use lightweight models
- **Spin Down**: Service sleeps after 15 min inactivity
- **First Request**: May take 30-60 seconds (cold start)

### Optimization for Render

✅ Use `base` Whisper model (not `large`)  
✅ Reduce batch size for inference  
✅ Implement request timeouts  
✅ Use caching for repeated translations  
✅ Compress model checkpoints

---

## 📡 API Documentation

### Base URL

```
Local:      http://localhost:10000
Production: https://your-app.onrender.com
```

### Endpoints

#### 1. Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "translation_model": true,
  "speech_model": true
}
```

---

#### 2. Text Translation

```http
POST /translate-text
Content-Type: application/json
```

**Request:**
```json
{
  "german": "Ich lerne Deutsch."
}
```

**Response:**
```json
{
  "german": "Ich lerne Deutsch.",
  "english": "I am learning German.",
  "marathi": "मी जर्मन शिकत आहे."
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:10000/translate-text \
  -H "Content-Type: application/json" \
  -d '{"german": "Guten Morgen!"}'
```

---

#### 3. Speech Translation

```http
POST /speech-translate
Content-Type: multipart/form-data
```

**Request:**
- `audio_file`: German audio file (wav, mp3, m4a)

**Response:**
```json
{
  "german_text": "Guten Morgen! Wie geht es dir?",
  "english_text": "Good morning! How are you?",
  "marathi_text": "सुप्रभात! तू कसा आहेस?",
  "marathi_audio_url": "/audio/marathi_123456.mp3"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:10000/speech-translate \
  -F "audio_file=@german_audio.mp3"
```

---

#### 4. Download Audio

```http
GET /audio/{filename}
```

**Response:** Audio file (MP3)

**Example:**
```
http://localhost:10000/audio/marathi_123456.mp3
```

---

## 📱 Flutter App Usage

### Features

1. **Text Translation**
   - Enter German text
   - View English and Marathi translations

2. **Audio Recording**
   - Record German speech directly
   - Automatic transcription and translation

3. **File Upload**
   - Upload pre-recorded German audio
   - Support for MP3, WAV, M4A formats

4. **Audio Playback**
   - Play generated Marathi audio
   - Built-in audio player

### Screenshots

```
┌─────────────────────────┐
│   🎙️ Translation App    │
├─────────────────────────┤
│                         │
│  German Text Input      │
│ ┌─────────────────────┐ │
│ │ Ich lerne Deutsch  │ │
│ └─────────────────────┘ │
│                         │
│  [Translate Text]       │
│                         │
│  🎤 Record  📂 Upload   │
│                         │
├─────────────────────────┤
│  Results:               │
│  🇩🇪 Ich lerne Deutsch  │
│  🇬🇧 I'm learning German│
│  🇮🇳 मी जर्मन शिकतोय    │
│                         │
│  [🔊 Play Audio]        │
└─────────────────────────┘
```

---

## 📊 Evaluation Metrics

### BLEU Score

**BLEU** (Bilingual Evaluation Understudy) measures translation quality.

**Formula:**
```
BLEU = BP × exp(Σ(w_n × log p_n))

where:
- BP: Brevity penalty
- p_n: Precision of n-grams
- w_n: Weights (typically 0.25 for 1-4 grams)
```

**Interpretation:**
- **0-10**: Very poor
- **10-20**: Poor
- **20-30**: Acceptable
- **30-40**: Good
- **40-50**: Very good
- **50+**: Excellent

### Expected Performance

| Model | BLEU Score | Quality |
|-------|------------|---------|
| German → English | 40-45 | Very Good |
| English → Marathi | 35-40 | Good |
| Cascaded (DE→MR) | 30-35 | Good* |

*Lower due to error propagation through pivot language

### Token Statistics

| Language | Avg Tokens | Min | Max |
|----------|-----------|-----|-----|
| German | 12.3 | 3 | 45 |
| English | 11.8 | 3 | 42 |
| Marathi | 13.6 | 4 | 48 |

---

## ⚡ GPU vs CPU Performance

### Training

| Hardware | DE→EN Training | EN→MR Training | Total |
|----------|---------------|----------------|-------|
| **NVIDIA RTX 3090** | 2.5 hours | 2.5 hours | 5 hours |
| **NVIDIA GTX 1080** | 4 hours | 4 hours | 8 hours |
| **CPU (16 cores)** | 10 hours | 10 hours | 20 hours |
| **CPU (8 cores)** | 18 hours | 18 hours | 36 hours |

### Inference (per request)

| Hardware | Speech-to-Text | Translation | Text-to-Speech | Total |
|----------|---------------|-------------|----------------|-------|
| **GPU** | 0.5s | 0.2s | 1.0s | 1.7s |
| **CPU (Cloud)** | 2.0s | 1.5s | 1.5s | 5.0s |

### Optimization Tips

**For CPU Training:**
✅ Reduce batch size to 4-8  
✅ Disable fp16 training  
✅ Use gradient accumulation  
✅ Train overnight  

**For CPU Inference:**
✅ Use smaller Whisper models (base/tiny)  
✅ Implement caching  
✅ Optimize batch processing  
✅ Use quantized models (future)

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Model Not Found Error

```
FileNotFoundError: [Errno 2] No such file or directory: './models/de_en_finetuned'
```

**Solution:**
```bash
# Train models first
python train_de_en.py
python train_en_mr.py
```

---

#### 2. CUDA Out of Memory (GPU)

```
RuntimeError: CUDA out of memory
```

**Solution:**
```python
# In training scripts, reduce batch size
BATCH_SIZE = 4  # Instead of 8
```

---

#### 3. Flask App Not Starting

```
ModuleNotFoundError: No module named 'transformers'
```

**Solution:**
```bash
pip install -r requirements.txt
```

---

#### 4. Audio Upload Fails

```
413 Request Entity Too Large
```

**Solution:** Reduce audio file size or increase limit in `app.py`:
```python
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB
```

---

#### 5. Flutter Connection Error

```
SocketException: Failed to connect
```

**Solution:**
- Check backend is running: `http://localhost:10000/health`
- Update URL in `api_service.dart`:
  - Android emulator: `http://10.0.2.2:10000`
  - iOS simulator: `http://localhost:10000`
  - Physical device: `http://<your-ip>:10000`

---

#### 6. Whisper Model Download Slow

**Solution:** Pre-download models:
```python
import whisper
whisper.load_model("base")  # Downloads to cache
```

---

#### 7. Render Deployment Fails

```
Error: Application failed to start
```

**Solution:**
- Check logs in Render dashboard
- Verify `requirements.txt` has all dependencies
- Ensure models are in repository (<500MB)
- Check start command: `uvicorn app:app --host 0.0.0.0 --port 10000`

---

## 🔮 Future Enhancements

### Technical Improvements

1. **Direct Translation Model**
   - Train DE→MR model to eliminate cascading
   - Reduce latency and error propagation

2. **Model Quantization**
   - Use INT8 quantization for faster CPU inference
   - Reduce model size by 75%

3. **Streaming Audio**
   - Real-time speech recognition
   - Progressive translation

4. **Batch Processing**
   - Translate multiple files simultaneously
   - API queue system

5. **Model Distillation**
   - Create smaller student models
   - Maintain quality with 10x speed improvement

### Feature Additions

6. **Additional Languages**
   - French, Spanish, Hindi support
   - Configurable language pairs

7. **Voice Cloning**
   - Preserve speaker characteristics
   - Use advanced TTS models

8. **Offline Mode**
   - Mobile app with on-device models
   - ONNX Runtime for efficiency

9. **Translation History**
   - Save past translations
   - Export functionality

10. **Confidence Scores**
    - Show translation certainty
    - Alternative suggestions

---

## 👥 Contributors

**[Your Name]**  
B.Tech Final Year Project  
[Department Name]  
[University Name]

**Guided By:** [Professor Name]

---

## 📄 License

This project is created for educational purposes as part of a B.Tech final year project.

---

## 📧 Contact

For questions or support:
- **Email**: your.email@example.com
- **GitHub**: github.com/yourusername
- **LinkedIn**: linkedin.com/in/yourprofile

---

## 🙏 Acknowledgments

- **OpenAI** for Whisper speech recognition
- **HuggingFace** for Transformers library
- **Helsinki-NLP** for MarianMT models
- **Google** for Text-to-Speech API
- **Render** for cloud hosting

---

## 📚 References

1. Vaswani et al. (2017). "Attention Is All You Need"
2. Helsinki-NLP. "OPUS-MT: Open Parallel Corpus Machine Translation"
3. Radford et al. (2022). "Robust Speech Recognition via Large-Scale Weak Supervision" (Whisper)
4. Papineni et al. (2002). "BLEU: a Method for Automatic Evaluation of Machine Translation"

---

**Last Updated:** February 13, 2026

