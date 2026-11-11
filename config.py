# --- PRE-TRAINED MODEL CONFIGURATIONS ---

# 1. Semantic Relevance Scoring (Cross-Encoder for high-accuracy document ranking)
CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# 2. Dynamic Keyword/Skill Extraction (Bi-Encoder for KeyBERT)
KEYBERT_MODEL = "all-MiniLM-L6-v2"

# System Settings
TOP_K_KEYWORDS = 15
MATCH_THRESHOLD = 50.0
