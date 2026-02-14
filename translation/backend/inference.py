"""
Translation Inference Module
Provides functions for German→English and English→Marathi translation
Uses fine-tuned MarianMT models or base models as fallback
"""

import os
import torch
from transformers import MarianMTModel, MarianTokenizer
from typing import List, Union

# ========================================================
# Configuration
# ========================================================

DE_EN_MODEL_PATH = "./models/de_en_finetuned_10k"
EN_MR_MODEL_PATH = "./models/en_mr_finetuned_10k"
DE_EN_BASE_MODEL = "Helsinki-NLP/opus-mt-de-en"
EN_MR_BASE_MODEL = "Helsinki-NLP/opus-mt-en-mr"
MAX_LENGTH = 128

# Force CPU to avoid RTX 5060 sm_120 incompatibility
device = torch.device("cpu")
print(f"⚠️  Using CPU (RTX 5060 GPU incompatible with PyTorch)")

# ========================================================
# Model Loader
# ========================================================

class TranslationModel:
    """
    Translation model wrapper for loading and inference
    Automatically falls back to base model if fine-tuned model not available
    """
    
    def __init__(self, model_path: str, base_model: str):
        """
        Load model and tokenizer from path or fallback to base model
        
        Args:
            model_path: Path to fine-tuned model
            base_model: HuggingFace base model name (fallback)
        """
        # Check if fine-tuned model exists (check for model.safetensors)
        model_exists = os.path.exists(model_path) and (
            os.path.exists(os.path.join(model_path, "model.safetensors")) or
            os.path.exists(os.path.join(model_path, "pytorch_model.bin"))
        )
        
        if model_exists:
            print(f"✅ Loading FINE-TUNED model from {model_path}...")
            load_path = model_path
            self.is_finetuned = True
        else:
            print(f"⚠️  Fine-tuned model not found at {model_path}")
            print(f"📥 Loading BASE model from HuggingFace: {base_model}...")
            load_path = base_model
            self.is_finetuned = False
        
        self.tokenizer = MarianTokenizer.from_pretrained(load_path)
        self.model = MarianMTModel.from_pretrained(load_path)
        self.model.to(device)
        self.model.eval()  # Set to evaluation mode
        
        if self.is_finetuned:
            print(f"✅ Fine-tuned model loaded on {device}")
        else:
            print(f"✅ Base model loaded on {device} (will work but not optimized)")
        print(f"   Use this temporarily until you download trained models from Colab")
    
    def translate(
        self, 
        texts: Union[str, List[str]], 
        max_length: int = MAX_LENGTH,
        num_beams: int = 4
    ) -> Union[str, List[str]]:
        """
        Translate text(s)
        
        Args:
            texts: Single text or list of texts to translate
            max_length: Maximum output length
            num_beams: Number of beams for beam search
            
        Returns:
            Translated text(s)
        """
        # Handle single string input
        single_input = isinstance(texts, str)
        if single_input:
            texts = [texts]
        
        # Tokenize
        inputs = self.tokenizer(
            texts,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=max_length
        ).to(device)
        
        # Generate translations
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                num_beams=num_beams,
                early_stopping=True
            )
        
        # Decode
        translations = self.tokenizer.batch_decode(
            outputs, 
            skip_special_tokens=True
        )
        
        # Return single string or list based on input
        return translations[0] if single_input else translations

# ========================================================
# Pipeline Manager
# ========================================================

class TranslationPipeline:
    """
    Complete translation pipeline: German → English → Marathi
    """
    
    def __init__(self):
        """
        Initialize translation models
        """
        print("=" * 60)
        print("🚀 Initializing Translation Pipeline")
        print("=" * 60)
        print(f"🔧 Device: {device}")
        print()
        
        # Load models (with automatic fallback to base models)
        print("📦 Loading German → English model...")
        self.de_en_model = TranslationModel(DE_EN_MODEL_PATH, DE_EN_BASE_MODEL)
        print()
        
        print("📦 Loading English → Marathi model...")
        self.en_mr_model = TranslationModel(EN_MR_MODEL_PATH, EN_MR_BASE_MODEL)
        
        print()
        print("=" * 60)
        if self.de_en_model.is_finetuned and self.en_mr_model.is_finetuned:
            print("✅ Pipeline ready with FINE-TUNED models!")
        elif self.de_en_model.is_finetuned or self.en_mr_model.is_finetuned:
            print("⚠️  Pipeline ready with PARTIAL training (1 base + 1 fine-tuned)")
        else:
            print("⚠️  Pipeline ready with BASE models (download trained models soon)")
        print("=" * 60)
    
    def translate_de_to_en(self, german_text: str) -> str:
        """
        Translate German to English
        
        Args:
            german_text: German input text
            
        Returns:
            English translation
        """
        return self.de_en_model.translate(german_text)
    
    def translate_en_to_mr(self, english_text: str) -> str:
        """
        Translate English to Marathi
        
        Args:
            english_text: English input text
            
        Returns:
            Marathi translation
        """
        return self.en_mr_model.translate(english_text)
    
    def translate_de_to_mr(self, german_text: str) -> dict:
        """
        Complete pipeline: German → English → Marathi
        
        Args:
            german_text: German input text
            
        Returns:
            Dictionary with all translation stages
        """
        # Step 1: German to English
        english_text = self.translate_de_to_en(german_text)
        
        # Step 2: English to Marathi
        marathi_text = self.translate_en_to_mr(english_text)
        
        return {
            "german": german_text,
            "english": english_text,
            "marathi": marathi_text
        }

# ========================================================
# Standalone Testing
# ========================================================

def main():
    """
    Test translation pipeline
    """
    # Initialize pipeline
    pipeline = TranslationPipeline()
    
    # Test cases
    test_sentences = [
        "Guten Morgen! Wie geht es dir?",
        "Ich lerne Deutsch.",
        "Das Wetter ist heute schön."
    ]
    
    print("\n" + "=" * 60)
    print("🧪 Testing Translation Pipeline")
    print("=" * 60)
    
    for german_text in test_sentences:
        result = pipeline.translate_de_to_mr(german_text)
        
        print(f"\n🇩🇪 German:  {result['german']}")
        print(f"🇬🇧 English: {result['english']}")
        print(f"🇮🇳 Marathi: {result['marathi']}")
        print("-" * 60)

if __name__ == "__main__":
    main()
