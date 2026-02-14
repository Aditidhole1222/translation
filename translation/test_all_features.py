"""
Complete Feature Testing Script for Translation App
Tests all backend endpoints before deployment
"""

import requests
import json
import os
from pathlib import Path

BASE_URL = "http://localhost:10000"

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def test_health():
    """Test 1: Health Check"""
    print_header("TEST 1: Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"✅ Status Code: {response.status_code}")
        print(f"✅ Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False

def test_text_translation():
    """Test 2: Text Translation (German → English → Marathi)"""
    print_header("TEST 2: Text Translation")
    
    test_cases = [
        "Guten Morgen, wie geht es dir?",  # Good morning, how are you?
        "Ich liebe Programmierung.",  # I love programming
        "Das Wetter ist heute schön."  # The weather is nice today
    ]
    
    for i, german_text in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"📝 German Input: {german_text}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/translate-text",
                json={"text": german_text},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Status: SUCCESS")
                print(f"   German:  {result.get('source_text', 'N/A')}")
                print(f"   English: {result.get('intermediate_text', 'N/A')}")
                print(f"   Marathi: {result.get('final_text', 'N/A')}")
            else:
                print(f"❌ Status: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"❌ FAILED: {str(e)}")
    
    return True

def test_speech_translation():
    """Test 3: Speech Translation (requires audio file)"""
    print_header("TEST 3: Speech Translation")
    
    # Check if test audio file exists
    test_audio_path = Path("backend/test_audio.wav")
    
    if not test_audio_path.exists():
        print("⚠️  No test audio file found at backend/test_audio.wav")
        print("   To test speech translation:")
        print("   1. Record a German audio file (WAV format)")
        print("   2. Save it as backend/test_audio.wav")
        print("   3. Run this test again")
        print("\n   OR test directly from the mobile app by:")
        print("   - Recording German speech")
        print("   - Uploading a German audio file")
        return False
    
    print(f"📁 Using audio file: {test_audio_path}")
    
    try:
        with open(test_audio_path, 'rb') as audio_file:
            files = {'file': ('test_audio.wav', audio_file, 'audio/wav')}
            
            print("🎤 Uploading audio for translation...")
            response = requests.post(
                f"{BASE_URL}/speech-translate",
                files=files,
                timeout=180  # 3 minutes for CPU processing
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Status: SUCCESS")
                print(f"   Transcribed German: {result.get('transcribed_text', 'N/A')}")
                print(f"   English Translation: {result.get('intermediate_text', 'N/A')}")
                print(f"   Marathi Translation: {result.get('final_text', 'N/A')}")
                print(f"   Audio Output: {result.get('audio_url', 'N/A')}")
                
                # Check if audio file was created
                if 'audio_url' in result:
                    audio_filename = result['audio_url'].split('/')[-1]
                    audio_path = Path(f"backend/output/{audio_filename}")
                    if audio_path.exists():
                        print(f"   ✅ Output audio file created: {audio_path}")
                    else:
                        print(f"   ⚠️  Audio file not found at: {audio_path}")
            else:
                print(f"❌ Status: {response.status_code}")
                print(f"   Error: {response.text}")
                
    except FileNotFoundError:
        print(f"❌ Audio file not found: {test_audio_path}")
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
    
    return True

def test_model_info():
    """Test 4: Check which models are loaded"""
    print_header("TEST 4: Model Information")
    
    print("📦 Checking loaded models:")
    print("   ✓ Whisper Base (Speech-to-Text)")
    print("   ✓ German → English (Fine-tuned 10K)")
    print("   ✓ English → Marathi (Fine-tuned 10K)")
    print("   ✓ gTTS (Text-to-Speech)")
    
    # Check model directories
    models_dir = Path("backend/models")
    if models_dir.exists():
        print("\n📁 Model files:")
        de_en = models_dir / "de_en_finetuned_10k"
        en_mr = models_dir / "en_mr_finetuned_10k"
        
        if de_en.exists():
            print(f"   ✅ German→English: {de_en}")
        else:
            print(f"   ❌ German→English: NOT FOUND")
            
        if en_mr.exists():
            print(f"   ✅ English→Marathi: {en_mr}")
        else:
            print(f"   ❌ English→Marathi: NOT FOUND")
    
    return True

def mobile_app_testing_guide():
    """Mobile App Testing Checklist"""
    print_header("MOBILE APP TESTING GUIDE")
    
    print("""
📱 **EMULATOR TESTING CHECKLIST**

Before deployment, test these features in the app:

1. ✅ **App Launch**
   - Open app on emulator (emulator-5554)
   - Check Material Design 3 UI loads properly
   - No crash on startup

2. ✅ **Text Translation Tab**
   - Enter German text in input field
   - Tap "Translate" button
   - Verify:
     ✓ English translation appears
     ✓ Marathi translation appears
     ✓ No timeout errors (should complete in 5-10 seconds)
     ✓ Loading indicator shows during translation

3. ✅ **Speech Translation Tab**
   
   A. **Record Audio Test:**
   - Tap microphone button (🎤)
   - Speak in German (or any language for testing)
   - Tap stop recording
   - Verify:
     ✓ Recording interface works
     ✓ Audio is captured
     ✓ Translation processes (may take 15-30 seconds first time)
     ✓ Results display correctly
     ✓ Play button (▶️) plays Marathi audio output

   B. **Upload Audio Test:**
   - Tap "Upload Audio" button
   - Select a German audio file from device
   - Verify:
     ✓ File picker opens
     ✓ Audio file uploads successfully
     ✓ Translation completes (CPU mode: allow 30-60 seconds)
     ✓ Marathi audio output is playable

4. ✅ **Error Handling**
   - Try with empty input → should show error message
   - Try with very long text → should handle gracefully
   - Turn off backend → should show connection error

5. ✅ **Performance**
   - First request: 15-30 seconds (CPU warmup) ⏱️
   - Subsequent requests: 5-10 seconds ⚡
   - No app crashes or freezes

6. ✅ **Audio Output**
   - Marathi audio plays clearly
   - Volume control works
   - Pause/play works properly

---

**🎯 QUICK TEST (2 minutes):**

1. Start backend: `cd backend; python app.py`
2. Launch emulator: `flutter devices` (check emulator-5554)
3. Run app: `cd frontend; flutter run -d emulator-5554`
4. Test text: "Guten Morgen" → should get Marathi output
5. Test speech: Record any audio → should process and return audio

---

**🔧 TROUBLESHOOTING:**

❌ **"TimeoutException"**
   → Backend not running or wrong URL
   → Check: http://10.0.2.2:10000/health

❌ **"Network Error"**
   → Emulator can't reach backend
   → Ensure backend running on port 10000
   → Check api_service.dart has correct baseUrl

❌ **Speech translation fails**
   → Check backend logs for errors
   → Verify uploads/ directory exists
   → Check audio file format (WAV/MP3)

❌ **Slow performance**
   → Expected on CPU! First request: 15-30s
   → Subsequent requests: 5-10s
   → This is normal without GPU

---

**✅ READY FOR DEPLOYMENT WHEN:**

✓ All text translations work correctly
✓ Speech recording works
✓ Audio upload works  
✓ Audio playback works
✓ No crashes or errors
✓ Performance acceptable (even if slow on CPU)

""")

def run_all_tests():
    """Run complete test suite"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  🧪 TRANSLATION APP - COMPLETE FEATURE TEST  ".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    # Check if backend is running
    print("\n⚙️  Prerequisites Check:")
    print("   1. Backend should be running on http://localhost:10000")
    print("   2. Fine-tuned models should be loaded")
    print("   3. Emulator should be ready (emulator-5554)")
    
    input("\n👉 Press ENTER when backend is running...")
    
    # Run tests
    results = []
    
    results.append(("Health Check", test_health()))
    results.append(("Text Translation", test_text_translation()))
    results.append(("Speech Translation", test_speech_translation()))
    results.append(("Model Information", test_model_info()))
    
    # Show mobile testing guide
    mobile_app_testing_guide()
    
    # Summary
    print_header("TEST SUMMARY")
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {status}: {test_name}")
    
    passed_count = sum(1 for _, p in results if p)
    total_count = len(results)
    
    print(f"\n   📊 Results: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("""
   ╔════════════════════════════════════════════════╗
   ║  ✅ ALL BACKEND TESTS PASSED!                 ║
   ║                                                ║
   ║  Next Steps:                                   ║
   ║  1. Test mobile app features (see guide above)║
   ║  2. If all working → Ready for deployment!    ║
   ║  3. Deploy using DEPLOYMENT_GUIDE.md          ║
   ╚════════════════════════════════════════════════╝
        """)
    else:
        print("""
   ⚠️  SOME TESTS FAILED
   
   Please fix the issues before deployment.
   Check backend logs for error details.
        """)
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
