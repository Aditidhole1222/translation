"""
GPU Detection and Setup Verification Script
Checks if CUDA-enabled GPU is available for training
"""

import sys

def check_gpu():
    print("=" * 60)
    print("🔍 Checking GPU Availability")
    print("=" * 60)
    
    # Check PyTorch installation
    try:
        import torch
        print(f"\n✅ PyTorch installed: {torch.__version__}")
    except ImportError:
        print("\n❌ PyTorch not installed!")
        print("Install with: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121")
        return
    
    # Check CUDA availability
    cuda_available = torch.cuda.is_available()
    
    if cuda_available:
        print(f"✅ CUDA is available!")
        print(f"   CUDA Version: {torch.version.cuda}")
        print(f"   GPU Count: {torch.cuda.device_count()}")
        
        for i in range(torch.cuda.device_count()):
            print(f"\n   GPU {i}: {torch.cuda.get_device_name(i)}")
            print(f"   Memory: {torch.cuda.get_device_properties(i).total_memory / 1024**3:.1f} GB")
        
        # Test GPU
        print("\n🧪 Testing GPU...")
        try:
            x = torch.randn(1000, 1000).cuda()
            y = torch.randn(1000, 1000).cuda()
            z = torch.matmul(x, y)
            print("✅ GPU test successful!")
            print(f"   Device: {z.device}")
        except Exception as e:
            print(f"❌ GPU test failed: {e}")
        
        print("\n" + "=" * 60)
        print("🚀 Your system is ready for GPU training!")
        print("   Expected training time: ~2-3 hours per model")
        print("=" * 60)
        
    else:
        print("❌ CUDA is NOT available")
        print("\n📝 Possible reasons:")
        print("   1. No NVIDIA GPU installed")
        print("   2. PyTorch installed without CUDA support")
        print("   3. CUDA drivers not installed")
        
        print("\n💡 To enable GPU support:")
        print("   1. Check if you have NVIDIA GPU: Windows + R → dxdiag")
        print("   2. Install CUDA Toolkit: https://developer.nvidia.com/cuda-downloads")
        print("   3. Reinstall PyTorch with CUDA:")
        print("\n   pip uninstall torch torchvision torchaudio")
        print("   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121")
        
        print("\n" + "=" * 60)
        print("⚠️  Will use CPU (slow training ~10 hours per model)")
        print("=" * 60)

if __name__ == "__main__":
    check_gpu()
