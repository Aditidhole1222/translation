"""Test gTTS functionality"""
from gtts import gTTS
import os
import traceback

try:
    os.makedirs('audio_outputs', exist_ok=True)
    print("Creating TTS object...")
    tts = gTTS(text='नमस्कार', lang='mr')
    print("Saving audio file...")
    tts.save('audio_outputs/test_marathi.mp3')
    print('✅ gTTS test successful - file saved to audio_outputs/test_marathi.mp3')
except Exception as e:
    print(f'❌ gTTS test failed')
    print(f'Error: {str(e)}')
    traceback.print_exc()
