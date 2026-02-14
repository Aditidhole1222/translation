"""
German to English Translation Model Fine-tuning Script
Uses Helsinki-NLP/opus-mt-de-en MarianMT model
Fine-tunes on custom German-English dataset
"""

import os
import torch
import pandas as pd
from transformers import (
    MarianMTModel,
    MarianTokenizer,
    Trainer,
    TrainingArguments,
    DataCollatorForSeq2Seq
)
from datasets import Dataset
from sklearn.model_selection import train_test_split
import evaluate

# ========================================================
# Configuration
# ========================================================

MODEL_NAME = "Helsinki-NLP/opus-mt-de-en"
DATASET_PATH = "german_to_english_10k_high_quality.csv"
OUTPUT_DIR = "./models/de_en_finetuned"
MAX_LENGTH = 128
BATCH_SIZE = 8  # Reduced for CPU compatibility
EPOCHS = 3
LEARNING_RATE = 5e-5

# Force CPU due to RTX 5060 incompatibility with PyTorch 2.6.0
# RTX 5060 has CUDA capability sm_120, but PyTorch only supports up to sm_90
device = torch.device("cpu")
print(f"🔧 Using device: CPU")
print(f"⚠️  Note: RTX 5060 (sm_120) is not compatible with PyTorch 2.6.0 (supports up to sm_90)")
print(f"⏱️  Training will take approximately 8-10 hours on CPU")

# ========================================================
# Load and Preprocess Dataset
# ========================================================

def load_and_preprocess_data(dataset_path):
    """
    Load CSV dataset and preprocess
    Only use 'german' and 'english' columns
    """
    print(f"📊 Loading dataset from {dataset_path}...")
    
    df = pd.read_csv(dataset_path)
    
    # Select only required columns (handle both capitalized and lowercase column names)
    if 'German' in df.columns and 'English' in df.columns:
        df = df[['German', 'English']]
        df.columns = ['german', 'english']  # Rename to lowercase
    elif 'german' in df.columns and 'english' in df.columns:
        df = df[['german', 'english']]
    else:
        raise ValueError(f"CSV must have columns 'German'/'german' and 'English'/'english'. Found: {df.columns.tolist()}")
    
    # Drop null rows
    df = df.dropna()
    
    # Strip whitespace
    df['german'] = df['german'].str.strip()
    df['english'] = df['english'].str.strip()
    
    # Remove empty strings
    df = df[(df['german'] != '') & (df['english'] != '')]
    
    print(f"✅ Loaded {len(df)} translation pairs")
    print(f"📝 Sample data:")
    print(df.head(3))
    
    return df

# ========================================================
# Split Data
# ========================================================

def split_data(df, test_size=0.2):
    """
    Split data into train and validation sets (80/20)
    """
    train_df, val_df = train_test_split(
        df, 
        test_size=test_size, 
        random_state=42,
        shuffle=True
    )
    
    print(f"📊 Train samples: {len(train_df)}")
    print(f"📊 Validation samples: {len(val_df)}")
    
    return train_df, val_df

# ========================================================
# Tokenization
# ========================================================

def preprocess_function(examples, tokenizer, max_length=MAX_LENGTH):
    """
    Tokenize source (German) and target (English) texts
    """
    # Tokenize inputs (source language)
    model_inputs = tokenizer(
        examples['german'],
        max_length=max_length,
        truncation=True,
        padding='max_length'
    )
    
    # Tokenize targets (target language)
    # In newer transformers, use text_target parameter instead of as_target_tokenizer()
    labels = tokenizer(
        text_target=examples['english'],
        max_length=max_length,
        truncation=True,
        padding='max_length'
    )
    
    model_inputs['labels'] = labels['input_ids']
    
    return model_inputs

# ========================================================
# Evaluation Metrics
# ========================================================

def compute_metrics(eval_preds, tokenizer):
    """
    Compute BLEU score for evaluation
    """
    bleu_metric = evaluate.load("sacrebleu")
    
    preds, labels = eval_preds
    
    # Decode predictions
    if isinstance(preds, tuple):
        preds = preds[0]
    
    # Replace -100 in labels (used for padding)
    labels = [[label if label != -100 else tokenizer.pad_token_id for label in seq] for seq in labels]
    
    decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)
    
    # Format for BLEU (references need to be in list of lists)
    decoded_labels = [[label] for label in decoded_labels]
    
    result = bleu_metric.compute(predictions=decoded_preds, references=decoded_labels)
    
    return {"bleu": result["score"]}

# ========================================================
# Main Training Pipeline
# ========================================================

def main():
    """
    Main training function
    """
    print("=" * 60)
    print("🚀 German → English Translation Model Fine-tuning")
    print("=" * 60)
    
    # Load dataset
    df = load_and_preprocess_data(DATASET_PATH)
    
    # Split data
    train_df, val_df = split_data(df)
    
    # Convert to HuggingFace Dataset
    train_dataset = Dataset.from_pandas(train_df)
    val_dataset = Dataset.from_pandas(val_df)
    
    # Load tokenizer and model
    print(f"\n🤖 Loading model: {MODEL_NAME}")
    tokenizer = MarianTokenizer.from_pretrained(MODEL_NAME)
    model = MarianMTModel.from_pretrained(MODEL_NAME)
    
    # Move model to device
    model.to(device)
    
    # Tokenize datasets
    print("\n🔄 Tokenizing datasets...")
    train_dataset = train_dataset.map(
        lambda x: preprocess_function(x, tokenizer),
        batched=True,
        remove_columns=train_dataset.column_names
    )
    
    val_dataset = val_dataset.map(
        lambda x: preprocess_function(x, tokenizer),
        batched=True,
        remove_columns=val_dataset.column_names
    )
    
    # Data collator
    data_collator = DataCollatorForSeq2Seq(
        tokenizer=tokenizer,
        model=model,
        padding=True
    )
    
    # Training arguments
    use_fp16 = torch.cuda.is_available()
    
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=LEARNING_RATE,
        per_device_train_batch_size=BATCH_SIZE,
        per_device_eval_batch_size=BATCH_SIZE,
        num_train_epochs=EPOCHS,
        weight_decay=0.01,
        save_total_limit=2,
        fp16=use_fp16,
        logging_steps=100,
        load_best_model_at_end=True,
        metric_for_best_model="bleu",
        greater_is_better=True,
        report_to="none"
    )
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        data_collator=data_collator,
        compute_metrics=lambda eval_preds: compute_metrics(eval_preds, tokenizer)
    )
    
    # Train
    print("\n🎯 Starting training...")
    trainer.train()
    
    # Evaluate
    print("\n📊 Evaluating model...")
    metrics = trainer.evaluate()
    print(f"\n✅ Final BLEU Score: {metrics['eval_bleu']:.2f}")
    
    # Save final model
    print(f"\n💾 Saving model to {OUTPUT_DIR}")
    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    
    print("\n✅ Training complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
