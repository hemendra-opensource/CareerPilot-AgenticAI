import os
import streamlit as st
from datetime import datetime
from config.config import Config
from utils.role_database import ROLE_DATABASE
from utils.report_generator import build_pdf_report

st.set_page_config(
    page_title="CareerPilot AI - Download Reports",
    page_icon="📥",
    layout="wide"
)

# ──────────────────────────────────────────────
# Custom Styling
# ──────────────────────────────────────────────
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .page-title {
            background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.6rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }

        .page-subtitle {
            font-size: 1.1rem;
            color: #6C757D;
            margin-bottom: 2rem;
        }

        .section-header {
            font-size: 1.4rem;
            font-weight: 600;
            color: #2D3748;
            margin-top: 2rem;
            margin-bottom: 1rem;
            border-left: 5px solid #FF416C;
            padding-left: 0.6rem;
        }

        .meta-card {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        }

        .meta-item {
            display: flex;
            justify-content: space-between;
            padding: 0.6rem 0;
            border-bottom: 1px solid #F7FAFC;
            font-size: 0.95rem;
        }
        .meta-item:last-child {
            border-bottom: none;
        }

        .meta-label {
            font-weight: 600;
            color: #4A5568;
        }

        .meta-value {
            color: #2D3748;
            font-family: monospace;
        }
    </style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────
st.markdown('<h1 class="page-title">📥 Career Reports</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="page-subtitle">Consolidate your career diagnostics, resume audits, skills roadmap, and mock interviews into a publication-ready PDF.</p>',
    unsafe_allow_html=True
)

# ──────────────────────────────────────────────
# Data Aggregation
# ──────────────────────────────────────────────
def collect_report_data() -> dict:
    """Aggregates all active agent outputs from st.session_state."""
    data = {
        "username": "Professional Candidate",
        "target_role": "Data Scientist",
        "ats_score": 70.0,
        "resume_strengths": [],
        "resume_weaknesses": [],
        "ats_feedback": "Resume analysis not completed.",
        "gap_score": 50.0,
        "matched_skills": [],
        "missing_skills": [],
        "timeline_months": "6 Months",
        "roadmap_stages": {},
        "monthly_plan": {},
        "priority_matrix": {},
        "interview_readiness": 50.0,
        "interview_risk_questions": [],
        "projects": [],
        "health_score": 50.0,
        "health_label": "Average",
        "readiness_score": 50.0,
        "readiness_label": "Needs Preparation",
        "advisor_summary": "Perform career assessment calculations first.",
        "hiring_outlook": "Highly competitive track.",
        "action_plan": {}
    }

    # 1. Target Role Track
    if "gap_results" in st.session_state and st.session_state["gap_results"]:
        data["target_role"] = st.session_state["gap_results"].get("target_role", "Data Scientist")
        data["gap_score"] = float(st.session_state["gap_results"].get("gap_score", 50.0))
        data["missing_skills"] = st.session_state["gap_results"].get("missing_skills", [])
        data["matched_skills"] = st.session_state["gap_results"].get("matched_skills", [])

    # 2. Resume Details
    if "analysis_results" in st.session_state and st.session_state["analysis_results"]:
        ar = st.session_state["analysis_results"]
        data["username"] = ar.get("personal_details", {}).get("name", "Professional Candidate")
        data["ats_score"] = float(ar.get("completeness_score", 70.0))
        data["resume_strengths"] = ar.get("strengths", [])
        data["resume_weaknesses"] = ar.get("weaknesses", [])
        
        # Format ATS audit items into string block
        audit_bullets = ar.get("ats_feedback", {}).get("missing_keywords", [])
        if audit_bullets:
            data["ats_feedback"] = f"Missing core keywords detected: {', '.join(audit_bullets)}. Focus on adding these items to improve scan alignment."
        else:
            data["ats_feedback"] = "Formatting blocks and scan metadata aligned with standards."

    # 3. Roadmap Details
    if "roadmap_results" in st.session_state and st.session_state["roadmap_results"]:
        rr = st.session_state["roadmap_results"]
        t_months = rr.get("timeline_months", 6)
        data["timeline_months"] = f"{t_months} Months"
        data["roadmap_stages"] = rr.get("stages", {})
        data["monthly_plan"] = rr.get("monthly_plan", {})
        data["priority_matrix"] = rr.get("priority_matrix", {})

    # 4. Interview Details
    if "interview_results" in st.session_state and st.session_state["interview_results"]:
        ir = st.session_state["interview_results"]
        data["interview_readiness"] = float(ir.get("readiness", {}).get("score", 50.0))
        data["interview_risk_questions"] = ir.get("weak_areas", {}).get("interview_risk_areas", [])

    # 5. Project Details
    if "project_results" in st.session_state and st.session_state["project_results"]:
        pr = st.session_state["project_results"]
        data["projects"] = (
            pr.get("beginner", []) +
            pr.get("intermediate", []) +
            pr.get("advanced", [])
        )

    # 6. Master Agent Details
    if "master_results" in st.session_state and st.session_state["master_results"]:
        mr = st.session_state["master_results"]
        data["health_score"] = float(mr.get("health_score", {}).get("score", 50.0))
        data["health_label"] = mr.get("health_score", {}).get("label", "Average")
        data["readiness_score"] = float(mr.get("readiness_score", {}).get("score", 50.0))
        data["readiness_label"] = mr.get("readiness_score", {}).get("label", "Needs Preparation")
        data["advisor_summary"] = mr.get("assessment", {}).get("career_summary", "")
        data["hiring_outlook"] = mr.get("assessment", {}).get("hiring_outlook", "")
        data["action_plan"] = mr.get("action_plan", {})

    return data

data = collect_report_data()

# ──────────────────────────────────────────────
# 1. UI Elements & Metadata Card
# ──────────────────────────────────────────────
st.markdown('<div class="section-header">1. Report Parameters Overview</div>', unsafe_allow_html=True)
col_meta, col_actions = st.columns([3, 2])

with col_meta:
    st.markdown('<div class="meta-card">', unsafe_allow_html=True)
    st.markdown("#### Diagnostic Values Summary")
    
    items = [
        ("Candidate Name", data["username"]),
        ("Target Career Track", data["target_role"]),
        ("Career Health Score", f"{data['health_score']}/100 ({data['health_label']})"),
        ("Hiring Readiness Score", f"{data['readiness_score']}/100 ({data['readiness_label']})"),
        ("Resume ATS Scan Score", f"{data['ats_score']}/100"),
        ("Core Skill Gap Score", f"{data['gap_score']}%"),
        ("Interview Readiness Score", f"{data['interview_readiness']}%"),
        ("Recommended Projects Count", str(len(data["projects"])))
    ]
    
    for label, val in items:
        st.markdown(
            f'<div class="meta-item">'
            f'<span class="meta-label">{label}</span>'
            f'<span class="meta-value">{val}</span>'
            f'</div>',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────
# 2. PDF Report Generator Actions
# ──────────────────────────────────────────────
# Ensure reports directory exists
reports_dir = os.path.join(os.getcwd(), "reports")
os.makedirs(reports_dir, exist_ok=True)
target_pdf_path = os.path.join(reports_dir, "career_assessment_report.pdf")

with col_actions:
    st.markdown('<div class="section-header" style="margin-top:0;">2. Generate Assessment</div>', unsafe_allow_html=True)
    
    if st.button("🛠️ Generate PDF Report", type="primary", use_container_width=True):
        with st.spinner("Compiling ReportLab flowables, building document structure, and writing report file..."):
            try:
                path = build_pdf_report(data, target_pdf_path)
                st.session_state["generated_pdf_path"] = path
                st.success("✅ Career Assessment Report built successfully!")
            except Exception as e:
                st.error(f"Error compiling PDF: {str(e)}")
                st.session_state["generated_pdf_path"] = None

    # Render download button if path exists in state
    saved_path = st.session_state.get("generated_pdf_path")
    if saved_path and os.path.exists(saved_path):
        st.markdown("<br>", unsafe_allow_html=True)
        try:
            with open(saved_path, "rb") as f:
                pdf_bytes = f.read()
                
            st.download_button(
                label="📥 Download Career Assessment Report (PDF)",
                data=pdf_bytes,
                file_name=f"CareerPilot_Report_{data['target_role'].replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error preparing file for download: {str(e)}")
    else:
        st.info("💡 Click **Generate PDF Report** above to compile your file.")

st.markdown("---")

# ──────────────────────────────────────────────
# 3. Report Outline Preview
# ──────────────────────────────────────────────
st.markdown('<div class="section-header">3. Report Outline Preview</div>', unsafe_allow_html=True)
with st.expander("🔍 View structured segments included in final PDF report", expanded=True):
    preview_data = [
        "**Cover Page:** Clean, recruiter-friendly layout drawing Candidate Name, Target Track, Date, and Branding.",
        "**Executive Summary:** Score cards presenting Health, Readiness, ATS Scan, and Skill Gaps.",
        "**Resume Analysis Summary:** Strengths, weaknesses, and ATS formatting keyword suggestions.",
        "**Skill Gaps Mapping:** Table detailing possessed capabilities alongside required technical gap targets.",
        "**Roadmap Timeline:** Month-by-month stages (Beginner, Intermediate, Advanced) based on core gaps.",
        "**Interview Readiness Dashboard:** Top risk questions and focus zones.",
        "**Recommended Projects:** Portfolio value, resume impact, duration, and development phases.",
        "**AI Career Advisor Narrative:** Summary context, risk indicators, market hiring outlook, and final recommendations."
    ]
    for bullet in preview_data:
        st.markdown(f"- {bullet}")
