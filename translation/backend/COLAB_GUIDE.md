# Google Colab GPU Training Guide

## Why Use Colab?
- **Free T4 GPU** (16GB VRAM) - fully compatible with PyTorch
- **2-3 hours per model** instead of 8-10 hours on CPU
- No local hardware issues with RTX 5060 compatibility

## Quick Start (5 minutes setup)

### Step 1: Upload Notebook to Colab
1. Open **Google Colab**: https://colab.research.google.com/
2. Click **File** → **Upload notebook**
3. Upload `colab_training.ipynb` from `backend` folder
4. Click **Runtime** → **Change runtime type** → Select **T4 GPU** → **Save**

### Step 2: Upload Your Datasets
When the notebook runs, it will ask you to upload:
- `german_to_english_120k_dataset.csv` (from `backend` folder)
- `english_to_marathi_120k_dataset.csv` (from `backend` folder)

### Step 3: Run All Cells
1. Click **Runtime** → **Run all**
2. Watch the progress bars
3. **Total time: ~4-6 hours** for both models

### Step 4: Download Trained Models
The notebook will automatically download:
- `de_en_finetuned.zip` (German → English model)
- `en_mr_finetuned.zip` (English → Marathi model)

### Step 5: Use Models Locally
1. Extract both zip files in `C:\Users\mohit\translation\backend\models\`
2. Your folder structure should be:
   ```
   backend/
     models/
       de_en_finetuned/
         config.json
         pytorch_model.bin
         tokenizer_config.json
         vocab.json
         ...
       en_mr_finetuned/
         config.json
         pytorch_model.bin
         tokenizer_config.json
         vocab.json
         ...
   ```

3. Test your API:
   ```powershell
   cd C:\Users\mohit\translation\backend
   python app.py
   ```

## Benefits
✅ **Free GPU** - No cost for training  
✅ **Faster Training** - 2-3 hours vs 8-10 hours on CPU  
✅ **No Compatibility Issues** - T4 GPU works perfectly with PyTorch  
✅ **Easy to Use** - Just upload datasets and run  

## Important Notes
- **Colab sessions timeout after 12 hours** - Both models will complete in time
- **Stay connected** - Keep the browser tab open during training
- **GPU quota** - Free Colab gives ~12 hours of GPU per day
- **Save progress** - Download models immediately after training completes

## Troubleshooting

### "GPU not available"
- Go to **Runtime** → **Change runtime type** → Select **T4 GPU**
- Click **Save** and re-run cells

### "Session disconnected"
- Colab has timeout limits
- Re-run the last successful cell to resume

### "Out of memory"
- The notebook is optimized for T4 GPU
- Should not happen with 16GB VRAM

## Alternative: Kaggle (if Colab quota exhausted)
Kaggle also offers free GPUs:
1. Go to https://www.kaggle.com/
2. Create notebook with GPU accelerator
3. Upload the same training scripts
4. Similar process to Colab
