"""
Generate German test audio files for testing speech translation
No microphone needed!
"""

from gtts import gTTS
import os

# Create test_audio directory
os.makedirs("test_audio", exist_ok=True)

# Test sentences in German
test_sentences = [
    {
        "text": "Guten Morgen, wie geht es dir?",
        "filename": "test_good_morning.mp3",
        "description": "Good morning, how are you?"
    },
    {
        "text": "Ich liebe Programmierung und Technologie.",
        "filename": "test_programming.mp3",
        "description": "I love programming and technology"
    },
    {
        "text": "Das Wetter ist heute sehr schön.",
        "filename": "test_weather.mp3",
        "description": "The weather is very nice today"
    },
    {
        "text": "Mein Name ist Student und ich studiere Informatik.",
        "filename": "test_student.mp3",
        "description": "My name is Student and I study Computer Science"
    },
    {
        "text": "Willkommen bei der Übersetzungs-App.",
        "filename": "test_welcome.mp3",
        "description": "Welcome to the translation app"
    }
]

print("\n" + "="*60)
print("  🎤 GENERATING GERMAN TEST AUDIO FILES")
print("="*60 + "\n")

for i, item in enumerate(test_sentences, 1):
    print(f"{i}. Creating: {item['filename']}")
    print(f"   German: {item['text']}")
    print(f"   Meaning: {item['description']}")
    
    try:
        # Generate German audio using gTTS
        tts = gTTS(text=item['text'], lang='de', slow=False)
        filepath = os.path.join("test_audio", item['filename'])
        tts.save(filepath)
        
        # Check file size
        file_size = os.path.getsize(filepath)
        print(f"   ✅ Saved: {filepath} ({file_size} bytes)")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()

print("="*60)
print("  ✅ TEST AUDIO FILES CREATED!")
print("="*60)

print(f"""
📁 Location: backend/test_audio/

🎯 Use these files to test speech translation:

1. Run the test script:
   python test_speech_translation.py

2. OR manually test each file:
   - Upload via Postman/API
   - Use in mobile app (upload audio feature)

3. Expected pipeline:
   German Audio → Whisper STT → German Text → English → Marathi → Marathi Audio

All files are ready for testing! 🚀
""")
