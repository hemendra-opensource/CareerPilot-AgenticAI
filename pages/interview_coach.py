import streamlit as st
from config.config import Config
from utils.role_database import ROLE_DATABASE
from agents.interview_agent import InterviewAgent

st.set_page_config(
    page_title="CareerPilot AI - Interview Coach",
    page_icon="🎙️",
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
            background: linear-gradient(135deg, #7F00FF 0%, #E100FF 100%);
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
            color: #465c82;
            margin-top: 1.5rem;
            margin-bottom: 0.8rem;
            border-left: 4px solid #7F00FF;
            padding-left: 0.5rem;
        }

        .badge-easy {
            background: #DEF7EC; color: #03543F;
            border-radius: 9999px; padding: 0.2rem 0.7rem;
            font-size: 0.78rem; font-weight: 700;
            display: inline-block; margin-right: 0.4rem;
        }
        .badge-medium {
            background: #FEFCBF; color: #744210;
            border-radius: 9999px; padding: 0.2rem 0.7rem;
            font-size: 0.78rem; font-weight: 700;
            display: inline-block; margin-right: 0.4rem;
        }
        .badge-hard {
            background: #FDE8E8; color: #9B1C1C;
            border-radius: 9999px; padding: 0.2rem 0.7rem;
            font-size: 0.78rem; font-weight: 700;
            display: inline-block; margin-right: 0.4rem;
        }
        .badge-category {
            background: #E9D8FD; color: #44337A;
            border-radius: 9999px; padding: 0.2rem 0.7rem;
            font-size: 0.78rem; font-weight: 700;
            display: inline-block; margin-right: 0.4rem;
        }

        .list-bullet {
            padding: 0.5rem;
            background-color: #F8F9FA;
            color: #495057;
            border-left: 3px solid #7F00FF;
            margin-bottom: 0.5rem;
            border-radius: 0 4px 4px 0;
        }

        .risk-bullet {
            padding: 0.5rem;
            background-color: #FFF5F5;
            border-left: 3px solid #FC8181;
            margin-bottom: 0.5rem;
            border-radius: 0 4px 4px 0;
            color: #742A2A;
        }

        .score-label {
            font-size: 1.1rem;
            font-weight: 600;
            margin-top: 0.4rem;
            margin-bottom: 0.2rem;
        }
    </style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────
st.markdown('<h1 class="page-title">🎙️ Interview Coach</h1>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Prepare for your interviews with role-specific questions, mock sessions, and AI coaching.</p>', unsafe_allow_html=True)

is_config_valid, config_msg = Config.validate()
if not is_config_valid:
    st.error(f"⚠️ Configuration Warning: {config_msg}")
    st.info("Please set your `GROQ_API_KEY` in the `.env` file.")
    st.stop()

# ──────────────────────────────────────────────
# Session State Data Loading
# ──────────────────────────────────────────────
completeness_score = 70.0
gap_score = 50.0
roadmap_current = 50.0
matched_skills = []
missing_skills = []
has_full_data = False

if 'analysis_results' in st.session_state and st.session_state['analysis_results']:
    completeness_score = float(
        st.session_state['analysis_results'].get('completeness_score', 70)
    )

if 'gap_results' in st.session_state and st.session_state['gap_results']:
    gap_data = st.session_state['gap_results']
    gap_score = float(gap_data.get('gap_score', 50))
    matched_skills = gap_data.get('matched_skills', [])
    missing_skills = gap_data.get('missing_skills', [])
    has_full_data = True

if 'roadmap_results' in st.session_state and st.session_state['roadmap_results']:
    roadmap_current = float(
        st.session_state['roadmap_results'].get('forecast', {}).get('current', 50)
    )

if has_full_data:
    default_role = st.session_state['gap_results'].get('target_role', 'Data Scientist')
    st.success(f"📂 Profile loaded — Role: **{default_role}** | Gap: **{gap_score}%** | Completeness: **{completeness_score}%**")
else:
    st.warning("⚠️ No full profile detected. Using default parameters. For best results, complete Resume Analysis and Skill Gap pages first.")
    default_role = 'Data Scientist'

# ──────────────────────────────────────────────
# 1. Selectors
# ──────────────────────────────────────────────
st.markdown('<div class="section-header">1. Interview Configuration</div>', unsafe_allow_html=True)
col_role, col_diff = st.columns(2)
with col_role:
    target_role = st.selectbox(
        "Select Target Role:",
        options=list(ROLE_DATABASE.keys()),
        index=list(ROLE_DATABASE.keys()).index(default_role) if default_role in ROLE_DATABASE else 0
    )
with col_diff:
    difficulty = st.selectbox(
        "Select Difficulty Level:",
        options=["Easy", "Medium", "Hard"]
    )

st.markdown("---")

# ──────────────────────────────────────────────
# 2. Run Analysis Button
# ──────────────────────────────────────────────
if st.button("🚀 Generate Interview Session", type="primary"):
    with st.spinner("Fetching questions, calculating readiness, and building AI coaching session..."):
        try:
            agent = InterviewAgent()
            results = agent.run_full_analysis(
                role=target_role,
                difficulty=difficulty,
                completeness_score=completeness_score,
                gap_score=gap_score,
                roadmap_current=roadmap_current,
                missing_skills=missing_skills,
                matched_skills=matched_skills
            )
            st.session_state['interview_results'] = results
            st.session_state['interview_role'] = target_role
            st.success("✅ Interview session generated successfully!")
        except Exception as e:
            st.error(f"Error generating interview session: {str(e)}")
            st.session_state['interview_results'] = None

# ──────────────────────────────────────────────
# 3. Render Results
# ──────────────────────────────────────────────
results = st.session_state.get('interview_results')

if results and results.get('role') == target_role:
    readiness = results['readiness']
    weak_areas = results['weak_areas']
    coaching = results['coaching']
    mock = results['mock_interview']

    # ── Readiness Score Card ──────────────────
    st.markdown('<div class="section-header">2. Interview Readiness Score</div>', unsafe_allow_html=True)
    col_score, col_breakdown = st.columns([1, 1])

    with col_score:
        score = readiness['score']
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #7F00FF 0%, #E100FF 100%);
                        padding:1.8rem; border-radius:12px; text-align:center;
                        color:white; box-shadow:0 4px 15px rgba(0,0,0,0.1);">
                <div style="font-size:0.9rem;font-weight:600;text-transform:uppercase;letter-spacing:1px;">
                    Interview Readiness
                </div>
                <div style="font-size:3.5rem;font-weight:700;margin-top:0.5rem;">{score}/100</div>
                <div style="font-size:1rem;margin-top:0.3rem;">{readiness['label']}</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.progress(score / 100.0)

    with col_breakdown:
        st.markdown("#### Score Breakdown")
        bd = readiness['breakdown']
        st.markdown(f"**Resume Completeness** (40% weight): `{bd['resume_completeness']} pts`")
        st.progress(bd['resume_completeness'] / 40.0)
        st.markdown(f"**Skill Match** (40% weight): `{bd['skill_match']} pts`")
        st.progress(bd['skill_match'] / 40.0)
        st.markdown(f"**Roadmap Coverage** (20% weight): `{bd['roadmap_coverage']} pts`")
        st.progress(bd['roadmap_coverage'] / 20.0)

    st.markdown("---")

    # ── Main Question Tabs ────────────────────
    st.markdown('<div class="section-header">3. Interview Questions</div>', unsafe_allow_html=True)

    def render_diff_badge(diff: str) -> str:
        cls = {"Easy": "badge-easy", "Medium": "badge-medium", "Hard": "badge-hard"}.get(diff, "badge-easy")
        return f'<span class="{cls}">{diff}</span>'

    tab_tech, tab_hr, tab_scenario, tab_mock = st.tabs([
        "⚙️ Technical", "🤝 HR", "🧩 Scenario", "🎭 Mock Interview"
    ])

    # ── Technical Questions ──
    with tab_tech:
        tech_qs = results['technical_questions']
        if tech_qs:
            for i, q in enumerate(tech_qs, 1):
                with st.expander(f"Q{i}: {q['question']}", expanded=False):
                    st.markdown(
                        f"{render_diff_badge(results['difficulty'])} "
                        f'<span class="badge-category">Technical</span>',
                        unsafe_allow_html=True
                    )
                    st.markdown("**Expected Answer Outline:**")
                    st.info(q['answer_outline'])
                    st.markdown("**Key Points Interviewer Looks For:**")
                    for point in q['key_points']:
                        st.markdown(f'<div class="list-bullet">✔ {point}</div>', unsafe_allow_html=True)
        else:
            st.info(f"No technical questions found for **{target_role}** at **{results['difficulty']}** difficulty.")

    # ── HR Questions ──
    with tab_hr:
        hr_qs = results['hr_questions']
        if hr_qs:
            for i, q in enumerate(hr_qs, 1):
                with st.expander(f"Q{i}: {q['question']}", expanded=False):
                    st.markdown(
                        f"{render_diff_badge(results['difficulty'])} "
                        f'<span class="badge-category">HR</span>',
                        unsafe_allow_html=True
                    )
                    st.markdown("**Expected Answer Outline:**")
                    st.info(q['answer_outline'])
                    st.markdown("**Key Points Interviewer Looks For:**")
                    for point in q['key_points']:
                        st.markdown(f'<div class="list-bullet">✔ {point}</div>', unsafe_allow_html=True)
        else:
            st.info(f"No HR questions found at **{results['difficulty']}** difficulty.")

    # ── Scenario Questions ──
    with tab_scenario:
        sc_qs = results['scenario_questions']
        if sc_qs:
            for i, q in enumerate(sc_qs, 1):
                with st.expander(f"Q{i}: {q['question']}", expanded=False):
                    st.markdown(
                        f"{render_diff_badge(results['difficulty'])} "
                        f'<span class="badge-category">Scenario</span>',
                        unsafe_allow_html=True
                    )
                    st.markdown("**Expected Answer Outline:**")
                    st.info(q['answer_outline'])
                    st.markdown("**Key Points Interviewer Looks For:**")
                    for point in q['key_points']:
                        st.markdown(f'<div class="list-bullet">✔ {point}</div>', unsafe_allow_html=True)
        else:
            st.info(f"No scenario questions found at **{results['difficulty']}** difficulty.")

    # ── Mock Interview ──
    with tab_mock:
        st.markdown(f"### 🎭 10-Question Mock Interview — {target_role}")
        st.caption("A randomized mix of Technical, HR, and Scenario questions across all difficulty levels.")
        st.markdown("---")
        for q in mock:
            diff_badge = render_diff_badge(q['difficulty'])
            cat_badge = f'<span class="badge-category">{q["category"]}</span>'
            with st.expander(f"Question {q['number']}: {q['question']}", expanded=False):
                st.markdown(f"{diff_badge} {cat_badge}", unsafe_allow_html=True)
                st.markdown("**Expected Answer Outline:**")
                st.info(q['answer_outline'])
                st.markdown("**Key Points:**")
                for point in q['key_points']:
                    st.markdown(f'<div class="list-bullet">✔ {point}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── Weak Areas ───────────────────────────
    st.markdown('<div class="section-header">4. Weak Areas & Interview Risk Zones</div>', unsafe_allow_html=True)
    col_weak, col_risk = st.columns(2)

    with col_weak:
        st.markdown("#### 🔴 Technical Weaknesses (Missing Skills)")
        tw = weak_areas.get('technical_weaknesses', [])
        if tw:
            for skill in tw:
                st.markdown(f'<div class="risk-bullet">⚠️ <strong>{skill}</strong> — Not yet acquired</div>',
                            unsafe_allow_html=True)
        else:
            st.success("✅ No critical technical weaknesses detected!")

    with col_risk:
        st.markdown("#### 🚨 Interview Risk Questions (Based on Missing Skills)")
        risks = weak_areas.get('interview_risk_areas', [])
        if risks:
            for risk in risks:
                st.markdown(f'<div class="risk-bullet">❓ {risk}</div>', unsafe_allow_html=True)
        else:
            st.success("✅ No high-risk question areas detected!")

    st.markdown("---")

    # ── AI Coaching Panel ────────────────────
    st.markdown('<div class="section-header">5. AI Interview Coaching</div>', unsafe_allow_html=True)
    st.info(coaching.get('preparation_summary', ''))

    col_focus, col_mistakes = st.columns(2)

    with col_focus:
        st.markdown("#### 📍 Key Focus Areas")
        for area in coaching.get('key_focus_areas', []):
            st.markdown(f'<div class="list-bullet">💡 {area}</div>', unsafe_allow_html=True)

    with col_mistakes:
        st.markdown("#### ❌ Common Mistakes to Avoid")
        for mistake in coaching.get('common_mistakes', []):
            st.markdown(f'<div class="risk-bullet">🚫 {mistake}</div>', unsafe_allow_html=True)

    st.markdown("#### ✅ Final Recommendations")
    for rec in coaching.get('final_recommendations', []):
        st.markdown(f'<div class="list-bullet">🏆 {rec}</div>', unsafe_allow_html=True)
