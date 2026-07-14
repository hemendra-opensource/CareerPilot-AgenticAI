import streamlit as st
from config.config import Config
from utils.role_database import ROLE_DATABASE
from agents.project_agent import ProjectAgent

st.set_page_config(
    page_title="CareerPilot AI - Project Recommender",
    page_icon="🛠️",
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
            background: linear-gradient(135deg, #00B4DB 0%, #0083B0 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }

        .page-subtitle {
            font-size: 1.1rem;
            color: #6C757D;
            margin-bottom: 2rem;
        }

        .section-header {
            font-size: 1.3rem;
            font-weight: 600;
            color: #2D3748;
            margin-top: 1.5rem;
            margin-bottom: 0.8rem;
            border-left: 4px solid #00B4DB;
            padding-left: 0.5rem;
        }

        .badge-beginner {
            background: #DEF7EC; color: #03543F;
            border-radius: 9999px; padding: 0.2rem 0.7rem;
            font-size: 0.78rem; font-weight: 700;
            display: inline-block; margin-right: 0.4rem;
        }
        .badge-intermediate {
            background: #FEFCBF; color: #744210;
            border-radius: 9999px; padding: 0.2rem 0.7rem;
            font-size: 0.78rem; font-weight: 700;
            display: inline-block; margin-right: 0.4rem;
        }
        .badge-advanced {
            background: #FDE8E8; color: #9B1C1C;
            border-radius: 9999px; padding: 0.2rem 0.7rem;
            font-size: 0.78rem; font-weight: 700;
            display: inline-block; margin-right: 0.4rem;
        }
        .badge-gap {
            background: linear-gradient(135deg, #7F00FF 0%, #E100FF 100%);
            color: white;
            border-radius: 9999px; padding: 0.2rem 0.8rem;
            font-size: 0.78rem; font-weight: 700;
            display: inline-block; margin-right: 0.4rem;
        }
        .skill-tag {
            background: #EBF8FF; color: #2B6CB0;
            border-radius: 6px; padding: 0.15rem 0.5rem;
            font-size: 0.75rem; font-weight: 600;
            display: inline-block; margin: 0.15rem;
        }
        .skill-tag-missing {
            background: #FFF5F5; color: #9B1C1C;
            border-radius: 6px; padding: 0.15rem 0.5rem;
            font-size: 0.75rem; font-weight: 600;
            display: inline-block; margin: 0.15rem;
            border: 1px solid #FC8181;
        }
        .list-bullet {
            padding: 0.4rem 0.6rem;
            background-color: #F8F9FA;
            color: #495057;
            border-left: 3px solid #6C63FF;
            margin-bottom: 0.4rem;
            border-radius: 0 4px 4px 0;
        
            border-left: 3px solid #00B4DB;
            margin-bottom: 0.4rem;
            border-radius: 0 4px 4px 0;
            border-left: 3px solid #00B4DB;
        }
        .phase-item {
            padding: 0.4rem 0.6rem;
            background-color: #F0FFF4;
            border-left: 3px solid #38A169;
            margin-bottom: 0.4rem;
            border-radius: 0 4px 4px 0;
            font-size: 0.9rem;
        }
        .impact-label {
            font-size: 0.82rem;
            font-weight: 600;
            color: #4A5568;
            margin-bottom: 0.1rem;
        }
    </style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────
st.markdown('<h1 class="page-title">🛠️ Project Recommender</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="page-subtitle">Discover practical projects that close your skill gaps, '
    'build your portfolio, and maximize your hiring readiness.</p>',
    unsafe_allow_html=True
)

is_config_valid, config_msg = Config.validate()
if not is_config_valid:
    st.error(f"⚠️ Configuration Warning: {config_msg}")
    st.info("Please set your `GROQ_API_KEY` in the `.env` file.")
    st.stop()

# ──────────────────────────────────────────────
# Session State Loading
# ──────────────────────────────────────────────
missing_skills: list[str] = []
matched_skills: list[str] = []
gap_score: float = 50.0
readiness_score: float = 50.0
roadmap_current: float = 50.0
has_full_data = False
default_role = "Data Scientist"

if "gap_results" in st.session_state and st.session_state["gap_results"]:
    gap_data = st.session_state["gap_results"]
    gap_score = float(gap_data.get("gap_score", 50))
    missing_skills = gap_data.get("missing_skills", [])
    matched_skills = gap_data.get("matched_skills", [])
    default_role = gap_data.get("target_role", "Data Scientist")
    has_full_data = True

# Pull readiness score from Phase 5 interview session (if available)
if "interview_results" in st.session_state and st.session_state["interview_results"]:
    readiness_score = float(
        st.session_state["interview_results"].get("readiness", {}).get("score", 50)
    )
elif has_full_data:
    # Derive approximate readiness from gap_score if Phase 5 hasn't run yet
    readiness_score = max(0.0, round(100.0 - gap_score, 1))

# Pull roadmap progress from Phase 4 forecast (if available)
if "roadmap_results" in st.session_state and st.session_state["roadmap_results"]:
    roadmap_current = float(
        st.session_state["roadmap_results"].get("forecast", {}).get("current", 50)
    )

if has_full_data:
    st.success(
        f"📂 Profile loaded — Role: **{default_role}** | "
        f"Gap: **{gap_score}%** | Readiness: **{readiness_score}%** | "
        f"Roadmap Progress: **{roadmap_current}%**"
    )
else:
    st.warning(
        "⚠️ No Skill Gap data found. Using defaults. "
        "Complete the Skill Gap Analyzer first for personalized recommendations."
    )

# ──────────────────────────────────────────────
# 1. Configuration
# ──────────────────────────────────────────────
st.markdown('<div class="section-header">1. Recommendation Configuration</div>', unsafe_allow_html=True)
col_role, col_spacer = st.columns([1, 1])
with col_role:
    target_role = st.selectbox(
        "Select Target Role:",
        options=list(ROLE_DATABASE.keys()),
        index=list(ROLE_DATABASE.keys()).index(default_role)
        if default_role in ROLE_DATABASE else 0
    )

# Missing skills display
if missing_skills:
    st.markdown("**🔴 Missing Skills Detected (Gap-Priority Targets):**")
    tags_html = " ".join(
        f'<span class="skill-tag-missing">⚠ {s}</span>' for s in missing_skills
    )
    st.markdown(tags_html, unsafe_allow_html=True)

st.markdown("---")

# ──────────────────────────────────────────────
# 2. Generate Button
# ──────────────────────────────────────────────
if st.button("🚀 Generate Project Recommendations", type="primary"):
    with st.spinner("Analyzing skill gaps, scoring projects, and generating AI coaching..."):
        try:
            agent = ProjectAgent()
            results = agent.run_full_analysis(
                role=target_role,
                missing_skills=missing_skills,
                matched_skills=matched_skills,
                gap_score=gap_score,
                readiness_score=readiness_score,
                roadmap_current=roadmap_current
            )
            st.session_state["project_results"] = results
            st.session_state["project_role"] = target_role
            st.success("✅ Project recommendations generated successfully!")
        except Exception as e:
            st.error(f"Error generating recommendations: {str(e)}")
            st.session_state["project_results"] = None

# ──────────────────────────────────────────────
# 3. Render Results
# ──────────────────────────────────────────────
results = st.session_state.get("project_results")

if results and results.get("role") == target_role:
    stats = results["stats"]
    coaching = results["coaching"]

    # ── Stats Row ────────────────────────────
    st.markdown('<div class="section-header">2. Recommendation Overview</div>', unsafe_allow_html=True)
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Total Projects", stats["total_projects"])
    c2.metric("Gap-Closing Projects", stats["gap_closers"])
    c3.metric("Avg Portfolio Impact", f"{stats['avg_portfolio_impact']}%")
    c4.metric("Missing Skills", len(missing_skills))
    c5.metric("Readiness Score", f"{stats.get('readiness_score', readiness_score)}%")
    c6.metric("Roadmap Progress", f"{stats.get('roadmap_current', roadmap_current)}%")

    # Priority scoring legend
    st.caption(
        "📐 **Priority Formula:** Missing Skills (40%) + Difficulty Alignment (30%) "
        "+ Readiness Score (20%) + Roadmap Progress (10%)"
    )
    st.markdown("---")

    # ──────────────────────────────────────────
    # Helper: render a list of project cards
    # ──────────────────────────────────────────
    def render_project_card(p: dict, diff_label: str, diff_css: str) -> None:
        """Renders a single project as a styled expander card."""
        gap_badge = (
            '<span class="badge-gap">🎯 Gap Closer</span>'
            if p.get("is_gap_closer") else ""
        )
        header = f"{p['title']}"
        with st.expander(header, expanded=False):
            # Badges row
            st.markdown(
                f'<span class="{diff_css}">{diff_label}</span>'
                f'<span style="color:#888;font-size:0.82rem">⏱ {p["duration"]}</span>'
                f"&nbsp;&nbsp;{gap_badge}",
                unsafe_allow_html=True
            )
            st.markdown("<br>", unsafe_allow_html=True)

            col_desc, col_scores = st.columns([2, 1])
            with col_desc:
                st.markdown(f"**📋 Description:**")
                st.info(p["description"])

                # Skills Required
                st.markdown("**✅ Skills Required:**")
                req_html = " ".join(
                    f'<span class="skill-tag">{s}</span>'
                    for s in p.get("skills_required", [])
                )
                st.markdown(req_html or "—", unsafe_allow_html=True)

                # Skills Learned
                st.markdown("<br>**🎓 Skills You Will Learn:**", unsafe_allow_html=True)
                learned = p.get("skills_learned", [])
                missing_lower = {s.lower() for s in missing_skills}
                learned_html = " ".join(
                    f'<span class="skill-tag-missing">{s}</span>'
                    if s.lower() in missing_lower
                    else f'<span class="skill-tag">{s}</span>'
                    for s in learned
                )
                st.markdown(learned_html or "—", unsafe_allow_html=True)

                # Companies
                st.markdown(
                    "<br>**🏢 Companies That Value This:**",
                    unsafe_allow_html=True
                )
                co_html = " ".join(
                    f'<span class="skill-tag">{c}</span>'
                    for c in p.get("companies_that_value", [])
                )
                st.markdown(co_html or "—", unsafe_allow_html=True)

            with col_scores:
                st.markdown("**📊 Impact Scores:**")
                pi = p.get("portfolio_impact", 0)
                ri = p.get("resume_impact", 0)
                hv = p.get("hiring_value", 0)
                gp = p.get("gap_priority", 0)
                cp = p.get("composite_priority", 0.0)

                # Composite Priority Score (headline)
                st.markdown(
                    f'<div class="impact-label" style="color:#7F00FF;font-size:0.95rem;">'
                    f'Priority Score: {cp}/100</div>',
                    unsafe_allow_html=True
                )
                st.progress(cp / 100)

                st.markdown("---")
                st.markdown(f'<div class="impact-label">Portfolio Impact: {pi}/100</div>', unsafe_allow_html=True)
                st.progress(pi / 100)

                st.markdown(f'<div class="impact-label">Resume Impact: {ri}/100</div>', unsafe_allow_html=True)
                st.progress(ri / 100)

                st.markdown(f'<div class="impact-label">Hiring Value: {hv}/100</div>', unsafe_allow_html=True)
                st.progress(hv / 100)

                if gp > 0:
                    st.markdown(f'<div class="impact-label">Gap-Closing Score: {gp} skill(s) addressed</div>', unsafe_allow_html=True)
                    st.progress(min(gp / 5, 1.0))

            # Dev Phases
            st.markdown("**🗺️ Project Development Roadmap:**")
            for phase in p.get("dev_phases", []):
                st.markdown(f'<div class="phase-item">🔹 {phase}</div>', unsafe_allow_html=True)

    # ── Project Tabs ────────────────────────
    st.markdown('<div class="section-header">3. Recommended Projects by Difficulty</div>', unsafe_allow_html=True)
    tab_beg, tab_int, tab_adv = st.tabs([
        "🌱 Beginner", "⚙️ Intermediate", "🚀 Advanced"
    ])

    with tab_beg:
        for p in results["beginner"]:
            render_project_card(p, "Beginner", "badge-beginner")

    with tab_int:
        for p in results["intermediate"]:
            render_project_card(p, "Intermediate", "badge-intermediate")

    with tab_adv:
        for p in results["advanced"]:
            render_project_card(p, "Advanced", "badge-advanced")

    st.markdown("---")

    # ── Career Impact Analysis ──────────────
    st.markdown('<div class="section-header">4. Career Impact Analysis</div>', unsafe_allow_html=True)
    st.caption("All projects ranked by combined portfolio + hiring value. Red skill tags = gap-closing skills.")

    impact_data = sorted(
        results["career_impact"],
        key=lambda x: x.get("portfolio_impact", 0) + x.get("hiring_value", 0),
        reverse=True
    )
    for item in impact_data:
        cols = st.columns([3, 1, 1, 1])
        cols[0].markdown(
            f"**{item['title']}** "
            f"{'🎯' if item.get('is_gap_closer') else ''} "
            f"— ⏱ {item['duration']}"
        )
        cols[1].metric("Portfolio", f"{item['portfolio_impact']}%")
        cols[2].metric("Resume", f"{item['resume_impact']}%")
        cols[3].metric("Hiring", f"{item['hiring_value']}%")

    st.markdown("---")

    # ── AI Recommendations ──────────────────
    st.markdown('<div class="section-header">5. AI Project Coaching</div>', unsafe_allow_html=True)
    st.info(coaching.get("overall_strategy", ""))

    col_seq, col_wins = st.columns(2)
    with col_seq:
        st.markdown("#### 🗂️ Recommended Build Sequence")
        for step in coaching.get("recommended_sequence", []):
            st.markdown(f'<div class="list-bullet">🔢 {step}</div>', unsafe_allow_html=True)

    with col_wins:
        st.markdown("#### ⚡ Quick Wins (Start Here)")
        for win in coaching.get("quick_wins", []):
            st.markdown(f'<div class="list-bullet">🏃 {win}</div>', unsafe_allow_html=True)

    st.markdown("#### 🎯 Long-Term Portfolio Goals")
    for goal in coaching.get("long_term_goals", []):
        st.markdown(f'<div class="list-bullet">🏆 {goal}</div>', unsafe_allow_html=True)

    st.markdown("---")
    note = coaching.get("motivational_note", "")
    if note:
        st.success(f"💬 {note}")
