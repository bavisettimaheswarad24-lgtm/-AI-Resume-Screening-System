import torch
import numpy as np
from sentence_transformers import CrossEncoder
from config import CROSS_ENCODER_MODEL

class AdvancedScreeningEngine:
    def __init__(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        # CrossEncoders process query & document simultaneously for superior accuracy
        self.encoder = CrossEncoder(CROSS_ENCODER_MODEL, device=device)

    def calculate_relevance(self, jd_text: str, resume_text: str) -> float:
        # Returns a logit score
        score = self.encoder.predict([jd_text, resume_text])
        # Convert logit to probability (0 to 1) using sigmoid
        prob = 1 / (1 + np.exp(-score))
        return float(prob)
        
    def evaluate_candidate(self, jd_text: str, resume_text: str, jd_skills: set, resume_skills: set, semantic_weight: float = 0.70, keyword_weight: float = 0.30, qual_data: dict = None) -> dict:
        semantic_score = self.calculate_relevance(jd_text, resume_text)
        
        # Keyword Overlap Logic
        matched_skills = jd_skills.intersection(resume_skills)
        missing_skills = jd_skills - resume_skills
        skill_ratio = len(matched_skills) / len(jd_skills) if jd_skills else 1.0

        # Weighted composite score based on customizable weights
        total_weight = (semantic_weight + keyword_weight) or 1.0
        norm_semantic = semantic_weight / total_weight
        norm_keyword = keyword_weight / total_weight
        base_score = (norm_semantic * semantic_score + norm_keyword * skill_ratio) * 100

        # Apply qualification adjustment factor if experience/company filters are active
        factor = qual_data.get("qual_score_factor", 1.0) if qual_data else 1.0
        final_score = min(100.0, max(0.0, base_score * factor))

        return {
            "score": round(final_score, 2),
            "semantic_score": round(semantic_score * 100, 2),
            "skill_match_ratio": round(skill_ratio * 100, 2),
            "matched_skills": sorted(list(matched_skills)),
            "missing_skills": sorted(list(missing_skills)),
            "qualifications": qual_data or {}
        }
