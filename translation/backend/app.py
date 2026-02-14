"""
FastAPI Backend for Multilingual Speech Translation
Provides REST API endpoints for text and speech translation
"""

import os
import shutil
import traceback
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
from pathlib import Path

from inference import TranslationPipeline
from speech_module import SpeechPipeline

# ========================================================
# Configuration
# ========================================================

app = FastAPI(
    title="Multilingual Speech Translation API",
    description="German → English → Marathi Translation Pipeline",
    version="1.0.0"
)

# CORS Configuration (Allow Flutter app to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Flutter app domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories
UPLOAD_DIR = Path("./uploads")
AUDIO_OUTPUT_DIR = Path("./audio_outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
AUDIO_OUTPUT_DIR.mkdir(exist_ok=True)

# File size limit (10 MB)
MAX_FILE_SIZE = 10 * 1024 * 1024

# ========================================================
# Request/Response Models
# ========================================================

class TextTranslationRequest(BaseModel):
    """
    Request model for text translation
    """
    german: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "german": "Ich lerne Deutsch."
            }
        }

class TextTranslationResponse(BaseModel):
    """
    Response model for text translation
    """
    german: str
    english: str
    marathi: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "german": "Ich lerne Deutsch.",
                "english": "I am learning German.",
                "marathi": "मी जर्मन शिकत आहे."
            }
        }

class SpeechTranslationResponse(BaseModel):
    """
    Response model for speech translation
    """
    german_text: str
    english_text: str
    marathi_text: str
    marathi_audio_url: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "german_text": "Guten Morgen!",
                "english_text": "Good morning!",
                "marathi_text": "सुप्रभात!",
                "marathi_audio_url": "/audio/output_12345.mp3"
            }
        }

# ========================================================
# Initialize Models (Load once at startup)
# ========================================================

translation_pipeline: Optional[TranslationPipeline] = None
speech_pipeline: Optional[SpeechPipeline] = None

@app.on_event("startup")
async def startup_event():
    """
    Load models when the application starts
    """
    global translation_pipeline, speech_pipeline
    
    print("=" * 60)
    print("🚀 Starting Multilingual Translation API")
    print("=" * 60)
    
    try:
        # Load translation models
        translation_pipeline = TranslationPipeline()
        
        # Load speech models
        speech_pipeline = SpeechPipeline(
            whisper_model="base",
            output_dir=str(AUDIO_OUTPUT_DIR)
        )
        
        print("\n✅ All models loaded successfully!")
        print("🌐 API is ready to serve requests")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error loading models: {e}")
        print("💡 Make sure fine-tuned models are in ./models/ directory")
        raise

# ========================================================
# Health Check Endpoint
# ========================================================

@app.get("/")
async def root():
    """
    Health check endpoint
    """
    return {
        "status": "running",
        "message": "Multilingual Speech Translation API",
        "version": "1.0.0",
        "pipeline": "German → English → Marathi"
    }

@app.get("/health")
async def health_check():
    """
    Detailed health check
    """
    return {
        "status": "healthy",
        "translation_model": translation_pipeline is not None,
        "speech_model": speech_pipeline is not None
    }

# ========================================================
# Text Translation Endpoint
# ========================================================

@app.post("/translate-text", response_model=TextTranslationResponse)
async def translate_text(request: TextTranslationRequest):
    """
    Translate German text to English and Marathi
    
    Args:
        request: TextTranslationRequest with German text
        
    Returns:
        TextTranslationResponse with all translations
    """
    if not translation_pipeline:
        raise HTTPException(
            status_code=503,
            detail="Translation model not loaded"
        )
    
    try:
        # Validate input
        if not request.german or not request.german.strip():
            raise HTTPException(
                status_code=400,
                detail="German text cannot be empty"
            )
        
        # Perform translation
        result = translation_pipeline.translate_de_to_mr(request.german)
        
        return TextTranslationResponse(
            german=result["german"],
            english=result["english"],
            marathi=result["marathi"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Translation error: {str(e)}"
        )

# ========================================================
# Speech Translation Endpoint
# ========================================================

@app.post("/speech-translate", response_model=SpeechTranslationResponse)
async def speech_translate(audio_file: UploadFile = File(...)):
    """
    Translate German speech to Marathi speech
    
    Pipeline:
    1. German Speech → German Text (Whisper)
    2. German Text → English Text (MarianMT)
    3. English Text → Marathi Text (MarianMT)
    4. Marathi Text → Marathi Speech (gTTS)
    
    Args:
        audio_file: German audio file (wav, mp3, m4a, etc.)
        
    Returns:
        SpeechTranslationResponse with translations and audio URL
    """
    if not translation_pipeline or not speech_pipeline:
        raise HTTPException(
            status_code=503,
            detail="Models not loaded"
        )
    
    # Validate file
    if not audio_file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file provided"
        )
    
    # Check file extension
    allowed_extensions = ['.wav', '.mp3', '.m4a', '.ogg', '.flac']
    file_ext = Path(audio_file.filename).suffix.lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file_ext} not supported. Allowed: {allowed_extensions}"
        )
    
    temp_audio_path = None
    output_audio_path = None
    
    try:
        # Save uploaded file
        temp_audio_path = UPLOAD_DIR / f"temp_{audio_file.filename}"
        
        with open(temp_audio_path, "wb") as buffer:
            content = await audio_file.read()
            
            # Check file size
            if len(content) > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail=f"File too large. Max size: {MAX_FILE_SIZE / (1024*1024):.1f} MB"
                )
            
            buffer.write(content)
        
        # Step 1: Speech to Text (German)
        print(f"🎤 Transcribing German audio...")
        german_text = speech_pipeline.audio_to_text(
            str(temp_audio_path),
            language="de"
        )
        
        if not german_text or not german_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not transcribe audio. Please ensure audio contains clear German speech."
            )
        
        print(f"✅ Transcribed: {german_text}")
        
        # Step 2 & 3: Translation (DE→EN→MR)
        print(f"🔄 Translating...")
        translation_result = translation_pipeline.translate_de_to_mr(german_text)
        
        english_text = translation_result["english"]
        marathi_text = translation_result["marathi"]
        
        print(f"✅ English: {english_text}")
        print(f"✅ Marathi: {marathi_text}")
        
        # Step 4: Text to Speech (Marathi)
        print(f"🔊 Generating Marathi speech...")
        output_filename = f"marathi_{hash(marathi_text) % 1000000}.mp3"
        output_audio_path = speech_pipeline.text_to_audio(
            marathi_text,
            language="mr",
            filename=output_filename
        )
        
        print(f"✅ Audio generated: {output_audio_path}")
        
        # Return response
        return SpeechTranslationResponse(
            german_text=german_text,
            english_text=english_text,
            marathi_text=marathi_text,
            marathi_audio_url=f"/audio/{output_filename}"
        )
        
    except HTTPException:
        raise
    
    except Exception as e:
        print(f"❌ Speech translation error:")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Processing error: {str(e)}"
        )
    
    finally:
        # Clean up temporary file
        if temp_audio_path and temp_audio_path.exists():
            temp_audio_path.unlink()

# ========================================================
# Audio File Serving Endpoint
# ========================================================

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    """
    Serve generated audio files
    
    Args:
        filename: Audio file name
        
    Returns:
        Audio file
    """
    file_path = AUDIO_OUTPUT_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Audio file not found"
        )
    
    return FileResponse(
        path=file_path,
        media_type="audio/mpeg",
        filename=filename
    )

# ========================================================
# Run Server
# ========================================================

if __name__ == "__main__":
    # Run with uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=10000,
        reload=False  # Disable reload in production
    )
