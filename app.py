import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from utils.parser import extract_text_from_file
from utils.extractor import KeywordExtractor
from utils.advisor import RecruiterAdvisor
from utils.qualification import QualificationMatcher
from matcher.model import AdvancedScreeningEngine

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Recruiter Pro | Enterprise Talent Intelligence",
    layout="wide",
    page_icon="⚡",
    initial_sidebar_state="collapsed"
)

# --- MODERN STYLING & GLASSMORPHISM CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Ambient background with mesh glow */
    .stApp {
        background-color: #07090e;
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(79, 70, 229, 0.15) 0%, transparent 45%),
            radial-gradient(circle at 90% 15%, rgba(147, 51, 234, 0.12) 0%, transparent 40%),
            radial-gradient(circle at 50% 90%, rgba(16, 185, 129, 0.10) 0%, transparent 50%);
        background-attachment: fixed;
        color: #f1f5f9;
    }

    /* Floating Card Effect */
    .floating-card {
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 12px 35px -8px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.08);
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
        margin-bottom: 20px;
    }

    .floating-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 18px 45px -10px rgba(99, 102, 241, 0.25);
        border-color: rgba(99, 102, 241, 0.35);
    }

    /* Hero Header */
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.2));
        border: 1px solid rgba(139, 92, 246, 0.35);
        border-radius: 9999px;
        padding: 6px 16px;
        font-size: 13px;
        font-weight: 700;
        color: #c7d2fe;
        letter-spacing: 0.6px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    .hero-title {
        font-family: 'Outfit', sans-serif;
        font-size: 42px;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -1px;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 16px;
        margin-top: 6px;
        margin-bottom: 22px;
        font-weight: 400;
    }

    /* Engaging Company Showcase with Official Brand Visuals */
    .company-showcase {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 16px 24px;
        margin-bottom: 26px;
    }

    .company-showcase-title {
        color: #94a3b8;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .company-grid {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        flex-wrap: wrap;
    }

    .company-card {
        display: flex;
        align-items: center;
        gap: 12px;
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 10px 18px;
        transition: all 0.25s ease;
    }

    .company-card:hover {
        background: rgba(30, 41, 59, 0.85);
        border-color: rgba(99, 102, 241, 0.4);
        transform: translateY(-2px);
    }

    .company-card svg {
        width: 26px;
        height: 26px;
        flex-shrink: 0;
    }

    .company-name {
        font-size: 14px;
        font-weight: 700;
        color: #f1f5f9;
        letter-spacing: 0.2px;
    }

    /* Metric Grid */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 18px;
        margin: 20px 0;
    }

    .metric-tile {
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px;
        text-align: left;
        position: relative;
        overflow: hidden;
        transition: all 0.2s ease;
    }

    .metric-tile:hover {
        border-color: rgba(99, 102, 241, 0.4);
        transform: translateY(-2px);
    }

    .metric-tile::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #6366f1, #10b981);
    }

    .metric-number {
        font-family: 'Outfit', sans-serif;
        font-size: 34px;
        font-weight: 700;
        color: #ffffff;
        margin: 4px 0;
    }

    .metric-desc {
        color: #94a3b8;
        font-size: 13px;
        font-weight: 500;
    }

    /* Badges */
    .badge-pill {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.3px;
        margin: 3px 4px 3px 0;
    }

    .badge-matched {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }

    .badge-missing {
        background: rgba(244, 63, 94, 0.15);
        color: #fb7185;
        border: 1px solid rgba(244, 63, 94, 0.3);
    }

    .badge-emerald {
        background: rgba(16, 185, 129, 0.18);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.35);
        padding: 6px 14px;
        font-size: 13px;
        font-weight: 700;
        border-radius: 8px;
    }

    .badge-blue {
        background: rgba(59, 130, 246, 0.18);
        color: #60a5fa;
        border: 1px solid rgba(59, 130, 246, 0.35);
        padding: 6px 14px;
        font-size: 13px;
        font-weight: 700;
        border-radius: 8px;
    }

    .badge-amber {
        background: rgba(245, 158, 11, 0.18);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.35);
        padding: 6px 14px;
        font-size: 13px;
        font-weight: 700;
        border-radius: 8px;
    }

    .badge-rose {
        background: rgba(239, 68, 68, 0.18);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.35);
        padding: 6px 14px;
        font-size: 13px;
        font-weight: 700;
        border-radius: 8px;
    }

    /* Advice box */
    .advice-container {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 16px;
        padding: 22px;
        margin-top: 14px;
    }

    .advice-title {
        font-family: 'Outfit', sans-serif;
        font-size: 20px;
        font-weight: 700;
        color: #c7d2fe;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #4f46e5 0%, #6366f1 50%, #7c3aed 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 28px !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        letter-spacing: 0.3px !important;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.35) !important;
        transition: all 0.2s ease !important;
    }

    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.5) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- LOAD MODELS (CACHED & LAZY LOADED ON DEMAND) ---
@st.cache_resource(show_spinner="⚡ Initializing AI Neural Models (Cross-Encoder & KeyBERT)...")
def get_models():
    import gc
    import torch
    try:
        torch.set_num_threads(1)
    except Exception:
        pass
    eng = AdvancedScreeningEngine()
    ext = KeywordExtractor()
    gc.collect()
    return eng, ext

# --- TOP NAVIGATION & HEADER ---
st.markdown("""
<div style="margin-bottom: 18px;">
    <div class="hero-badge">⚡ Enterprise AI Talent Intelligence</div>
    <h1 class="hero-title">AI Recruiter Pro</h1>
    <p class="hero-subtitle">Cross-Encoder Deep Semantic Transformer • KeyBERT Extraction • Advanced Data Visualizations • Strategic Hiring Advisor</p>
</div>
""", unsafe_allow_html=True)

# --- ENGAGING COMPANY SHOWCASE WITH OFFICIAL HIGH-RES LOGOS ---
st.markdown("""
<div class="company-showcase">
    <div class="company-showcase-title">
        Benchmarked Against Talent Criteria At Leading Tech Organizations
    </div>
    <div class="company-grid">
        <!-- Google -->
        <div class="company-card">
            <svg viewBox="0 0 48 48">
                <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
                <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
                <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>
                <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
            </svg>
            <span class="company-name">Google</span>
        </div>
        <!-- Microsoft -->
        <div class="company-card">
            <svg viewBox="0 0 23 23">
                <path fill="#f35325" d="M1 1h10v10H1z"/>
                <path fill="#81bc06" d="M12 1h10v10H12z"/>
                <path fill="#05a6f0" d="M1 12h10v10H1z"/>
                <path fill="#ffba08" d="M12 12h10v10H12z"/>
            </svg>
            <span class="company-name">Microsoft</span>
        </div>
        <!-- Meta -->
        <div class="company-card">
            <svg viewBox="0 0 40 40">
                <defs>
                    <linearGradient id="meta-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#0064e0"/>
                        <stop offset="50%" stop-color="#0082fb"/>
                        <stop offset="100%" stop-color="#00b2ff"/>
                    </linearGradient>
                </defs>
                <path fill="url(#meta-grad)" d="M20 12c-5.2 0-9.2 3.6-11.8 7.3C6.3 22 5 24.3 5 26.5 5 30.1 7.6 32 10.9 32c3.1 0 5.6-2 7.7-5.1 1.1-1.6 2.1-3.3 3.4-3.3s2.3 1.7 3.4 3.3c2.1 3.1 4.6 5.1 7.7 5.1 3.3 0 5.9-1.9 5.9-5.5 0-2.2-1.3-4.5-3.2-7.2-2.6-3.7-6.6-7.3-11.8-7.3zm0 4.2c3.4 0 6.6 2.8 8.8 6 1.4 2 2.2 3.6 2.2 4.6 0 1.5-1 2.3-2.6 2.3-2.1 0-3.9-1.7-5.4-3.9-1.5-2.2-2.3-4-3-6.2v-.8c0-.6 0-1.2 0-2zm-2.4 2.8c-.7 2.2-1.5 4-3 6.2-1.5 2.2-3.3 3.9-5.4 3.9-1.6 0-2.6-.8-2.6-2.3 0-1 .8-2.6 2.2-4.6 2.2-3.2 5.4-6 8.8-6v2.8z"/>
            </svg>
            <span class="company-name">Meta</span>
        </div>
        <!-- Amazon -->
        <div class="company-card">
            <svg viewBox="0 0 40 40">
                <path fill="#FF9900" d="M26.2 31c-7.2 4.6-17.5 7-26 2.4-.4-.2-.5-.8-.1-1.1 5.6-4.5 12.8-7.1 20.2-7.1 2.2 0 4.4.2 6.5.6.7.2.9.9.4 1.3l-1 .9z"/>
                <path fill="#FF9900" d="M29.5 27.6c-.6-.7-3.8-.4-5.2-.2-.4.1-.5-.3-.1-.6 2.6-1.7 6.8-1.2 7.3-.6.6.7-.2 4.9-2.6 6.9-.4.3-.7.1-.5-.3.8-1.3 1.7-4.5 1.1-5.2z"/>
                <path fill="#FFFFFF" d="M20.5 7.5C14.7 7.5 10 11.8 10 17.1c0 3.2 1.8 6.1 4.5 7.7.4.2.8.1.9-.3l1.1-1.6c.1-.2.1-.5-.1-.7-1.7-1.2-2.7-2.9-2.7-4.8 0-3.5 3-6.4 6.8-6.4s6.8 2.9 6.8 6.4c0 1.9-1 3.6-2.7 4.8-.2.2-.2.5-.1.7l1.1 1.6c.1.4.5.5.9.3 2.7-1.6 4.5-4.5 4.5-7.7 0-5.3-4.7-9.6-10.5-9.6z"/>
            </svg>
            <span class="company-name">Amazon</span>
        </div>
        <!-- NVIDIA -->
        <div class="company-card">
            <svg viewBox="0 0 40 40">
                <path fill="#76B900" d="M19.7 10c-5.8 0-10.5 4.7-10.5 10.5s4.7 10.5 10.5 10.5c3.2 0 6.1-1.5 8.1-3.8.4-.5.3-1.2-.2-1.6l-1.3-1c-.4-.3-1-.3-1.4.1-1.4 1.4-3.2 2.3-5.2 2.3-4.1 0-7.5-3.4-7.5-7.5s3.4-7.5 7.5-7.5c2.7 0 5 1.4 6.3 3.6.3.5.9.6 1.4.3l1.5-1c.5-.3.6-.9.3-1.4C26.9 11.8 23.5 10 19.7 10z"/>
            </svg>
            <span class="company-name">NVIDIA</span>
        </div>
        <!-- OpenAI -->
        <div class="company-card">
            <svg viewBox="0 0 40 40">
                <path fill="#10A37F" d="M35.6 17.3c-.5-3.1-2.6-5.6-5.5-6.6-.7-.2-1.3-.3-2-.3-.5-2.6-2.3-4.8-4.7-5.8-3.3-1.4-7.1-.5-9.4 2.1-.8-.3-1.6-.4-2.4-.4-3.4 0-6.5 2.1-7.7 5.2-2.1 1.3-3.4 3.6-3.4 6.1 0 1.2.3 2.3.9 3.3-.5 3.1 1.6 6.1 4.7 6.8.7.2 1.3.3 2 .3.5 2.6 2.3 4.8 4.7 5.8 1.4.6 2.9.8 4.4.8 2.1 0 4.1-.7 5.7-2 .8.3 1.6.4 2.4.4 3.4 0 6.5-2.1 7.7-5.2 2.1-1.3 3.4-3.6 3.4-6.1 0-1.5-.5-2.9-1.4-4.1l-.8-.4zM20 28.5c-4.7 0-8.5-3.8-8.5-8.5s3.8-8.5 8.5-8.5 8.5 3.8 8.5 8.5-3.8 8.5-8.5 8.5z"/>
            </svg>
            <span class="company-name">OpenAI</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- SAMPLE DATASET ---
DEMO_JD = """Senior Machine Learning Engineer (Generative AI & Search)
We are seeking a Senior Machine Learning Engineer with 4+ years of production experience to architect our next-generation neural search and LLM application stack.
Requirements:
- Deep expertise in Python, PyTorch, Transformers, HuggingFace, and Sentence-Transformers
- Production experience with Vector Databases (Milvus, Pinecone, Qdrant) and Retrieval-Augmented Generation (RAG)
- Strong background in Semantic Search, Cross-Encoders, Re-ranking algorithms, and NLP model evaluation
- Hands-on proficiency with Docker, Kubernetes, FastAPI, CI/CD pipelines, and AWS cloud infrastructure
- Master's or Bachelor's degree in Computer Science, Data Science, or related STEM field"""

DEMO_RESUMES = {
    "Alex_Rivers_Senior_MLE.pdf": """Alex Rivers - Senior ML Engineer
Email: alex.rivers@example.com | San Francisco, CA
SUMMARY: 5+ years experience building production neural search engines and LLM systems at scale.
SKILLS: Python, PyTorch, Transformers, HuggingFace, Sentence-Transformers, Vector Databases, Pinecone, RAG, Semantic Search, Cross-Encoders, Docker, Kubernetes, FastAPI, AWS.
EXPERIENCE:
Staff Machine Learning Engineer at TechCorp (2022 - Present):
- Designed and deployed end-to-end RAG semantic search architecture serving 15M monthly active users using PyTorch, HuggingFace, and Pinecone vector store.
- Reduced inference latency by 45% using model distillation and quantization techniques with Docker and Kubernetes on AWS.
- Led cross-encoder reranking integration improving Top-3 retrieval NDCG from 0.68 to 0.89.""",

    "Jordan_Lee_Data_Scientist.pdf": """Jordan Lee - Senior Data Scientist
Email: jordan.lee@example.com | New York, NY
SUMMARY: 4 years experience in NLP, statistical modeling, and customer analytics.
SKILLS: Python, Pandas, Scikit-Learn, PyTorch, NLP, SQL, Tableau, HuggingFace, BERT, Docker, Git, GCP.
EXPERIENCE:
Senior NLP Data Scientist at DataPulse (2021 - Present):
- Trained domain-specific BERT and classification transformers for sentiment analysis and customer topic modeling.
- Built automated reporting pipelines with Python, Docker, and Google Cloud BigQuery.
- Collaborated with engineering teams to containerize ML inference services using FastAPI.""",

    "Sam_Taylor_FullStack_Dev.pdf": """Sam Taylor - Senior Full Stack Developer
Email: sam.taylor@example.com | Austin, TX
SUMMARY: 6 years building modern scalable web applications, microservices, and React frontends.
SKILLS: JavaScript, TypeScript, React, Node.js, Express, PostgreSQL, MongoDB, Docker, AWS, Python, Redis.
EXPERIENCE:
Senior Full Stack Engineer at CloudScale (2020 - Present):
- Built high-performance microservices and RESTful APIs using Node.js, TypeScript, and PostgreSQL.
- Architected event-driven distributed systems using Redis queues and AWS ECS.
- Explored OpenAI API integrations for automated document summarization features."""
}

# --- INPUT SECTION (FLOATING CARDS) ---
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="floating-card">', unsafe_allow_html=True)
    st.markdown("### 📋 Job Requirements Specification")
    st.caption("Paste the requisition description or benchmark requirements.")
    jd_input = st.text_area("Job Description (JD)", height=230, placeholder="e.g. Senior Machine Learning Engineer with Python, PyTorch, Transformers, Vector DBs, and FastAPI...")
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="floating-card">', unsafe_allow_html=True)
    st.markdown("### 📂 Candidate Talent Pool")
    st.caption("Upload PDF, DOCX, or TXT resumes for multi-candidate evaluation.")
    uploaded_files = st.file_uploader("Upload Resumes (PDF / DOCX / TXT)", type=["pdf", "docx", "txt"], accept_multiple_files=True)
    st.caption("Tip: You can upload multiple resumes simultaneously to rank and benchmark candidates.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- REQUISITION QUALIFICATIONS & TARGET CRITERIA (OPTIONAL) ---
st.markdown('<div class="floating-card">', unsafe_allow_html=True)
st.markdown("### 🎯 Mandatory Qualifications & Experience Requirements (Optional)")
st.caption("Benchmark candidates against specific years of experience, target company backgrounds, and academic degrees.")
col_q1, col_q2, col_q3 = st.columns([1, 1.6, 1.2])
with col_q1:
    min_exp_input = st.number_input("Minimum Experience (Years)", min_value=0, max_value=25, value=4, step=1, help="Flag candidates with less than this experience.")
with col_q2:
    target_companies_input = st.text_input("Target Companies or Domain Keywords", value="TechCorp, DataPulse, Google, Tier-1", placeholder="e.g. Google, Amazon, TechCorp, FinTech, Tier-1", help="Comma-separated list of companies/industries candidates should have worked in.")
with col_q3:
    req_degree_input = st.selectbox("Minimum Degree Qualification", ["Any Degree", "Bachelor's Degree", "Master's Degree", "PhD / Doctorate"], index=0)
st.markdown('</div>', unsafe_allow_html=True)

# Run Button
run_analysis = st.button("🚀 Run Deep Semantic Analysis & Strategic Ranking", use_container_width=True)

# --- EXECUTION ENGINE ---
if run_analysis:
    active_jd = jd_input.strip() if jd_input else DEMO_JD
    
    # Resolve candidates: use uploaded files, or fallback to sample resumes if none uploaded
    candidates_to_process = []
    if uploaded_files:
        for f in uploaded_files:
            candidates_to_process.append({"name": f.name, "bytes": f.read()})
    else:
        st.info("ℹ️ No resumes uploaded: Running analysis with benchmark candidate profiles (Senior MLE, Data Scientist, Full Stack Dev).")
        for name, text in DEMO_RESUMES.items():
            candidates_to_process.append({"name": name, "raw_text": text})

    with st.spinner("Executing Transformer Semantic Cross-Encoder & Evaluating Qualifications..."):
            engine, extractor = get_models()
            jd_keywords = extractor.extract_keywords(active_jd, top_n=15)
            results = []

            for candidate in candidates_to_process:
                cand_name = candidate["name"]
                if "bytes" in candidate:
                    resume_text = extract_text_from_file(candidate["bytes"], cand_name)
                else:
                    resume_text = candidate.get("raw_text", "")
                
                resume_keywords = extractor.extract_keywords(resume_text, top_n=20)
                
                # Evaluate explicit qualifications (Experience, Companies, Degrees)
                qual_data = QualificationMatcher.evaluate_qualifications(
                    resume_text=resume_text,
                    min_experience_required=min_exp_input,
                    target_companies=target_companies_input,
                    required_degree=req_degree_input
                )
                
                eval_data = engine.evaluate_candidate(active_jd, resume_text, jd_keywords, resume_keywords, qual_data=qual_data)
                eval_data["Candidate"] = cand_name
                eval_data["resume_text"] = resume_text
                eval_data["qualifications"] = qual_data
                
                # Generate AI Advisor recommendations
                advice = RecruiterAdvisor.generate_advice(cand_name, eval_data, active_jd)
                eval_data["advice"] = advice
                results.append(eval_data)

            st.session_state["screening_results"] = results
            st.session_state["jd_keywords"] = sorted(list(jd_keywords))
            st.session_state["active_jd"] = active_jd

# --- RENDER RESULTS DASHBOARD ---
if "screening_results" in st.session_state and st.session_state["screening_results"]:
    results = st.session_state["screening_results"]
    df = pd.DataFrame(results).sort_values(by="score", ascending=False).reset_index(drop=True)
    jd_skills = st.session_state.get("jd_keywords", [])
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="hero-badge">📊 Comprehensive Talent Analytics & Visual Insights</div>', unsafe_allow_html=True)

    # --- 3 DISTINCT TABS FOR VISUALIZATION, LEADERBOARD, & ADVICE ---
    tab_viz, tab_rankings, tab_advisor = st.tabs([
        "📊 Intuitive Visual Analytics",
        "🏆 Candidate Leaderboard & Breakdown", 
        "💡 AI Recruiter Strategic Advisor & Interview Prep"
    ])

    # === TAB 1: INTUITIVE, EASY-TO-UNDERSTAND VISUAL ANALYTICS ===
    with tab_viz:
        # Chart 1: Simple & Direct Candidate Ranking Bar Chart
        st.markdown('<div class="floating-card">', unsafe_allow_html=True)
        st.markdown("### 1️⃣ Who is the Best Candidate? (Overall Match Ranking)")
        st.caption("Simple ranked comparison: Higher score means the candidate's skills and experience match the job better.")
        
        # Color coding: Green for strong, Amber for medium, Red for low
        colors = []
        labels = []
        for s in df["score"]:
            if s >= 75:
                colors.append("#10b981") # Green
                labels.append(f"{s:.1f}% — Strong Fit 🟢")
            elif s >= 50:
                colors.append("#f59e0b") # Amber
                labels.append(f"{s:.1f}% — Potential Fit 🟡")
            else:
                colors.append("#ef4444") # Red
                labels.append(f"{s:.1f}% — Low Fit 🔴")

        fig_rank = go.Figure()
        fig_rank.add_trace(go.Bar(
            x=df["score"][::-1],
            y=df["Candidate"][::-1],
            orientation="h",
            marker=dict(
                color=colors[::-1],
                line=dict(color="rgba(255, 255, 255, 0.2)", width=1)
            ),
            text=labels[::-1],
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="#ffffff", size=13, family="Plus Jakarta Sans", weight=700)
        ))

        fig_rank.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.4)",
            font=dict(color="#cbd5e1", family="Plus Jakarta Sans"),
            xaxis=dict(range=[0, 105], gridcolor="rgba(255,255,255,0.06)", title="Match Percentage (%)"),
            yaxis=dict(title="", tickfont=dict(size=13, color="#f8fafc", weight=600)),
            height=260,
            margin=dict(l=20, r=20, t=10, b=35)
        )
        st.plotly_chart(fig_rank, use_container_width=True, key="chart_simple_ranking")

        top_candidate_name = df.iloc[0]["Candidate"]
        top_candidate_score = df.iloc[0]["score"]
        st.markdown(f"""
        <div style="background: rgba(16, 185, 129, 0.1); border-left: 4px solid #10b981; padding: 10px 16px; border-radius: 0 10px 10px 0; margin-top: 8px;">
            <span style="font-weight: 700; color: #34d399;">💡 Key Takeaway:</span> 
            <span style="color: #f1f5f9;"><b>{top_candidate_name}</b> is your highest-scoring candidate at <b>{top_candidate_score:.1f}%</b> match.</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        col_v1, col_v2 = st.columns([1.2, 1], gap="medium")

        # Chart 2: Skills Matched vs Skills Missing (Easy Side-by-Side Comparison)
        with col_v1:
            st.markdown('<div class="floating-card">', unsafe_allow_html=True)
            st.markdown("### 2️⃣ Skills Found vs. Skills Missing")
            st.caption("Green shows skills the candidate has; Red shows skills they miss.")

            matched_counts = [len(r["matched_skills"]) for _, r in df.iterrows()]
            missing_counts = [len(r["missing_skills"]) for _, r in df.iterrows()]

            fig_skills_comp = go.Figure()
            fig_skills_comp.add_trace(go.Bar(
                name="✅ Skills Found in Resume",
                x=df["Candidate"],
                y=matched_counts,
                marker_color="#10b981",
                text=matched_counts,
                textposition="auto"
            ))
            fig_skills_comp.add_trace(go.Bar(
                name="❌ Skills Missing from Job",
                x=df["Candidate"],
                y=missing_counts,
                marker_color="#ef4444",
                text=missing_counts,
                textposition="auto"
            ))

            fig_skills_comp.update_layout(
                barmode="group",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(15, 23, 42, 0.4)",
                font=dict(color="#cbd5e1", family="Plus Jakarta Sans"),
                yaxis=dict(title="Number of Skills", gridcolor="rgba(255,255,255,0.06)", dtick=2),
                xaxis=dict(title=""),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                height=300,
                margin=dict(l=20, r=20, t=30, b=20)
            )
            st.plotly_chart(fig_skills_comp, use_container_width=True, key="chart_matched_vs_missing")
            st.markdown('</div>', unsafe_allow_html=True)

        # Chart 3: Talent Pool Fit Breakdown (Donut Chart)
        with col_v2:
            st.markdown('<div class="floating-card">', unsafe_allow_html=True)
            st.markdown("### 3️⃣ Hiring Recommendation Split")
            st.caption("How your talent pool breaks down into hiring tiers.")

            strong_fits = len(df[df["score"] >= 65])
            moderate_fits = len(df[(df["score"] >= 50) & (df["score"] < 65)])
            low_fits = len(df[df["score"] < 50])

            labels_donut = []
            values_donut = []
            colors_donut = []

            if strong_fits > 0:
                labels_donut.append("🟢 Ready to Interview (≥65%)")
                values_donut.append(strong_fits)
                colors_donut.append("#10b981")
            if moderate_fits > 0:
                labels_donut.append("🟡 Borderline / Review (50-64%)")
                values_donut.append(moderate_fits)
                colors_donut.append("#f59e0b")
            if low_fits > 0:
                labels_donut.append("🔴 Low Match (<50%)")
                values_donut.append(low_fits)
                colors_donut.append("#ef4444")

            fig_donut = go.Figure(data=[go.Pie(
                labels=labels_donut,
                values=values_donut,
                hole=0.6,
                marker=dict(colors=colors_donut),
                textinfo="value+percent",
                hoverinfo="label+value"
            )])

            fig_donut.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#cbd5e1", family="Plus Jakarta Sans"),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
                height=300,
                margin=dict(l=20, r=20, t=10, b=40),
                annotations=[dict(text=f"<b>{len(df)}</b><br>Total", x=0.5, y=0.5, font_size=18, font_color="#ffffff", showarrow=False)]
            )
            st.plotly_chart(fig_donut, use_container_width=True, key="chart_pool_donut")
            st.markdown('</div>', unsafe_allow_html=True)

        # Chart 4: Simple Visual Summary Checklist
        st.markdown('<div class="floating-card">', unsafe_allow_html=True)
        st.markdown("### 4️⃣ Quick Candidate Comparison Summary")
        st.caption("At-a-glance overview of candidate scores and quick recommendation.")

        summary_rows = []
        for idx, r in df.iterrows():
            medal = "🥇 #1" if idx == 0 else ("🥈 #2" if idx == 1 else ("🥉 #3" if idx == 2 else f"#{idx+1}"))
            matched_preview = ", ".join(r["matched_skills"][:5]) if r["matched_skills"] else "None"
            missing_preview = ", ".join(r["missing_skills"][:4]) if r["missing_skills"] else "None"
            qual = r.get("qualifications", {})
            exp_str = f"{qual.get('detected_experience', 0):.1f} yrs" + (" ✅" if qual.get("meets_experience") else " ⚠️")
            co_str = ", ".join(qual.get("matched_companies", [])) if qual.get("matched_companies") else "None"
            
            summary_rows.append({
                "Rank": medal,
                "Candidate": r["Candidate"],
                "Overall Score": f"{r['score']}%",
                "Experience": exp_str,
                "Target Companies": co_str,
                "Verified Skills Found": matched_preview,
                "Key Missing Skills": missing_preview,
                "Recommendation": r["advice"]["verdict"]
            })
        
        st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # === TAB 2: CANDIDATE LEADERBOARD & DEEP DIVE ===
    with tab_rankings:
        for idx, row in df.iterrows():
            medal = "🥇" if idx == 0 else ("🥈" if idx == 1 else ("🥉" if idx == 2 else f"#{idx+1}"))
            score_color = "#10b981" if row['score'] >= 75 else ("#6366f1" if row['score'] >= 60 else "#f59e0b")
            qual = row.get("qualifications", {})
            
            with st.expander(f"{medal} **{row['Candidate']}** — Overall Match: {row['score']}% | Exp: {qual.get('detected_experience', 0):.1f} yrs | Semantic: {row['semantic_score']}% | Keywords: {row['skill_match_ratio']}%", expanded=(idx==0)):
                
                col_chart, col_skills = st.columns([1, 1.2], gap="medium")
                
                with col_chart:
                    # Clean Modern Gauge Chart
                    fig_gauge = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=row['score'],
                        number={'suffix': "%", 'font': {'color': '#f8fafc', 'family': 'Outfit', 'size': 32}},
                        gauge={
                            'axis': {'range': [0, 100], 'tickcolor': "#475569"},
                            'bar': {'color': score_color, 'thickness': 0.28},
                            'bgcolor': "rgba(15, 23, 42, 0.6)",
                            'borderwidth': 0,
                            'steps': [
                                {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.15)'},
                                {'range': [50, 70], 'color': 'rgba(245, 158, 11, 0.15)'},
                                {'range': [70, 100], 'color': 'rgba(16, 185, 129, 0.15)'}
                            ]
                        }
                    ))
                    fig_gauge.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        margin=dict(l=20, r=20, t=25, b=10),
                        height=200
                    )
                    st.plotly_chart(fig_gauge, use_container_width=True, key=f"gauge_{row['Candidate']}_{idx}")

                with col_skills:
                    st.markdown("#### Competency & Qualification Breakdown")
                    st.markdown(f"**Action Verdict:** <span class='{row['advice']['verdict_badge']}'>{row['advice']['verdict']}</span>", unsafe_allow_html=True)
                    st.write("")
                    
                    # Qualifications bar
                    st.markdown(f"""
                    <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 10px 14px; margin-bottom: 12px; font-size: 13px;">
                        <div>💼 <b>Experience:</b> {qual.get('exp_status', 'N/A')}</div>
                        <div style="margin-top: 4px;">🏢 <b>Target Companies:</b> <span style="color: #60a5fa;">{', '.join(qual.get('matched_companies', [])) or 'No specific target company matched'}</span></div>
                        <div style="margin-top: 4px;">🎓 <b>Education:</b> {qual.get('detected_education', 'Not Specified')}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("**✅ Verified Matched Skills:**")
                    if row["matched_skills"]:
                        pills = "".join([f"<span class='badge-pill badge-matched'>✓ {s}</span>" for s in row["matched_skills"]])
                        st.markdown(pills, unsafe_allow_html=True)
                    else:
                        st.caption("No direct keyword overlap found.")
                    
                    st.markdown("<br>**❌ Missing Job Competencies:**", unsafe_allow_html=True)
                    if row["missing_skills"]:
                        missing_pills = "".join([f"<span class='badge-pill badge-missing'>✕ {s}</span>" for s in row["missing_skills"][:12]])
                        st.markdown(missing_pills, unsafe_allow_html=True)
                    else:
                        st.caption("All job description keywords matched!")

    # === TAB 3: AI RECRUITER STRATEGIC ADVISOR ===
    with tab_advisor:
        st.markdown("""
        <div class="advice-container">
            <div class="advice-title">
                <span>💡</span> AI Talent Advisor & Strategic Interview Blueprint
            </div>
            <p style="color: #94a3b8; font-size: 14px; margin: 0 0 16px 0;">
                Comprehensive hiring advice, candidate risk assessments, and targeted interview probes generated from model evaluation.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        selected_candidate = st.selectbox(
            "Select Candidate to Review Advice & Interview Strategy:", 
            options=[row["Candidate"] for _, row in df.iterrows()]
        )
        
        cand_data = df[df["Candidate"] == selected_candidate].iloc[0]
        advice_info = cand_data["advice"]
        
        col_adv1, col_adv2 = st.columns([1, 1], gap="large")
        
        with col_adv1:
            st.markdown('<div class="floating-card">', unsafe_allow_html=True)
            st.markdown(f"### 📋 Strategic Verdict: <span class='{advice_info['verdict_badge']}'>{advice_info['verdict']}</span>", unsafe_allow_html=True)
            st.info(f"**Recommended Action Plan:** {advice_info['action_plan']}")
            
            st.markdown("#### 🌟 Candidate Strengths")
            for s in advice_info["strengths"]:
                st.markdown(f"- {s}")
                
            st.markdown("#### ⚠️ Competency Risks & Red Flags")
            for r in advice_info["risks"]:
                st.markdown(f"- {r}")
                
            st.markdown('</div>', unsafe_allow_html=True)

        with col_adv2:
            st.markdown('<div class="floating-card">', unsafe_allow_html=True)
            st.markdown("### 🎯 Tailored Interview Questions")
            st.caption("Targeted probes generated dynamically to test depth on matches and investigate identified skill gaps:")
            
            for i, q in enumerate(advice_info["questions"], 1):
                st.markdown(f"""
                <div style="background: rgba(15, 23, 42, 0.6); border-left: 3px solid #6366f1; padding: 12px 16px; border-radius: 0 10px 10px 0; margin-bottom: 12px;">
                    <div style="font-size: 13px; color: #a5b4fc; font-weight: 700; margin-bottom: 4px;">Question {i}</div>
                    <div style="font-size: 14px; color: #f1f5f9; line-height: 1.5;">{q}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("#### 📝 Executive Hiring Manager Note")
            st.code(advice_info["summary"], language="markdown")
            st.markdown('</div>', unsafe_allow_html=True)
