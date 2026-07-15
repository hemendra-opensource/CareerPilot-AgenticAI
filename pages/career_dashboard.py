import streamlit as st
from config.config import Config
from utils.role_database import ROLE_DATABASE
from agents.master_agent import MasterAgent

st.set_page_config(
    page_title="CareerPilot AI - Master Career Dashboard",
    page_icon="👑",
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
            background: linear-gradient(135deg, #1F1C2C 0%, #928DAB 100%);
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
            border-left: 5px solid #1F1C2C;
            padding-left: 0.6rem;
        }

        .score-box-health {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            padding: 2rem; border-radius: 12px; text-align: center;
            color: white; box-shadow: 0 4px 15px rgba(17,153,142,0.25);
        }
        
        .score-box-readiness {
            background: linear-gradient(135deg, #3a7bd5 0%, #3a6073 100%);
            padding: 2rem; border-radius: 12px; text-align: center;
            color: white; box-shadow: 0 4px 15px rgba(58,123,213,0.25);
        }

        .score-title {
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            opacity: 0.9;
        }

        .score-value {
            font-size: 3.8rem;
            font-weight: 700;
            margin-top: 0.5rem;
            margin-bottom: 0.2rem;
        }

        .score-label {
            font-size: 1.1rem;
            font-weight: 600;
        }

        .sub-card {
            background-color: #FFFFFF;
            color: black;
            border: 1px solid #E9ECEF;
            border-radius: 10px;
            padding: 1.2rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 5px rgba(0,0,0
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 1.2rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 5px rgba(0,0,0,0.02);
        }

        .sub-card-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: #2D3748;
            margin-bottom: 0.8rem;
            display: flex;
            justify-content: space-between;
        }

        .action-bullet-immediate {
            padding: 0.6rem 0.8rem;
            background-color: #FFF5F5;
            border-left: 4px solid #FC8181;
            margin-bottom: 0.5rem;
            border-radius: 0 6px 6px 0;
            color: #742A2A;
            font-size: 0.9rem;
        }

        .action-bullet-short {
            padding: 0.6rem 0.8rem;
            background-color: #FFFAF0;
            border-left: 4px solid #ED8936;
            margin-bottom: 0.5rem;
            border-radius: 0 6px 6px 0;
            color: #7B341E;
            font-size: 0.9rem;
        }

        .action-bullet-medium {
            padding: 0.6rem 0.8rem;
            background-color: #EBF8FF;
            border-left: 4px solid #4299E1;
            margin-bottom: 0.5rem;
            border-radius: 0 6px 6px 0;
            color: #2B6CB0;
            font-size: 0.9rem;
        }

        .action-bullet-long {
            padding: 0.6rem 0.8rem;
            background-color: #F0FFF4;
            border-left: 4px solid #48BB78;
            margin-bottom: 0.5rem;
            border-radius: 0 6px 6px 0;
            color: #22543D;
            font-size: 0.9rem;
        }

        .advisor-card {
            background-color: #F7FAFC;
            border: 1px dashed #CBD5E0;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }

        .advisor-bullet {
            padding: 0.5rem 0.7rem;
            background-color: #EDF2F7;
            colo
            border-left: 3px solid #4A5568;
            margin-bottom: 0.4rem;
            border-radius: 0 4px 4px 0;
            font-size: 0.9rem;
        }
    </style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────
st.markdown('<h1 class="page-title">👑 Master Career Agent</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="page-subtitle">Unified career evaluator, planner, and advisor consolidating your resume, gaps, roadmaps, and interview analytics.</p>',
    unsafe_allow_html=True
)

is_config_valid, config_msg = Config.validate()
if not is_config_valid:
    st.error(f"⚠️ Configuration Warning: {config_msg}")
    st.info("Please set your `GROQ_API_KEY` in the `.env` file.")
    st.stop()

# ──────────────────────────────────────────────
# Session State Aggregation
# ──────────────────────────────────────────────
ats_score = 70.0
gap_score = 50.0
interview_readiness = 50.0
roadmap_current = 50.0
missing_skills = []
matched_skills = []
recommended_projects = []
has_full_profile = False
default_role = "Data Scientist"

# Phase 2: Resume
if "analysis_results" in st.session_state and st.session_state["analysis_results"]:
    ats_score = float(st.session_state["analysis_results"].get("completeness_score", 70.0))

# Phase 3: Skill Gap
if "gap_results" in st.session_state and st.session_state["gap_results"]:
    gap_data = st.session_state["gap_results"]
    gap_score = float(gap_data.get("gap_score", 50.0))
    missing_skills = gap_data.get("missing_skills", [])
    matched_skills = gap_data.get("matched_skills", [])
    default_role = gap_data.get("target_role", "Data Scientist")
    has_full_profile = True

# Phase 4: Roadmap
if "roadmap_results" in st.session_state and st.session_state["roadmap_results"]:
    roadmap_current = float(
        st.session_state["roadmap_results"].get("forecast", {}).get("current", 50.0)
    )

# Phase 5: Interview
if "interview_results" in st.session_state and st.session_state["interview_results"]:
    interview_readiness = float(
        st.session_state["interview_results"].get("readiness", {}).get("score", 50.0)
    )
elif has_full_profile:
    interview_readiness = max(0.0, round(100.0 - gap_score, 1))

# Phase 6: Projects
if "project_results" in st.session_state and st.session_state["project_results"]:
    proj_results = st.session_state["project_results"]
    recommended_projects = (
        proj_results.get("beginner", []) +
        proj_results.get("intermediate", []) +
        proj_results.get("advanced", [])
    )

# Profile Display Status
if has_full_profile:
    st.success(
        f"📂 Executive profile active — Role: **{default_role}** | "
        f"Parsed Resume ATS: **{ats_score}%** | Skill Gap: **{gap_score}%**"
    )
else:
    st.warning("⚠️ No active career profile found. Navigate through previous agent tabs (Resume, Skill Gap, Roadmap, Interview, Projects) to establish target role metadata.")

# Target Role Selector
st.markdown('<div class="section-header">1. Assessment Configuration</div>', unsafe_allow_html=True)
col_role, col_spacer = st.columns([1, 1])
with col_role:
    target_role = st.selectbox(
        "Select Target Career Track:",
        options=list(ROLE_DATABASE.keys()),
        index=list(ROLE_DATABASE.keys()).index(default_role) if default_role in ROLE_DATABASE else 0
    )

st.markdown("---")

# ──────────────────────────────────────────────
# 2. Execution Trigger
# ──────────────────────────────────────────────
if st.button("🚀 Execute Master Career Assessment", type="primary"):
    with st.spinner("Aggregating multi-agent outputs, computing health metrics, and drafting AI advisory assessment..."):
        try:
            master = MasterAgent()
            results = master.run_full_orchestration(
                role=target_role,
                ats_score=ats_score,
                gap_score=gap_score,
                missing_skills=missing_skills,
                matched_skills=matched_skills,
                interview_readiness=interview_readiness,
                projects=recommended_projects
            )
            st.session_state["master_results"] = results
            st.session_state["master_role"] = target_role
            st.success("✅ Master Career assessment finalized successfully!")
        except Exception as e:
            st.error(f"Error executing master coordinator: {str(e)}")
            st.session_state["master_results"] = None

# ──────────────────────────────────────────────
# 3. Main Dashboard Rendering
# ──────────────────────────────────────────────
results = st.session_state.get("master_results")

if results and results.get("target_role") == target_role:
    health = results["health_score"]
    readiness = results["readiness_score"]
    action_plan = results["action_plan"]
    assessment = results["assessment"]
    stats = results["subsystem_stats"]

    # ── Executive KPI Cards ───────────────────
    st.markdown('<div class="section-header">2. Executive Career Status</div>', unsafe_allow_html=True)
    col_h, col_r = st.columns(2)
    
    with col_h:
        st.markdown(f"""
            <div class="score-box-health">
                <div class="score-title">Career Health Score</div>
                <div class="score-value">{health['score']}</div>
                <div class="score-label">{health['label']}</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.progress(health["score"] / 100.0)

    with col_r:
        st.markdown(f"""
            <div class="score-box-readiness">
                <div class="score-title">Hiring Readiness Score</div>
                <div class="score-value">{readiness['score']}</div>
                <div class="score-label">{readiness['label']}</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.progress(readiness["score"] / 100.0)

    st.markdown("---")

    # ── Subsystems Overview Tab Layout ────────
    st.markdown('<div class="section-header">3. Subsystem Summaries</div>', unsafe_allow_html=True)
    t_res, t_gap, t_road, t_int, t_proj = st.tabs([
        "📄 Resume", "🔍 Skill Gap", "🗺️ Roadmap", "🎙️ Interview Prep", "🛠️ Portfolio Projects"
    ])

    with t_res:
        st.markdown('<div class="sub-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="sub-card-title">Resume completeness <span>{stats["ats_score"]}%</span></div>', unsafe_allow_html=True)
        st.progress(stats["ats_score"] / 100.0)
        st.markdown("""
            **Focus Areas:**
            - Optimize formatting blocks (Contact, Experience, Skills, Education).
            - Add quantifiable metrics to experience bullet points.
            - Ensure ATS keywords align with the target tracks.
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    with t_gap:
        st.markdown('<div class="sub-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="sub-card-title">Skill Gap Analysis <span>{stats["gap_score"]}% Gap</span></div>', unsafe_allow_html=True)
        st.progress(max(0.0, 100.0 - stats["gap_score"]) / 100.0)
        st.markdown(f"**Matched Competencies:** {', '.join(matched_skills) if matched_skills else 'None detected'}")
        st.markdown(f"**Missing Competencies:** {', '.join(missing_skills) if missing_skills else 'None detected'}")
        st.markdown('</div>', unsafe_allow_html=True)

    with t_road:
        st.markdown('<div class="sub-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="sub-card-title">Roadmap coverage <span>{roadmap_current}%</span></div>', unsafe_allow_html=True)
        st.progress(roadmap_current / 100.0)
        st.markdown(f"""
            **Roadmap Progression Track:**
            - **Current Status:** Phase 4 Scheduled Milestone
            - **Estimated Preparation Timeframe:** {("3 Months" if gap_score < 25 else "6 Months" if gap_score < 60 else "12 Months")}
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    with t_int:
        st.markdown('<div class="sub-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="sub-card-title">Interview preparation <span>{stats["interview_readiness"]}% Readiness</span></div>', unsafe_allow_html=True)
        st.progress(stats["interview_readiness"] / 100.0)
        st.markdown(f"**Critical risk questions to practice:** {stats['missing_skills_count']} missing skill zones mapped to the templates.")
        st.markdown('</div>', unsafe_allow_html=True)

    with t_proj:
        st.markdown('<div class="sub-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="sub-card-title">Portfolio strength <span>{stats["avg_portfolio_impact"]}% Avg Impact</span></div>', unsafe_allow_html=True)
        st.progress(stats["avg_portfolio_impact"] / 100.0)
        st.markdown(f"**Total recommended projects:** {stats['recommended_projects_count']} projects configured to close skill gaps.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Unified Action Plan ───────────────────
    st.markdown('<div class="section-header">4. Unified Career Action Plan</div>', unsafe_allow_html=True)
    col_7, col_30 = st.columns(2)
    with col_7:
        st.markdown("#### 📅 Immediate Actions (Next 7 Days)")
        for item in action_plan["immediate_7_days"]:
            st.markdown(f'<div class="action-bullet-immediate">⚡ {item}</div>', unsafe_allow_html=True)
            
    with col_30:
        st.markdown("#### 📆 Short-Term Goals (30 Days)")
        for item in action_plan["short_term_30_days"]:
            st.markdown(f'<div class="action-bullet-short">🏃 {item}</div>', unsafe_allow_html=True)

    col_90, col_365 = st.columns(2)
    with col_90:
        st.markdown("#### 📅 Medium-Term Goals (90 Days)")
        for item in action_plan["medium_term_90_days"]:
            st.markdown(f'<div class="action-bullet-medium">🎯 {item}</div>', unsafe_allow_html=True)
            
    with col_365:
        st.markdown("#### 📆 Long-Term Goals (6–12 Months)")
        for item in action_plan["long_term_goals"]:
            st.markdown(f'<div class="action-bullet-long">🏆 {item}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── AI Career Advisor Summary ─────────────
    st.markdown('<div class="section-header">5. AI Career Advisor Feedback</div>', unsafe_allow_html=True)
    st.markdown('<div class="advisor-card">', unsafe_allow_html=True)
    st.markdown(f"#### 📖 Career Summary")
    st.write(assessment.get("career_summary", ""))
    
    col_str, col_risk = st.columns(2)
    with col_str:
        st.markdown("#### 💪 Key Strengths")
        for strength in assessment.get("strengths_assessment", []):
            st.markdown(f'<div class="advisor-bullet">⭐ {strength}</div>', unsafe_allow_html=True)
            
    with col_risk:
        st.markdown("#### ⚠️ Key Risks & Weaknesses")
        for risk in assessment.get("risks_assessment", []):
            st.markdown(f'<div class="action-bullet-immediate" style="margin-left:0;border-left-width:3px;">🚨 {risk}</div>', unsafe_allow_html=True)

    st.markdown("#### 📈 Hiring Outlook")
    st.write(assessment.get("hiring_outlook", ""))

    st.markdown("#### 🚀 Strategic Recommended Next Steps")
    for step in assessment.get("recommended_next_steps", []):
        st.markdown(f'<div class="advisor-bullet">✔ {step}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
