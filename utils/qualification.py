"""
AI Recruiter Pro - Qualification & Experience Screening Module
Extracts years of experience, target company/domain matches, and education credentials from resumes.
"""

import re
from typing import Dict, Any, List, Optional

class QualificationMatcher:
    @staticmethod
    def extract_years_of_experience(text: str) -> float:
        """
        Extracts the highest or most relevant years of experience mentioned in the text,
        or calculates based on date ranges found.
        """
        # Pattern 1: Direct mentions like "5+ years experience", "6 years of experience", "4 yrs experience"
        patterns = [
            r'(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)(?:\s+(?:of\s+)?experience|\s+in\b)',
            r'(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)\s+building',
            r'(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)\s+working',
            r'(?:experience|background)\s*:\s*(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)',
            r'summary\s*:\s*(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)',
        ]
        
        found_years = []
        for pat in patterns:
            matches = re.findall(pat, text, re.IGNORECASE)
            for m in matches:
                try:
                    val = float(m)
                    if 0.5 <= val <= 35:  # Realistic filter
                        found_years.append(val)
                except ValueError:
                    continue

        if found_years:
            return max(found_years)

        # Fallback: scan for year ranges like (2018 - Present) or (2019 - 2023)
        year_ranges = re.findall(r'\b(20\d\d|19\d\d)\s*[-–—to]+\s*(Present|Current|20\d\d)\b', text, re.IGNORECASE)
        total_span = 0.0
        current_year = 2026 # Context year
        for start, end in year_ranges:
            try:
                s_yr = int(start)
                e_yr = current_year if end.lower() in ['present', 'current'] else int(end)
                diff = max(0, e_yr - s_yr)
                if diff <= 30:
                    total_span = max(total_span, float(diff))
            except ValueError:
                continue

        return total_span

    @staticmethod
    def extract_education(text: str) -> str:
        """Detects the highest academic degree mentioned."""
        lower = text.lower()
        if re.search(r'\b(ph\.?d|doctorate|doctor of philosophy)\b', lower):
            return "PhD / Doctorate"
        elif re.search(r'\b(master\'?s|m\.?s|m\.?tech|m\.?sc|mba)\b', lower):
            return "Master's Degree"
        elif re.search(r'\b(bachelor\'?s|b\.?s|b\.?tech|b\.?e|b\.?sc|undergraduate)\b', lower):
            return "Bachelor's Degree"
        return "Not Explicitly Specified"

    @staticmethod
    def match_target_companies(text: str, target_companies_str: str) -> List[str]:
        """Checks if candidate worked at or mentions any of the requested target companies/domains."""
        if not target_companies_str.strip():
            return []
        
        targets = [t.strip() for t in re.split(r'[,;\n/]+', target_companies_str) if t.strip()]
        matched = []
        for company in targets:
            # Word boundary regex search
            escaped = re.escape(company)
            if re.search(rf'\b{escaped}\b', text, re.IGNORECASE):
                matched.append(company)
        return matched

    @classmethod
    def evaluate_qualifications(
        cls, 
        resume_text: str, 
        min_experience_required: int = 0, 
        target_companies: str = "",
        required_degree: str = "Any"
    ) -> Dict[str, Any]:
        """
        Evaluates candidate against explicit qualification criteria.
        """
        detected_exp = cls.extract_years_of_experience(resume_text)
        detected_edu = cls.extract_education(resume_text)
        matched_companies = cls.match_target_companies(resume_text, target_companies)
        
        # 1. Experience Check
        meets_exp = detected_exp >= min_experience_required if min_experience_required > 0 else True
        if min_experience_required > 0:
            exp_status = f"✅ {detected_exp:.1f} yrs (Meets {min_experience_required}+ yr requirement)" if meets_exp else f"⚠️ {detected_exp:.1f} yrs (Under {min_experience_required} yr requirement)"
        else:
            exp_status = f"{detected_exp:.1f} yrs detected" if detected_exp > 0 else "Experience not explicitly quantified"

        # 2. Company / Domain Check
        has_target_companies = bool(target_companies.strip())
        meets_company = bool(matched_companies) if has_target_companies else True

        # 3. Education Check
        meets_degree = True
        if required_degree != "Any":
            degree_order = {"Bachelor's Degree": 1, "Master's Degree": 2, "PhD / Doctorate": 3}
            cand_lvl = degree_order.get(detected_edu, 0)
            req_lvl = degree_order.get(required_degree, 1)
            meets_degree = cand_lvl >= req_lvl

        # Qualification Bonus / Penalty multiplier
        qual_score_factor = 1.0
        if min_experience_required > 0:
            if meets_exp:
                qual_score_factor += 0.05
            else:
                deficit = min_experience_required - detected_exp
                penalty = min(0.20, (deficit / min_experience_required) * 0.15)
                qual_score_factor -= penalty

        if has_target_companies:
            if meets_company:
                qual_score_factor += 0.08
            else:
                qual_score_factor -= 0.05

        return {
            "detected_experience": detected_exp,
            "meets_experience": meets_exp,
            "exp_status": exp_status,
            "detected_education": detected_edu,
            "meets_degree": meets_degree,
            "matched_companies": matched_companies,
            "target_companies_configured": has_target_companies,
            "meets_company": meets_company,
            "qual_score_factor": qual_score_factor
        }

