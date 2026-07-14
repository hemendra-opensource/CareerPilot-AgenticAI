import streamlit as st
from config.config import Config
from utils.role_database import ROLE_DATABASE
from agents.roadmap_agent import RoadmapAgent
from agents.skill_gap_agent import SkillMatcher

st.set_page_config(
    page_title="CareerPilot AI - Roadmap Generator",
    page_icon="🗺️",
    layout="wide"
)

# Custom Styling
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
            border-left: 4px solid #FF416C;
            padding-left: 0.5rem;
        }
        
        .timeline-card {
            background-color: #F8F9FA;
            border-left: 5px solid #FF416C;
            padding: 1.2rem;
            border-radius: 0 8px 8px 0;
            margin-bottom: 1.2rem;
            box-shadow: 0 2px 5px rgba(0,0,0,0.02);
        }
        
        .timeline-time {
            font-weight: 700;
            color: #FF416C;
            font-size: 1.1rem;
            margin-bottom: 0.3rem;
        }
        
        .timeline-focus {
            font-weight: 600;
            color: #1F2937;
            font-size: 0.95rem;
            margin-bottom: 0.5rem;
        }
        
        .priority-high {
            background-color: #FDE8E8;
            color: #9B1C1C;
            font-weight: bold;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
        }
        
        .priority-medium {
            background-color: #FEFCBF;
            color: #744210;
            font-weight: bold;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
        }
        
        .priority-low {
            background-color: #E5E7EB;
            color: #374151;
            font-weight: bold;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="page-title">🗺️ Career Roadmap Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Build your step-by-step career development program complete with monthly schedules and resources.</p>', unsafe_allow_html=True)

# Verify API configuration
is_config_valid, config_msg = Config.validate()
if not is_config_valid:
    st.error(f"⚠️ Configuration Warning: {config_msg}")
    st.info("Please set your `GROQ_API_KEY` in the `.env` file to enable AI parsing and feedback.")
else:
    candidate_skills = []
    target_role = ""
    gap_score = 0.0
    has_results = False
    
    # Check session state for previous results
    if 'gap_results' in st.session_state and st.session_state['gap_results']:
        results = st.session_state['gap_results']
        candidate_skills = results.get("matched_skills", []) + results.get("additional_skills", [])
        target_role = results.get("target_role", "")
        gap_score = results.get("gap_score", 0.0)
        st.success(f"📂 Loaded skill gap data for **{target_role}** (Gap Score: {gap_score}%)")
        has_results = True
    else:
        st.warning("⚠️ No active skill gap analysis detected. Please navigate to the Skill Gap Analyzer page first, or input custom parameters below:")
        
    if not has_results:
        # Fallback inputs
        target_role = st.selectbox("Select Target Role:", options=list(ROLE_DATABASE.keys()))
        manual_skills = st.text_area("Enter your skills (separated by commas):", value="Python, SQL, Git")
        candidate_skills = [s.strip() for s in manual_skills.split(",") if s.strip()]
        
        # Calculate gap score deterministically
        if candidate_skills:
            req_skills = ROLE_DATABASE[target_role]
            match = SkillMatcher.match_skills(candidate_skills, req_skills)
            gap_score = match["gap_score"]
            
    st.markdown("---")
    
    if st.button("Generate Personalized Career Roadmap", type="primary"):
        if not candidate_skills:
            st.error("Please ensure you have entered skills before generating the roadmap.")
        else:
            with st.spinner("Generating personalized career roadmap and querying AI coach..."):
                try:
                    agent = RoadmapAgent()
                    roadmap_data = agent.generate_roadmap(candidate_skills, target_role, gap_score)
                    st.session_state['roadmap_results'] = roadmap_data
                    st.session_state['roadmap_target'] = target_role
                    st.success("✅ Roadmap generated successfully!")
                except Exception as e:
                    st.error(f"Error generating roadmap: {str(e)}")
                    st.session_state['roadmap_results'] = None
                    
    # Render Roadmap results
    roadmap = st.session_state.get('roadmap_results')
    
    if roadmap and roadmap.get('target_role') == target_role:
        stages = roadmap["stages"]
        timeline_months = roadmap["timeline_months"]
        monthly_plan = roadmap["monthly_plan"]
        priority_matrix = roadmap["priority_matrix"]
        resource_repository = roadmap["resource_repository"]
        forecast = roadmap["forecast"]
        
        # 1. Summary Metrics
        st.markdown('<div class="section-header">1. Roadmap Overview</div>', unsafe_allow_html=True)
        col_r1, col_r2, col_r3 = st.columns(3)
        with col_r1:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%); padding: 1.5rem; border-radius: 12px; text-align: center; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                    <div style="font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Selected Role</div>
                    <div style="font-size: 2rem; font-weight: 700; margin-top: 0.5rem;">{target_role}</div>
                </div>
            """, unsafe_allow_html=True)
        with col_r2:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #360033 0%, #0b8793 100%); padding: 1.5rem; border-radius: 12px; text-align: center; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                    <div style="font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Roadmap Duration</div>
                    <div style="font-size: 2.8rem; font-weight: 700; margin-top: 0.5rem;">{timeline_months} Months</div>
                </div>
            """, unsafe_allow_html=True)
        with col_r3:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #e65c00 0%, #F9D423 100%); padding: 1.5rem; border-radius: 12px; text-align: center; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                    <div style="font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Current Gap Score</div>
                    <div style="font-size: 2.8rem; font-weight: 700; margin-top: 0.5rem;">{gap_score}%</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 2. Roadmap Stages (Beginner, Intermediate, Advanced)
        st.markdown('<div class="section-header">2. Career Development Milestones</div>', unsafe_allow_html=True)
        c_beg, c_int, c_adv = st.columns(3)
        
        with c_beg:
            st.markdown("### 🟢 Beginner Stage")
            for item in stages["Beginner"]:
                icon = "✅" if item["status"] == "Matched" else "🔴"
                st.write(f"{icon} **{item['skill']}** ({item['status']})")
                
        with c_int:
            st.markdown("### 🟡 Intermediate Stage")
            for item in stages["Intermediate"]:
                icon = "✅" if item["status"] == "Matched" else "🔴"
                st.write(f"{icon} **{item['skill']}** ({item['status']})")
                
        with c_adv:
            st.markdown("### 🔵 Advanced Stage")
            for item in stages["Advanced"]:
                icon = "✅" if item["status"] == "Matched" else "🔴"
                st.write(f"{icon} **{item['skill']}** ({item['status']})")
                
        st.markdown("---")
        
        # 3. Monthly Timeline Plan
        st.markdown('<div class="section-header">3. Month-by-Month Schedule</div>', unsafe_allow_html=True)
        for month_range, content in monthly_plan.items():
            st.markdown(f"""
                <div class="timeline-card">
                    <div class="timeline-time">⏱️ {month_range}</div>
                    <div class="timeline-focus">Focus Area: {content['focus']}</div>
                    <div>Skills to study / reinforce: <strong>{', '.join(content['skills'])}</strong></div>
                </div>
            """, unsafe_allow_html=True)
            
        # 4. Priority Ranking Matrix & Resource Suggestions
        st.markdown('<div class="section-header">4. Skill Priorities & Study Resources</div>', unsafe_allow_html=True)
        tab_pri, tab_res = st.tabs(["🎯 Skill Priority Matrix", "📚 Recommended Study Resources"])
        
        with tab_pri:
            st.markdown("Review the priority classification of your skills for this career path:")
            
            p_cols = st.columns(3)
            with p_cols[0]:
                st.markdown('<span class="priority-high">🔥 HIGH PRIORITY (Missing Required)</span>', unsafe_allow_html=True)
                st.write("")
                for s in priority_matrix["High"]:
                    st.write(f"- **{s}**")
                if not priority_matrix["High"]:
                    st.info("No high priority gaps.")
            with p_cols[1]:
                st.markdown('<span class="priority-medium">⚡ MEDIUM PRIORITY (Possessed Required)</span>', unsafe_allow_html=True)
                st.write("")
                for s in priority_matrix["Medium"]:
                    st.write(f"- **{s}**")
            with p_cols[2]:
                st.markdown('<span class="priority-low">💡 LOW PRIORITY (Possessed Electives)</span>', unsafe_allow_html=True)
                st.write("")
                for s in priority_matrix["Low"]:
                    st.write(f"- **{s}**")
                    
        with tab_res:
            st.markdown("Interactive resource repository for missing skills:")
            if resource_repository:
                for skill, res in resource_repository.items():
                    with st.expander(f"📚 {skill} - Learning Materials"):
                        st.markdown(f"**Official Documentation:** [Link]({res['docs']})")
                        st.markdown(f"**Recommended Course:** {res['course']}")
                        st.markdown(f"**Practice Platform:** {res['practice']}")
            else:
                st.success("No missing skills to recommend resources for!")
                
        st.markdown("---")
        
        # 5. Career Readiness Forecast & AI Guidance
        st.markdown('<div class="section-header">5. Career Readiness Forecast & AI Guidance</div>', unsafe_allow_html=True)
        
        col_fore, col_guide = st.columns([1, 1])
        
        with col_fore:
            st.markdown("#### Readiness Timeline Forecast")
            
            # Current
            st.write(f"**Current Career Readiness:** {forecast['current']}%")
            st.progress(forecast['current'] / 100.0)
            st.caption(forecast['comments'].get("current_readiness_comment", ""))
            
            # Midpoint
            st.write(f"**Midpoint Readiness Forecast:** {forecast['midpoint']}%")
            st.progress(forecast['midpoint'] / 100.0)
            st.caption(forecast['comments'].get("projected_readiness_comment", ""))
            
            # Final
            st.write(f"**Readiness After Roadmap Completion:** {forecast['final']}%")
            st.progress(forecast['final'] / 100.0)
            st.caption(forecast['comments'].get("post_completion_readiness_comment", ""))
            
        with col_guide:
            st.markdown("#### AI Strategic Guidance")
            st.info(forecast['comments'].get("ai_roadmap_explanation", ""))
