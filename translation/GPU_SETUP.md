# 🚀 GPU Setup Guide for Fast Training

## Your System
- **GPU:** NVIDIA GeForce RTX 5060 (4GB VRAM)
- **Current PyTorch:** CPU-only version
- **Target:** GPU-enabled training (~2-3 hours instead of 10!)

---

## ⚡ Quick Setup Instructions

### Step 1: Uninstall CPU-only PyTorch

```powershell
pip uninstall torch torchvision torchaudio -y
```

### Step 2: Install PyTorch with CUDA Support

```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

**Note:** This installs PyTorch with CUDA 12.1 support (compatible with RTX 5060)

### Step 3: Verify GPU is Detected

```powershell
python backend\check_gpu.py
```

You should see:
```
✅ CUDA is available!
   GPU 0: NVIDIA GeForce RTX 5060
   Memory: 4.0 GB
```

### Step 4: Fix OpenMP Conflict (if needed)

Add this to your environment:
```powershell
$env:KMP_DUPLICATE_LIB_OK = "TRUE"
```

Or add permanently to your activation script.

---

## 🎯 Training Performance Comparison

| Hardware | Training Time per Model | Total Time |
|----------|------------------------|------------|
| CPU Only | ~10 hours | ~20 hours |
| RTX 5060 (GPU) | ~2-3 hours | ~4-6 hours |

**Speed improvement: ~4x faster!** ⚡

---

## 💾 Memory Optimization for 4GB GPU

Your RTX 5060 has 4GB VRAM. The training scripts are already optimized, but if you get OOM (Out of Memory) errors:

### Option 1: Reduce Batch Size
In `train_de_en.py` and `train_en_mr.py`, change:
```python
BATCH_SIZE = 4  # Instead of 8
```

### Option 2: Enable Gradient Accumulation
```python
TrainingArguments(
    per_device_train_batch_size=4,
    gradient_accumulation_steps=2,  # Effective batch size = 4*2 = 8
    ...
)
```

---

## 🧪 Test GPU Before Training

```powershell
# Run quick GPU test
python backend\check_gpu.py

# If successful, start training
python backend\train_de_en.py
```

---

## ⚠️ Troubleshooting

### Error: "CUDA out of memory"
**Solution:** Reduce batch size to 4 or even 2

### Error: "CUDA driver version is insufficient"
**Solution:** Update NVIDIA drivers from https://www.nvidia.com/Download/index.aspx

### Error: Still using CPU after installation
**Solution:** 
1. Completely restart your terminal
2. Reactivate virtual environment
3. Run `python -c "import torch; print(torch.cuda.is_available())"`

---

## 🎓 Alternative: Google Colab (FREE GPU)

If you encounter issues or want even faster training with better GPUs:

### Colab Setup (15 GB GPU for FREE!)

1. **Upload to Google Drive:**
   - Upload both CSV datasets
   - Upload training scripts

2. **Open Google Colab:** https://colab.research.google.com

3. **Enable GPU:**
   - Runtime → Change runtime type → GPU → T4 GPU

4. **Run Training:**
```python
# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Install dependencies
!pip install transformers datasets evaluate sacrebleu

# Run training
!python /content/drive/MyDrive/train_de_en.py
```

**Colab Benefits:**
- ✅ FREE Tesla T4 GPU (16GB VRAM)
- ✅ No local hardware needed
- ✅ Training time: ~1.5-2 hours per model
- ✅ Can run overnight without your PC on

---

## 📊 Expected Results with GPU

### German → English
- Training time: ~2-3 hours
- BLEU Score: 40-45
- GPU Memory: ~3.5 GB

### English → Marathi  
- Training time: ~2-3 hours
- BLEU Score: 35-40
- GPU Memory: ~3.5 GB

---

## ✅ Quick Start Commands

```powershell
# 1. Reinstall PyTorch with GPU support
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 2. Verify GPU
python backend\check_gpu.py

# 3. Start training
python backend\train_de_en.py

# 4. After first model finishes
python backend\train_en_mr.py
```

---

Good luck with GPU training! 🚀
