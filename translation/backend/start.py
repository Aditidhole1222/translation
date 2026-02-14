"""
Quick Start Script for Local Development
"""

import subprocess
import sys
import os

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")

def main():
    print_header("Multilingual Translation System - Quick Start")
    
    # Step 1: Install dependencies
    print_header("Step 1: Installing Dependencies")
    print("Running: pip install -r requirements.txt")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Step 2: Check for models
    print_header("Step 2: Checking Models")
    
    de_en_exists = os.path.exists("./models/de_en_finetuned")
    en_mr_exists = os.path.exists("./models/en_mr_finetuned")
    
    if not de_en_exists or not en_mr_exists:
        print("⚠️  Fine-tuned models not found!")
        print("\n📝 You need to train the models first:")
        print("   1. Place datasets in the backend folder:")
        print("      - german_to_english_120k_dataset.csv")
        print("      - english_to_marathi_120k_dataset.csv")
        print("   2. Run training scripts:")
        print("      python train_de_en.py")
        print("      python train_en_mr.py")
        print("\n💡 This will take several hours depending on your hardware.")
        print("   GPU is recommended for faster training.")
        return
    else:
        print("✅ Models found!")
    
    # Step 3: Start server
    print_header("Step 3: Starting API Server")
    print("Starting server on http://localhost:10000")
    print("\n🌐 API will be available at:")
    print("   - Health: http://localhost:10000/health")
    print("   - Docs:   http://localhost:10000/docs")
    print("\n⏹️  Press Ctrl+C to stop the server")
    print("-" * 60 + "\n")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "app:app",
            "--host", "0.0.0.0",
            "--port", "10000",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n\n✅ Server stopped")

if __name__ == "__main__":
    main()
