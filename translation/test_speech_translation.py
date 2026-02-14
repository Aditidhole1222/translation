"""
Test speech translation with pre-generated German audio files
NO MICROPHONE NEEDED!
"""

import requests
import os
import time
from pathlib import Path

BASE_URL = "http://localhost:10000"
TEST_AUDIO_DIR = Path("backend/test_audio")

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def check_backend():
    """Check if backend is running"""
    print("⏳ Checking backend status...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running!\n")
            return True
    except:
        pass
    
    print("❌ Backend not running. Start it with:")
    print("   cd backend")
    print("   $env:KMP_DUPLICATE_LIB_OK=\"TRUE\"")
    print("   python app.py\n")
    return False

def generate_test_audio():
    """Generate test audio files if they don't exist"""
    if not TEST_AUDIO_DIR.exists() or len(list(TEST_AUDIO_DIR.glob("*.mp3"))) == 0:
        print("📁 Test audio files not found. Generating...")
        os.system("python backend/generate_test_audio.py")
        print()

def test_text_translation():
    """Quick test of text translation"""
    print_header("QUICK TEST: Text Translation")
    
    test_text = "Guten Morgen, wie geht es dir?"
    print(f"📝 Testing: {test_text} (Good morning, how are you?)\n")
    
    try:
        response = requests.post(
            f"{BASE_URL}/translate-text",
            json={"german": test_text},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ German:  {result.get('source_text', 'N/A')}")
            print(f"✅ English: {result.get('intermediate_text', 'N/A')}")
            print(f"✅ Marathi: {result.get('final_text', 'N/A')}")
            print(f"\n⏱️  Time: ~5-10 seconds (CPU mode)")
            return True
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_speech_translation():
    """Test speech translation with generated audio files"""
    print_header("MAIN TEST: Speech Translation (No Mic Needed!)")
    
    # Get all test audio files
    audio_files = list(TEST_AUDIO_DIR.glob("*.mp3"))
    
    if not audio_files:
        print("❌ No test audio files found!")
        print("   Run: python backend/generate_test_audio.py")
        return False
    
    print(f"📁 Found {len(audio_files)} test audio files\n")
    
    success_count = 0
    
    for i, audio_path in enumerate(audio_files, 1):
        print(f"\n{'─'*70}")
        print(f"Test {i}/{len(audio_files)}: {audio_path.name}")
        print(f"{'─'*70}")
        
        try:
            # Read audio file
            with open(audio_path, 'rb') as audio_file:
                files = {'audio_file': (audio_path.name, audio_file, 'audio/mpeg')}
                
                print(f"📤 Uploading: {audio_path.name}")
                print(f"   Size: {audio_path.stat().st_size} bytes")
                print(f"⏳ Processing (may take 15-30 seconds on CPU)...\n")
                
                start_time = time.time()
                
                # Send to speech-translate endpoint
                response = requests.post(
                    f"{BASE_URL}/speech-translate",
                    files=files,
                    timeout=180  # 3 minutes for CPU
                )
                
                elapsed_time = time.time() - start_time
                
                if response.status_code == 200:
                    result = response.json()
                    
                    print(f"✅ SUCCESS! (took {elapsed_time:.1f}s)")
                    print(f"\n   📝 Transcribed (German): {result.get('transcribed_text', 'N/A')}")
                    print(f"   🇬🇧 English Translation: {result.get('intermediate_text', 'N/A')}")
                    print(f"   🇮🇳 Marathi Translation: {result.get('final_text', 'N/A')}")
                    
                    if 'audio_url' in result:
                        audio_url = result['audio_url']
                        print(f"   🔊 Marathi Audio: {audio_url}")
                        
                        # Verify output file exists
                        output_filename = audio_url.split('/')[-1]
                        output_path = Path(f"backend/audio_outputs/{output_filename}")
                        
                        if output_path.exists():
                            print(f"   ✅ Output file created: {output_path} ({output_path.stat().st_size} bytes)")
                        else:
                            print(f"   ⚠️  Output file not found at: {output_path}")
                    
                    success_count += 1
                    
                else:
                    print(f"❌ FAILED!")
                    print(f"   Status: {response.status_code}")
                    print(f"   Error: {response.text}")
                
        except requests.Timeout:
            print(f"❌ TIMEOUT! (>{180}s)")
            print("   Speech translation taking too long on CPU")
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
    
    return success_count, len(audio_files)

def main():
    """Main test runner"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  🎤 SPEECH TRANSLATION TEST - NO MICROPHONE NEEDED! 🎤  ".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    # Check backend
    if not check_backend():
        return
    
    # Generate test audio if needed
    generate_test_audio()
    
    # Run tests
    print_header("STARTING TESTS")
    
    # Test 1: Text translation (quick)
    text_success = test_text_translation()
    
    if not text_success:
        print("\n⚠️  Text translation failed. Fix this before testing speech.")
        return
    
    # Test 2: Speech translation (main test)
    success_count, total_count = test_speech_translation()
    
    # Summary
    print_header("TEST SUMMARY")
    
    print(f"""
   📊 Results:
      ✅ Text Translation: PASSED
      ✅ Speech Translation: {success_count}/{total_count} files processed

   ⏱️  Performance (CPU Mode):
      - First request: 15-30 seconds (model warmup)
      - Subsequent: 10-20 seconds per audio file
      - Text-only: 5-10 seconds

   📱 Mobile App Testing:
      Since you don't have a microphone, test with:
      1. ✅ Text translation (type German text)
      2. ✅ Upload audio feature (use test files from backend/test_audio/)
      3. ❌ Record audio (skip - requires microphone)

   🎯 What to Test in App:
      1. Launch app: cd frontend; flutter run -d emulator-5554
      2. Test Text Tab: Enter "Guten Morgen" → check translations
      3. Test Upload Audio: Upload backend/test_audio/test_good_morning.mp3
      4. Check audio playback works (play Marathi output)

   """)
    
    if success_count == total_count and success_count > 0:
        print("╔" + "="*68 + "╗")
        print("║" + " "*68 + "║")
        print("║" + "  ✅ ALL SPEECH TESTS PASSED! READY FOR DEPLOYMENT! ✅  ".center(68) + "║")
        print("║" + " "*68 + "║")
        print("╚" + "="*68 + "╝")
        
        print("""
   🚀 Next Steps:
      1. Test in mobile app (text + upload audio)
      2. If all working → Deploy using DEPLOYMENT_GUIDE.md
      3. Choose: Ngrok (quick) or Render (permanent)
        """)
    else:
        print("""
   ⚠️  Some tests failed. Check backend logs for errors.
        """)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
