from keybert import KeyBERT
from config import KEYBERT_MODEL

class KeywordExtractor:
    def __init__(self):
        # Uses pre-trained HuggingFace models for dynamic extraction
        self.kw_model = KeyBERT(model=KEYBERT_MODEL)

    def extract_keywords(self, text: str, top_n: int = 15) -> set:
        # Extracts context-aware keyphrases (1 to 2 words)
        keywords = self.kw_model.extract_keywords(
            text, 
            keyphrase_ngram_range=(1, 2), 
            stop_words='english', 
            top_n=top_n
        )
        return {kw[0].lower() for kw in keywords}
