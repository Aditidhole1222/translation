# 🚀 HOW TO ENABLE GPU IN GOOGLE COLAB

## STEP-BY-STEP VISUAL GUIDE

### Before You Start
✅ Open the notebook in **Google Colab** (https://colab.research.google.com/)  
✅ Upload `colab_training.ipynb`

---

## Enable GPU (REQUIRED!)

### Step 1: Click "Runtime" Menu
Look at the top menu bar in Colab:
```
File  Edit  View  Insert  Runtime  Tools  Help
              ↑
          Click here
```

### Step 2: Select "Change runtime type"
A dropdown menu will appear. Click:
```
✓ Run all
  Run before
  Run after
  ──────────────────
  ► Change runtime type  ←── Click this
  Disconnect and delete runtime
  Manage sessions
```

### Step 3: Set Hardware Accelerator to GPU
A popup window will appear with these options:

```
┌─────────────────────────────────┐
│  Notebook settings              │
├─────────────────────────────────┤
│                                 │
│  Runtime type:                  │
│  ● Python 3                     │
│                                 │
│  Hardware accelerator:          │
│  ○ None                         │
│  ● T4 GPU          ←── SELECT   │
│  ○ TPU                          │
│                                 │
│         [Cancel]  [Save]        │
│                      ↑          │
│                  Click Save     │
└─────────────────────────────────┘
```

**Important:** Select **T4 GPU**, then click **Save**

### Step 4: Verify GPU is Enabled
After saving, run the first code cell. You should see:

```
✅ GPU hardware detected!
✅ GPU: Tesla T4
✅ GPU Memory: 15.0 GB
🚀 READY TO TRAIN!
```

**If you see "NO GPU DETECTED":**
- You didn't save the settings
- Try again from Step 1
- Make sure you're in Google Colab, not running locally

---

## Common Mistakes

❌ **Running notebook locally**  
   → Open it in Google Colab instead: https://colab.research.google.com/

❌ **Selecting "None" instead of "T4 GPU"**  
   → Go back and select T4 GPU

❌ **Forgetting to click "Save"**  
   → Settings won't apply without clicking Save

❌ **Using Jupyter Notebook**  
   → Use Google Colab, not local Jupyter

---

## After Enabling GPU

1. **Run all cells**: Runtime → Run all
2. **Upload datasets** when prompted:
   - `german_to_english_120k_dataset.csv`
   - `english_to_marathi_120k_dataset.csv`
3. **Wait** ~4-6 hours for training
4. **Download** models when complete

---

## Troubleshooting

### "GPU quota exceeded"
- Free Colab has limits (~12 hours GPU per day)
- Wait 24 hours or use Colab Pro

### "Runtime disconnected"
- Colab timeouts after inactivity
- Keep browser tab open
- Re-run from last checkpoint

### "CUDA out of memory"
- Shouldn't happen with T4 (16GB)
- If it does, reduce BATCH_SIZE in training scripts

---

## Alternative: Kaggle

If Colab doesn't work, try Kaggle (also free GPU):

1. Go to https://www.kaggle.com/
2. Create new notebook
3. Settings → Accelerator → GPU
4. Upload same training scripts
5. Similar process to Colab
