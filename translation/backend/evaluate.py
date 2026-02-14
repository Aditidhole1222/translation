"""
BLEU Score Evaluation Script
Evaluates translation quality using BLEU metrics
"""

import pandas as pd
import evaluate
from inference import TranslationPipeline
from tqdm import tqdm

# ========================================================
# Configuration
# ========================================================

# Evaluation datasets (subset for testing)
DE_EN_TEST_PATH = "german_to_english_120k_dataset.csv"
EN_MR_TEST_PATH = "english_to_marathi_120k_dataset.csv"
SAMPLE_SIZE = 100  # Number of samples to evaluate

# ========================================================
# Load Test Data
# ========================================================

def load_test_data(dataset_path, columns, sample_size=SAMPLE_SIZE):
    """
    Load and prepare test dataset
    
    Args:
        dataset_path: Path to CSV file
        columns: List of columns to use
        sample_size: Number of samples to evaluate
        
    Returns:
        DataFrame with test samples
    """
    print(f"📊 Loading test data from {dataset_path}...")
    
    df = pd.read_csv(dataset_path)
    df = df[columns].dropna()
    
    # Sample random data
    df_sample = df.sample(n=min(sample_size, len(df)), random_state=42)
    
    print(f"✅ Loaded {len(df_sample)} test samples")
    
    return df_sample

# ========================================================
# BLEU Score Calculation
# ========================================================

def calculate_bleu(predictions, references):
    """
    Calculate BLEU score
    
    Args:
        predictions: List of predicted translations
        references: List of reference translations
        
    Returns:
        BLEU score dictionary
    """
    bleu_metric = evaluate.load("sacrebleu")
    
    # Format references (each reference needs to be in a list)
    formatted_refs = [[ref] for ref in references]
    
    result = bleu_metric.compute(
        predictions=predictions,
        references=formatted_refs
    )
    
    return result

# ========================================================
# Evaluate German → English
# ========================================================

def evaluate_de_en(pipeline, test_df):
    """
    Evaluate German to English translation
    
    Args:
        pipeline: TranslationPipeline instance
        test_df: Test dataframe with 'german' and 'english' columns
        
    Returns:
        BLEU score and examples
    """
    print("\n" + "=" * 60)
    print("📊 Evaluating German → English Translation")
    print("=" * 60)
    
    predictions = []
    references = test_df['english'].tolist()
    
    # Generate predictions
    for german_text in tqdm(test_df['german'], desc="Translating"):
        english_pred = pipeline.translate_de_to_en(german_text)
        predictions.append(english_pred)
    
    # Calculate BLEU
    bleu_result = calculate_bleu(predictions, references)
    
    print(f"\n✅ BLEU Score: {bleu_result['score']:.2f}")
    
    # Show examples
    print("\n📝 Examples:")
    print("-" * 60)
    for i in range(min(5, len(test_df))):
        print(f"\n🇩🇪 Source:     {test_df.iloc[i]['german']}")
        print(f"🇬🇧 Reference:  {references[i]}")
        print(f"🤖 Prediction: {predictions[i]}")
    
    return bleu_result, predictions

# ========================================================
# Evaluate English → Marathi
# ========================================================

def evaluate_en_mr(pipeline, test_df):
    """
    Evaluate English to Marathi translation
    
    Args:
        pipeline: TranslationPipeline instance
        test_df: Test dataframe with 'english' and 'marathi' columns
        
    Returns:
        BLEU score and examples
    """
    print("\n" + "=" * 60)
    print("📊 Evaluating English → Marathi Translation")
    print("=" * 60)
    
    predictions = []
    references = test_df['marathi'].tolist()
    
    # Generate predictions
    for english_text in tqdm(test_df['english'], desc="Translating"):
        marathi_pred = pipeline.translate_en_to_mr(english_text)
        predictions.append(marathi_pred)
    
    # Calculate BLEU
    bleu_result = calculate_bleu(predictions, references)
    
    print(f"\n✅ BLEU Score: {bleu_result['score']:.2f}")
    
    # Show examples
    print("\n📝 Examples:")
    print("-" * 60)
    for i in range(min(5, len(test_df))):
        print(f"\n🇬🇧 Source:     {test_df.iloc[i]['english']}")
        print(f"🇮🇳 Reference:  {references[i]}")
        print(f"🤖 Prediction: {predictions[i]}")
    
    return bleu_result, predictions

# ========================================================
# Token Statistics
# ========================================================

def calculate_token_statistics(texts):
    """
    Calculate token length statistics
    
    Args:
        texts: List of text samples
        
    Returns:
        Statistics dictionary
    """
    token_lengths = [len(text.split()) for text in texts]
    
    stats = {
        "min": min(token_lengths),
        "max": max(token_lengths),
        "mean": sum(token_lengths) / len(token_lengths),
        "median": sorted(token_lengths)[len(token_lengths) // 2]
    }
    
    return stats

# ========================================================
# Main Evaluation
# ========================================================

def main():
    """
    Main evaluation function
    """
    print("=" * 60)
    print("🚀 Translation Model Evaluation")
    print("=" * 60)
    
    # Initialize pipeline
    pipeline = TranslationPipeline()
    
    # Load test data
    de_en_test = load_test_data(
        DE_EN_TEST_PATH,
        columns=['german', 'english'],
        sample_size=SAMPLE_SIZE
    )
    
    en_mr_test = load_test_data(
        EN_MR_TEST_PATH,
        columns=['english', 'marathi'],
        sample_size=SAMPLE_SIZE
    )
    
    # Evaluate DE→EN
    de_en_bleu, de_en_preds = evaluate_de_en(pipeline, de_en_test)
    
    # Evaluate EN→MR
    en_mr_bleu, en_mr_preds = evaluate_en_mr(pipeline, en_mr_test)
    
    # Token statistics
    print("\n" + "=" * 60)
    print("📊 Token Length Statistics")
    print("=" * 60)
    
    de_stats = calculate_token_statistics(de_en_test['german'].tolist())
    en_stats = calculate_token_statistics(en_mr_test['english'].tolist())
    mr_stats = calculate_token_statistics(en_mr_preds)
    
    print(f"\n🇩🇪 German:  Min={de_stats['min']}, Max={de_stats['max']}, Avg={de_stats['mean']:.1f}")
    print(f"🇬🇧 English: Min={en_stats['min']}, Max={en_stats['max']}, Avg={en_stats['mean']:.1f}")
    print(f"🇮🇳 Marathi: Min={mr_stats['min']}, Max={mr_stats['max']}, Avg={mr_stats['mean']:.1f}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 EVALUATION SUMMARY")
    print("=" * 60)
    print(f"\n✅ German → English BLEU: {de_en_bleu['score']:.2f}")
    print(f"✅ English → Marathi BLEU: {en_mr_bleu['score']:.2f}")
    
    print("\n💡 Performance Notes:")
    print("- BLEU scores above 30 indicate reasonable translation quality")
    print("- Fine-tuning improves domain-specific translations")
    print("- Cascaded translation (DE→EN→MR) may compound errors")
    print("- Consider using larger models for production deployment")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
