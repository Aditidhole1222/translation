"""
Speech Processing Module
Provides Speech-to-Text (Whisper) and Text-to-Speech (gTTS) functionality
"""

import os
import torch
import whisper
from gtts import gTTS
from pathlib import Path
import tempfile
from typing import Optional

# ========================================================
# Configuration
# ========================================================

WHISPER_MODEL_NAME = "base"  # Options: tiny, base, small, medium, large
TTS_LANGUAGE = "mr"  # Marathi
AUDIO_OUTPUT_DIR = "./audio_outputs"

# Create output directory
Path(AUDIO_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# ========================================================
# Speech-to-Text (Whisper)
# ========================================================

class SpeechToText:
    """
    German Speech-to-Text using OpenAI Whisper
    """
    
    def __init__(self, model_name: str = WHISPER_MODEL_NAME):
        """
        Initialize Whisper model
        
        Args:
            model_name: Whisper model size (tiny, base, small, medium, large)
        """
        print(f"🔄 Loading Whisper model: {model_name}")
        # Force CPU mode to avoid RTX 5060 sm_120 incompatibility
        self.device = "cpu"
        self.model = whisper.load_model(model_name, device=self.device)
        print(f"✅ Whisper model loaded on CPU")
    
    def transcribe(
        self, 
        audio_path: str, 
        language: str = "de"
    ) -> dict:
        """
        Transcribe audio file to text
        
        Args:
            audio_path: Path to audio file
            language: Language code (de for German)
            
        Returns:
            Dictionary with transcription and metadata
        """
        print(f"🎤 Transcribing audio: {audio_path}")
        
        # Transcribe
        result = self.model.transcribe(
            audio_path,
            language=language,
            fp16=torch.cuda.is_available()  # Use fp16 if GPU available
        )
        
        text = result["text"].strip()
        
        print(f"✅ Transcription: {text}")
        
        return {
            "text": text,
            "language": result.get("language", language),
            "segments": result.get("segments", [])
        }
    
    def transcribe_german(self, audio_path: str) -> str:
        """
        Transcribe German audio to text
        
        Args:
            audio_path: Path to German audio file
            
        Returns:
            Transcribed German text
        """
        result = self.transcribe(audio_path, language="de")
        return result["text"]

# ========================================================
# Text-to-Speech (gTTS)
# ========================================================

class TextToSpeech:
    """
    Text-to-Speech using Google TTS (gTTS)
    """
    
    def __init__(self, output_dir: str = AUDIO_OUTPUT_DIR):
        """
        Initialize TTS
        
        Args:
            output_dir: Directory to save generated audio files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ TTS initialized, output: {self.output_dir}")
    
    def synthesize(
        self, 
        text: str, 
        language: str = TTS_LANGUAGE,
        filename: Optional[str] = None,
        slow: bool = False
    ) -> str:
        """
        Convert text to speech
        
        Args:
            text: Text to convert
            language: Language code (mr for Marathi)
            filename: Output filename (auto-generated if None)
            slow: Speak slowly
            
        Returns:
            Path to generated audio file
        """
        print(f"🔊 Generating speech for: {text[:50]}...")
        
        # Generate filename if not provided
        if filename is None:
            filename = f"tts_{hash(text) % 1000000}.mp3"
        
        # Ensure .mp3 extension
        if not filename.endswith('.mp3'):
            filename += '.mp3'
        
        output_path = self.output_dir / filename
        
        # Generate speech
        tts = gTTS(text=text, lang=language, slow=slow)
        tts.save(str(output_path))
        
        print(f"✅ Audio saved: {output_path}")
        
        return str(output_path)
    
    def synthesize_marathi(
        self, 
        marathi_text: str, 
        filename: Optional[str] = None
    ) -> str:
        """
        Convert Marathi text to speech
        
        Args:
            marathi_text: Marathi text to convert
            filename: Output filename (auto-generated if None)
            
        Returns:
            Path to generated Marathi audio file
        """
        return self.synthesize(
            text=marathi_text,
            language="mr",
            filename=filename
        )

# ========================================================
# Complete Speech Pipeline
# ========================================================

class SpeechPipeline:
    """
    Complete speech processing pipeline
    """
    
    def __init__(
        self, 
        whisper_model: str = WHISPER_MODEL_NAME,
        output_dir: str = AUDIO_OUTPUT_DIR
    ):
        """
        Initialize speech pipeline
        
        Args:
            whisper_model: Whisper model size
            output_dir: Audio output directory
        """
        print("=" * 60)
        print("🚀 Initializing Speech Pipeline")
        print("=" * 60)
        
        self.stt = SpeechToText(whisper_model)
        self.tts = TextToSpeech(output_dir)
        
        print("✅ Speech pipeline ready!")
        print("=" * 60)
    
    def audio_to_text(self, audio_path: str, language: str = "de") -> str:
        """
        Convert audio to text
        
        Args:
            audio_path: Path to audio file
            language: Language code
            
        Returns:
            Transcribed text
        """
        return self.stt.transcribe(audio_path, language)["text"]
    
    def text_to_audio(
        self, 
        text: str, 
        language: str = "mr",
        filename: Optional[str] = None
    ) -> str:
        """
        Convert text to audio
        
        Args:
            text: Text to convert
            language: Language code
            filename: Output filename
            
        Returns:
            Path to audio file
        """
        return self.tts.synthesize(text, language, filename)

# ========================================================
# Standalone Testing
# ========================================================

def main():
    """
    Test speech processing
    """
    pipeline = SpeechPipeline()
    
    # Test TTS
    print("\n" + "=" * 60)
    print("🧪 Testing Text-to-Speech")
    print("=" * 60)
    
    test_marathi = "नमस्कार! तुमचं नाव काय आहे?"
    audio_path = pipeline.text_to_audio(test_marathi, language="mr")
    
    print(f"\n✅ Generated audio: {audio_path}")
    
    # Note: STT testing requires actual audio file
    print("\n💡 For STT testing, provide a German audio file")

if __name__ == "__main__":
    main()
