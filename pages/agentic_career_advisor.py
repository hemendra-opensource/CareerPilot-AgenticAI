import streamlit as st
from config.config import Config
from utils.role_database import ROLE_DATABASE

st.set_page_config(
    page_title="CareerPilot AI - Agentic Career Advisor",
    page_icon="🕵🏻",
    layout="wide"
)

# ──────────────────────────────────────────────
# Custom Styling
# ──────────────────────────────────────────────
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

        .page-title {
            background: linear-gradient(135deg, #1e4c5e 0%, #203A43 50%, #2C5364 100%);
            color: transparent;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.6rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        .page-subtitle { font-size: 1.1rem; color: #6C757D; margin-bottom: 2rem; }

        .section-header {
            font-size: 1.4rem;
            font-weight: 600;
            color: #2D3748;
            margin-top: 2rem;
            margin-bottom: 1rem;
            border-left: 5px solid #2C5364;
            padding-left: 0.6rem;
            color: #2C5364;
        }

        .agent-step {
            display: flex;
            align-items: center;
            padding: 0.9rem 1.2rem;
            border-radius: 10px;
            margin-bottom: 0.7rem;
            border: 1px solid #E2E8F0;
            background-color: #FFFFFF;
        }
        .agent-step-idle   { border-left: 5px solid #CBD5E0; }
        .agent-step-run    { border-left: 5px solid #F6AD55; background-color: #FFFAF0; }
        .agent-step-done   { border-left: 5px solid #68D391; background-color: #F0FFF4; }
        .agent-step-failed { border-left: 5px solid #FC8181; background-color: #FFF5F5; }

        .step-icon  { font-size: 1.5rem; margin-right: 0.8rem; }
        .step-role  { font-weight: 600; color: #2D3748; font-size: 0.95rem; }
        .step-track { font-size: 0.82rem; color: #718096; }
        .step-badge {
            margin-left: auto;
            font-size: 0.78rem;
            font-weight: 600;
            padding: 0.2rem 0.6rem;
            border-radius: 20px;
        }
        .badge-idle   { background:#EDF2F7; color:#4A5568; }
        .badge-run    { background:#FEFCBF; color:#744210; }
        .badge-done   { background:#C6F6D5; color:#22543D; }
        .badge-failed { background:#FED7D7; color:#742A2A; }

        .result-card {
            background-color: #F7FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        }
        .result-kpi {
            font-size: 2.8rem;
            font-weight: 700;
            color: #2C5364;
        }
        .result-label { font-size: 0.9rem; font-weight: 600; color: #718096; text-transform: uppercase; }
    </style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────
st.markdown('<h1 class="page-title">🕵🏻 Agentic Career Advisor</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="page-subtitle">Run a fully autonomous multi-agent career pipeline — from resume parsing to final career strategy.</p>',
    unsafe_allow_html=True
)

is_config_valid, config_msg = Config.validate()
if not is_config_valid:
    st.error(f"⚠️ Configuration Warning: {config_msg}")
    st.info("Please set your `GROQ_API_KEY` in the `.env` file.")
    st.stop()

# ──────────────────────────────────────────────
# Agent step labels (no imports from crew yet)
# ──────────────────────────────────────────────
AGENT_STEPS = [
    {"step": 1, "icon": "📄", "label": "Resume Specialist",  "role": "Resume Evaluation Expert"},
    {"step": 2, "icon": "🔍", "label": "Skill Gap Analyst",  "role": "Career Skills Analyst"},
    {"step": 3, "icon": "🗺️", "label": "Roadmap Strategist", "role": "Learning Path Planner"},
    {"step": 4, "icon": "🎙️", "label": "Interview Coach",    "role": "Technical Interview Mentor"},
    {"step": 5, "icon": "🛠️", "label": "Project Mentor",     "role": "Portfolio Builder"},
    {"step": 6, "icon": "👑", "label": "Career Advisor",     "role": "Senior Career Consultant"},
]

# ──────────────────────────────────────────────
# Input Configuration
# ──────────────────────────────────────────────
st.markdown('<div class="section-header">1. Crew Configuration</div>', unsafe_allow_html=True)

col_role, col_spacer = st.columns([1, 1])
with col_role:
    target_role = st.selectbox(
        "Target Career Track:",
        options=list(ROLE_DATABASE.keys()),
        index=0,
        key="crew_target_role"
    )

st.markdown("**Paste Resume Text for Agentic Analysis:**")
resume_text = st.text_area(
    label="Resume Text",
    placeholder="Paste your complete resume text here for the multi-agent pipeline to analyze...",
    height=180,
    key="crew_resume_text",
    label_visibility="collapsed"
)

# Optionally pre-fill from prior session state if available
if not resume_text and "analysis_results" in st.session_state:
    extracted = st.session_state["analysis_results"].get("extracted_text", "")
    if extracted:
        resume_text = extracted
        st.info("💡 Auto-loaded resume text from Resume Analyzer session.")

st.markdown("---")

# ──────────────────────────────────────────────
# 2. Agent Execution Panel
# ──────────────────────────────────────────────
st.markdown('<div class="section-header">2. Multi-Agent Execution</div>', unsafe_allow_html=True)

def render_steps(statuses: dict[int, str]):
    """Renders the live agent step panel."""
    for s in AGENT_STEPS:
        st_key = statuses.get(s["step"], "idle")
        css_cls = {
            "idle": "agent-step-idle",
            "running": "agent-step-run",
            "success": "agent-step-done",
            "failed": "agent-step-failed"
        }.get(st_key, "agent-step-idle")
        badge_cls = {
            "idle": "badge-idle",
            "running": "badge-run",
            "success": "badge-done",
            "failed": "badge-failed"
        }.get(st_key, "badge-idle")
        badge_txt = {
            "idle": "Waiting",
            "running": "Running...",
            "success": "Completed",
            "failed": "Failed"
        }.get(st_key, "Waiting")

        st.markdown(f"""
            <div class="agent-step {css_cls}">
                <span class="step-icon">{s['icon']}</span>
                <div>
                    <div class="step-role">{s['label']}</div>
                    <div class="step-track">{s['role']}</div>
                </div>
                <span class="step-badge {badge_cls}">{badge_txt}</span>
            </div>
        """, unsafe_allow_html=True)

# Initialize step statuses
if "crew_step_statuses" not in st.session_state:
    st.session_state["crew_step_statuses"] = {s["step"]: "idle" for s in AGENT_STEPS}

# Step panel placeholder
step_panel = st.empty()
with step_panel.container():
    render_steps(st.session_state["crew_step_statuses"])

st.markdown("---")

# ──────────────────────────────────────────────
# 3. Run Crew Button
# ──────────────────────────────────────────────
run_col, _ = st.columns([1, 3])
with run_col:
    run_clicked = st.button("🚀 Run Full Career Analysis", type="primary", use_container_width=True)

if run_clicked:
    if not resume_text.strip():
        st.error("Please paste your resume text before running the multi-agent pipeline.")
    else:
        # Reset statuses
        st.session_state["crew_step_statuses"] = {s["step"]: "idle" for s in AGENT_STEPS}
        st.session_state["crew_results"] = None

        # Status update callback
        def update_status(step: int, label: str, status: str):
            st.session_state["crew_step_statuses"][step] = status

        try:
            from crew.workflow import CareerCrewWorkflow

            with st.spinner("🤖 Multi-agent crew is running..."):
                workflow = CareerCrewWorkflow()
                results = workflow.run(
                    resume_text=resume_text.strip(),
                    target_role=target_role,
                    status_callback=update_status
                )
            st.session_state["crew_results"] = results

            # Propagate results back to main session state so other pages can use them
            ctx = results.get("context", {})
            if ctx.get("gap_result"):
                st.session_state["gap_results"] = ctx["gap_result"]
            if ctx.get("roadmap_result"):
                st.session_state["roadmap_results"] = ctx["roadmap_result"]
            if ctx.get("interview_result"):
                st.session_state["interview_results"] = ctx["interview_result"]
            if ctx.get("project_result"):
                st.session_state["project_results"] = ctx["project_result"]
            if ctx.get("master_result"):
                st.session_state["master_results"] = ctx["master_result"]

            st.success(
                f"✅ Crew completed — {results['success_count']}/6 agents succeeded "
                f"({results['failed_count']} failed)."
            )
        except Exception as exc:
            st.error(f"Critical crew execution error: {str(exc)}")

# Re-render updated statuses
with step_panel.container():
    render_steps(st.session_state["crew_step_statuses"])

# ──────────────────────────────────────────────
# 4. Results Dashboard
# ──────────────────────────────────────────────
crew_results = st.session_state.get("crew_results")
if crew_results and crew_results.get("context", {}).get("master_result"):
    st.markdown('<div class="section-header">3. Final Career Assessment</div>', unsafe_allow_html=True)

    master = crew_results["context"]["master_result"]
    health = master.get("health_score", {})
    readiness = master.get("readiness_score", {})
    action_plan = master.get("action_plan", {})
    assessment = master.get("assessment", {})

    # KPI Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Career Health Score", f"{health.get('score', 'N/A')}/100")
        st.caption(health.get("label", ""))
    with c2:
        st.metric("Hiring Readiness", f"{readiness.get('score', 'N/A')}/100")
        st.caption(readiness.get("label", ""))
    with c3:
        gap_r = crew_results["context"].get("gap_result", {})
        st.metric("Skill Gap Score", f"{gap_r.get('gap_score', 'N/A')}%")
    with c4:
        st.metric("Missing Skills", len(gap_r.get("missing_skills", [])))

    st.markdown("---")

    # Step Summaries
    t1, t2, t3, t4 = st.tabs(["📊 Gap Analysis", "🗺️ Roadmap", "🎙️ Interview Prep", "🛠️ Projects"])

    with t1:
        gap_result = crew_results["context"].get("gap_result", {})
        st.markdown(f"**Matched Skills:** {', '.join(gap_result.get('matched_skills', [])) or 'None'}")
        st.markdown(f"**Missing Skills:** {', '.join(gap_result.get('missing_skills', [])) or 'None'}")

    with t2:
        roadmap = crew_results["context"].get("roadmap_result", {})
        st.markdown(f"**Timeline:** {roadmap.get('timeline_months', 'N/A')} months")
        for period, details in roadmap.get("monthly_plan", {}).items():
            if isinstance(details, dict):
                st.markdown(f"- **{period}:** {details.get('focus')} → {', '.join(details.get('skills', []))}")

    with t3:
        interview = crew_results["context"].get("interview_result", {})
        st.markdown(f"**Readiness Score:** {interview.get('readiness', {}).get('score', 'N/A')}%")
        risk_q = interview.get("weak_areas", {}).get("interview_risk_areas", [])
        if risk_q:
            st.markdown("**High-Risk Questions:**")
            for q in risk_q[:3]:
                st.markdown(f"  - {q}")

    with t4:
        proj = crew_results["context"].get("project_result", {})
        all_projects = proj.get("beginner", []) + proj.get("intermediate", []) + proj.get("advanced", [])
        top = sorted(all_projects, key=lambda x: x.get("composite_priority", 0), reverse=True)[:4]
        for p in top:
            st.markdown(f"**{p.get('title')}** ({p.get('difficulty_label', 'N/A')}) — Priority: {p.get('composite_priority', 0)}/100")

    st.markdown("---")

    # AI Career Advisor
    st.markdown('<div class="section-header">4. AI Career Advisor Summary</div>', unsafe_allow_html=True)
    st.write(assessment.get("career_summary", ""))
    
    col_s, col_r = st.columns(2)
    with col_s:
        st.markdown("**Key Strengths:**")
        for s in assessment.get("strengths_assessment", []):
            st.markdown(f"- {s}")
    with col_r:
        st.markdown("**Key Risks:**")
        for r in assessment.get("risks_assessment", []):
            st.markdown(f"- {r}")

    # Action Plan
    if action_plan:
        st.markdown('<div class="section-header">5. Unified Action Plan</div>', unsafe_allow_html=True)
        ca, cb = st.columns(2)
        with ca:
            st.markdown("**Next 7 Days:**")
            for item in action_plan.get("immediate_7_days", []):
                st.markdown(f"- {item}")
            st.markdown("**Next 90 Days:**")
            for item in action_plan.get("medium_term_90_days", []):
                st.markdown(f"- {item}")
        with cb:
            st.markdown("**Next 30 Days:**")
            for item in action_plan.get("short_term_30_days", []):
                st.markdown(f"- {item}")
            st.markdown("**6–12 Months:**")
            for item in action_plan.get("long_term_goals", []):
                st.markdown(f"- {item}")
