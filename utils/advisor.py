"""
AI Recruiter Pro - Strategic Hiring Advisor Module
Generates actionable recruiter insights, risk evaluations, and interview questions
based on semantic score and skill gap analysis.
"""

from typing import List, Dict, Any

class RecruiterAdvisor:
    @staticmethod
    def generate_advice(candidate_name: str, eval_data: Dict[str, Any], jd_text: str) -> Dict[str, Any]:
        score = eval_data.get("score", 0.0)
        semantic_score = eval_data.get("semantic_score", 0.0)
        skill_ratio = eval_data.get("skill_match_ratio", 0.0)
        matched_skills: List[str] = eval_data.get("matched_skills", [])
        missing_skills: List[str] = eval_data.get("missing_skills", [])

        # 1. Hiring Verdict
        if score >= 80:
            verdict = "🚀 Strong Hire / Fast Track"
            verdict_badge = "badge-emerald"
            action_plan = "Fast-track candidate directly to the technical panel round. High domain alignment and strong keyword coverage."
        elif score >= 65:
            verdict = "✅ Recommend for Technical Screen"
            verdict_badge = "badge-blue"
            action_plan = "Solid match for the role. Schedule a 45-minute technical deep dive focusing on architecture and gap areas."
        elif score >= 50:
            verdict = "⚖️ Borderline / Conditional Review"
            verdict_badge = "badge-amber"
            action_plan = "Candidate demonstrates relevant background but lacks several core proficiencies specified in the job description."
        else:
            verdict = "⏸️ Low Alignment / Keep on File"
            verdict_badge = "badge-rose"
            action_plan = "Significant deviation from required prerequisites. Recommend reviewing alternate requisitions or archiving."

        # 2. Key Strengths Analysis
        strengths = []
        qual = eval_data.get("qualifications", {})
        if qual.get("matched_companies"):
            top_co = ", ".join(qual["matched_companies"])
            strengths.append(f"Target company / industry background: Verified experience with **{top_co}**.")
        if qual.get("meets_experience") and qual.get("detected_experience", 0) >= 5:
            strengths.append(f"Strong seniority track record ({qual.get('detected_experience', 0):.1f}+ years hands-on experience).")
        if semantic_score >= 70:
            strengths.append(f"Strong overall domain semantics ({semantic_score:.1f}% context match) - candidate has worked in closely related problem spaces.")
        if matched_skills:
            top_matched = ", ".join([f"**{s}**" for s in matched_skills[:5]])
            strengths.append(f"Verified core skills found in resume: {top_matched}.")
        if skill_ratio >= 75:
            strengths.append(f"High technical prerequisite match ({skill_ratio:.1f}% requirements covered).")
        if not strengths:
            strengths.append("Found foundational background; further screening required to identify transferable skills.")

        # 3. Risks & Gaps to Probe
        risks = []
        if qual.get("target_companies_configured") and not qual.get("meets_company"):
            risks.append("Candidate does not list direct background from the requested target companies/domains.")
        if qual.get("detected_experience", 0) > 0 and not qual.get("meets_experience"):
            risks.append(f"Tenure discrepancy: Estimated ~{qual.get('detected_experience', 0):.1f} yrs experience, below the specified threshold.")
        if missing_skills:
            top_missing = ", ".join([f"**{s}**" for s in missing_skills[:6]])
            risks.append(f"Missing mentions for required skills: {top_missing}.")
        if semantic_score > skill_ratio + 25:
            risks.append("Candidate narrative sounds relevant conceptually, but lacks explicit execution tooling or specific required tech stack.")
        elif skill_ratio > semantic_score + 25:
            risks.append("Candidate lists matching buzzwords, but context similarity scored lower - verify hands-on architectural depth vs surface-level keywords.")
        if not risks:
            risks.append("No critical gaps identified against the provided job specification.")

        # 4. Tailored Interview Questions
        questions = []
        # Question based on matched skill depth
        if matched_skills:
            lead_skill = matched_skills[0].title()
            questions.append(
                f"**Hands-On Architecture ({lead_skill}):** 'Can you walk us through the most challenging production system you designed using {lead_skill}? What trade-offs did you face regarding scalability and performance?'"
            )
        # Question based on missing skills / adaptability
        if missing_skills:
            probe_skill = missing_skills[0].title()
            questions.append(
                f"**Competency Gap Probe ({probe_skill}):** 'The role heavily involves {probe_skill}, which wasn't prominently featured on your resume. What is your exposure to it, and how have you navigated adopting adjacent technologies quickly?'"
            )
        # Situational / System impact question
        questions.append(
            "**System Impact & Leadership:** 'Describe a situation where a project requirement shifted abruptly mid-sprint. How did you realign technical priorities without compromising quality?'"
        )

        # 5. Executive Summary for Hiring Manager
        summary = (
            f"**Candidate Summary for {candidate_name}:** Overall match rating of **{score:.1f}%** "
            f"(Semantic Context: {semantic_score:.1f}%, Prerequisite Keyword Coverage: {skill_ratio:.1f}%). "
            f"{'Candidate demonstrates high compatibility with the core JD.' if score >= 70 else 'Candidate offers partial overlap; review interview gap questions before advancing.'}"
        )

        return {
            "verdict": verdict,
            "verdict_badge": verdict_badge,
            "action_plan": action_plan,
            "strengths": strengths,
            "risks": risks,
            "questions": questions,
            "summary": summary
        }

    @staticmethod
    def generate_html_dossier(candidate_name: str, eval_data: Dict[str, Any], advice: Dict[str, Any], jd_title: str = "Target Position") -> str:
        score = eval_data.get("score", 0.0)
        semantic = eval_data.get("semantic_score", 0.0)
        keywords_ratio = eval_data.get("skill_match_ratio", 0.0)
        matched_skills = eval_data.get("matched_skills", [])
        missing_skills = eval_data.get("missing_skills", [])

        matched_pills = "".join([f'<span style="display:inline-block; background:#dcfce7; color:#166534; padding:4px 10px; border-radius:12px; font-size:12px; margin:2px 4px 2px 0; font-weight:600;">✓ {s}</span>' for s in matched_skills]) or "None detected"
        missing_pills = "".join([f'<span style="display:inline-block; background:#fee2e2; color:#991b1b; padding:4px 10px; border-radius:12px; font-size:12px; margin:2px 4px 2px 0; font-weight:600;">✕ {s}</span>' for s in missing_skills[:12]]) or "None"

        strengths_li = "".join([f'<li style="margin-bottom:6px;">{s.replace("**", "<b>").replace("**", "</b>")}</li>' for s in advice.get("strengths", [])])
        risks_li = "".join([f'<li style="margin-bottom:6px;">{r.replace("**", "<b>").replace("**", "</b>")}</li>' for s in advice.get("risks", [])])
        questions_blocks = "".join([
            f'<div style="background:#f8fafc; border-left:4px solid #4f46e5; padding:10px 14px; margin-bottom:10px; border-radius:0 8px 8px 0;">'
            f'<div style="font-size:12px; color:#4f46e5; font-weight:700;">Question {i}</div>'
            f'<div style="font-size:13px; color:#1e293b; margin-top:2px;">{q.replace("**", "<b>").replace("**", "</b>")}</div>'
            f'</div>'
            for i, q in enumerate(advice.get("questions", []), 1)
        ])

        return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>AI Recruiter Evaluation: {candidate_name}</title>
<style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; color: #0f172a; margin: 0; padding: 30px; background: #ffffff; }}
    .container {{ max-width: 800px; margin: 0 auto; }}
    .header {{ border-bottom: 2px solid #e2e8f0; padding-bottom: 16px; margin-bottom: 24px; }}
    .badge {{ display: inline-block; padding: 6px 14px; border-radius: 6px; font-weight: bold; font-size: 13px; background: #e0e7ff; color: #3730a3; }}
    .metric-row {{ display: flex; gap: 16px; margin: 20px 0; }}
    .metric-box {{ flex: 1; padding: 14px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; text-align: center; }}
    .metric-val {{ font-size: 26px; font-weight: 800; color: #4f46e5; }}
    .metric-lbl {{ font-size: 12px; color: #64748b; font-weight: 600; text-transform: uppercase; }}
    h3 {{ color: #1e293b; margin-top: 24px; margin-bottom: 10px; border-bottom: 1px solid #f1f5f9; padding-bottom: 6px; }}
    @media print {{ body {{ padding: 0; }} .no-print {{ display: none; }} }}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <div style="font-size: 12px; text-transform: uppercase; letter-spacing: 1px; color: #64748b; font-weight: 700;">AI Recruiter Pro • Interview Dossier</div>
        <h1 style="margin: 6px 0 4px 0; font-size: 28px; color: #0f172a;">{candidate_name}</h1>
        <div style="color: #64748b; font-size: 14px;">Evaluation Benchmark for <b>{jd_title}</b></div>
    </div>

    <div style="margin-bottom: 16px;">
        <span class="badge">Verdict: {advice.get('verdict', 'Under Review')}</span>
        <span style="font-size: 13px; color: #475569; margin-left: 10px;">{advice.get('action_plan', '')}</span>
    </div>

    <div class="metric-row">
        <div class="metric-box">
            <div class="metric-val">{score:.1f}%</div>
            <div class="metric-lbl">Overall Composite Match</div>
        </div>
        <div class="metric-box">
            <div class="metric-val">{semantic:.1f}%</div>
            <div class="metric-lbl">Semantic AI Alignment</div>
        </div>
        <div class="metric-box">
            <div class="metric-val">{keywords_ratio:.1f}%</div>
            <div class="metric-lbl">Required Skills Coverage</div>
        </div>
    </div>

    <h3>✅ Verified Technical Competencies</h3>
    <div style="margin-bottom: 16px;">{matched_pills}</div>

    <h3>⚠️ Competency Gaps</h3>
    <div style="margin-bottom: 16px;">{missing_pills}</div>

    <h3>🌟 Key Candidate Strengths</h3>
    <ul>{strengths_li}</ul>

    <h3>🎯 Recommended Interview Questions</h3>
    {questions_blocks}

    <h3>📝 Executive Note for Interviewers</h3>
    <div style="background: #f1f5f9; padding: 12px 16px; border-radius: 6px; font-size: 13px; line-height: 1.5; color: #334155;">
        {advice.get('summary', '')}
    </div>

    <div style="margin-top: 30px; text-align: center;" class="no-print">
        <button onclick="window.print()" style="background:#4f46e5; color:#fff; border:none; padding:10px 24px; border-radius:6px; font-weight:600; cursor:pointer;">🖨️ Print or Save as PDF</button>
    </div>
</div>
</body>
</html>"""

