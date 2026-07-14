import streamlit as st
from config.config import Config
from utils.role_database import ROLE_DATABASE
from agents.skill_gap_agent import SkillGapAgent

st.set_page_config(
    page_title="CareerPilot AI - Skill Gap Analyzer",
    page_icon="⚖️",
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
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
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
            border-left: 4px solid #11998e;
            padding-left: 0.5rem;
        }
        
        /* Badges styling */
        .badge-matched {
            background-color: #DEF7EC;
            color: #03543F;
            border: 1px solid #BCF0DA;
            border-radius: 9999px;
            padding: 0.3rem 0.8rem;
            font-size: 0.85rem;
            font-weight: 600;
            display: inline-block;
            margin: 0.2rem;
        }
        
        .badge-missing {
            background-color: #FDE8E8;
            color: #9B1C1C;
            border: 1px solid #FBD5D5;
            border-radius: 9999px;
            padding: 0.3rem 0.8rem;
            font-size: 0.85rem;
            font-weight: 600;
            display: inline-block;
            margin: 0.2rem;
        }
        
        .badge-additional {
            background-color: #F3F4F6;
            color: #374151;
            border: 1px solid #E5E7EB;
            border-radius: 9999px;
            padding: 0.3rem 0.8rem;
            font-size: 0.85rem;
            font-weight: 500;
            display: inline-block;
            margin: 0.2rem;
        }
        
        .list-bullet {
            padding: 0.5rem;
            background-color: #F8F9FA;
            color : #495057;
            border-left: 3px solid #11998e;
            margin-bottom: 0.5rem;
            border-radius: 0 4px 4px 0;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="page-title">⚖️ Skill Gap Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Compare your current resume skills against target roles to map your career readiness.</p>', unsafe_allow_html=True)

# Verify API configuration
is_config_valid, config_msg = Config.validate()
if not is_config_valid:
    st.error(f"⚠️ Configuration Warning: {config_msg}")
    st.info("Please set your `GROQ_API_KEY` in the `.env` file to enable AI parsing and feedback.")
else:
    # 1. Target Role Selection
    st.markdown('<div class="section-header">1. Select Target Career Role</div>', unsafe_allow_html=True)
    target_role = st.selectbox(
        "Choose your target career path:",
        options=list(ROLE_DATABASE.keys())
    )
    
    # 2. Extract Candidate Skills
    st.markdown('<div class="section-header">2. Candidate Skills Input</div>', unsafe_allow_html=True)
    
    candidate_skills = []
    has_parsed_resume = False
    
    if 'analysis_results' in st.session_state and st.session_state['analysis_results']:
        candidate_skills = st.session_state['analysis_results']['parsed_data'].get('skills', [])
        filename = st.session_state.get('uploaded_filename', 'Parsed Resume')
        st.success(f"📂 Loaded skills from parsed resume: **{filename}**")
        has_parsed_resume = True
    else:
        st.warning("⚠️ No active parsed resume detected. Please upload your resume on the Resume Analyzer page first, or input custom skills manually below:")
        
    # Render skills tag viewer or manual editor
    if has_parsed_resume:
        # Show skills tags
        skills_html = "".join([f'<span class="badge-additional">{skill}</span>' for skill in candidate_skills])
        st.markdown(skills_html, unsafe_allow_html=True)
        # Checkbox to override manual entry if they want
        if st.checkbox("Override and enter skills manually"):
            has_parsed_resume = False
            
    if not has_parsed_resume:
        # Manual entry fallback text area
        manual_input = st.text_area(
            "Enter your skills (separated by commas):",
            value="Python, SQL, HTML, CSS, JavaScript, Git"
        )
        candidate_skills = [s.strip() for s in manual_input.split(",") if s.strip()]

    st.markdown("---")
    
    # 3. Trigger Analysis
    if st.button("Run Skill Gap Analysis", type="primary"):
        if not candidate_skills:
            st.error("Please enter at least one skill to perform the analysis.")
        else:
            with st.spinner("Calculating skill alignments and generating AI coach feedback..."):
                try:
                    agent = SkillGapAgent()
                    results = agent.analyze_gaps(candidate_skills, target_role)
                    
                    st.session_state['gap_results'] = results
                    st.session_state['gap_target_role'] = target_role
                    st.success("✅ Analysis completed successfully!")
                except Exception as e:
                    st.error(f"Error executing analysis: {str(e)}")
                    st.session_state['gap_results'] = None

    # Render Results if available in Session State
    results = st.session_state.get('gap_results')
    
    if results and results.get('target_role') == target_role:
        gap_score = results["gap_score"]
        readiness_score = 100 - gap_score
        matched_skills = results["matched_skills"]
        missing_skills = results["missing_skills"]
        additional_skills = results["additional_skills"]
        advice = results["advice"]
        
        # 4. Gap Score Metrics & Career Readiness Meter
        st.markdown('<div class="section-header">3. Skill Alignment Metrics</div>', unsafe_allow_html=True)
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); padding: 1.5rem; border-radius: 12px; text-align: center; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                    <div style="font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Career Readiness</div>
                    <div style="font-size: 2.8rem; font-weight: 700; margin-top: 0.5rem;">{readiness_score}%</div>
                </div>
            """, unsafe_allow_html=True)
        with col_m2:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f857a6 0%, #ff5858 100%); padding: 1.5rem; border-radius: 12px; text-align: center; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                    <div style="font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Skill Gap Score</div>
                    <div style="font-size: 2.8rem; font-weight: 700; margin-top: 0.5rem;">{gap_score}%</div>
                </div>
            """, unsafe_allow_html=True)
        with col_m3:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%); padding: 1.5rem; border-radius: 12px; text-align: center; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                    <div style="font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Matched Skills</div>
                    <div style="font-size: 2.8rem; font-weight: 700; margin-top: 0.5rem;">{len(matched_skills)}/{len(results["required_skills"])}</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Career Alignment Progress**")
        st.progress(readiness_score / 100.0)
        
        # 5. Split lists showing possessed vs missing skills
        st.markdown('<div class="section-header">4. Skill Matching Breakdown</div>', unsafe_allow_html=True)
        
        col_matched, col_missing, col_additional = st.columns(3)
        
        with col_matched:
            st.markdown("### Possessed required skills (Green)")
            if matched_skills:
                matched_html = "".join([f'<span class="badge-matched">{skill}</span>' for skill in matched_skills])
                st.markdown(matched_html, unsafe_allow_html=True)
            else:
                st.info("No required skills matched.")
                
        with col_missing:
            st.markdown("### Missing required skills (Red)")
            if missing_skills:
                missing_html = "".join([f'<span class="badge-missing">{skill}</span>' for skill in missing_skills])
                st.markdown(missing_html, unsafe_allow_html=True)
            else:
                st.success("🎉 You possess all required skills for this role!")
                
        with col_additional:
            st.markdown("### Additional Skills (Possessed but not required)")
            if additional_skills:
                additional_html = "".join([f'<span class="badge-additional">{skill}</span>' for skill in additional_skills])
                st.markdown(additional_html, unsafe_allow_html=True)
            else:
                st.info("No additional skills detected.")
                
        st.markdown("---")
        
        # 6. AI Recommendations Panel
        st.markdown('<div class="section-header">5. AI Career Recommendations & Roadmap</div>', unsafe_allow_html=True)
        
        st.markdown("#### Readiness Summary")
        st.info(advice.get("career_readiness_summary", ""))
        
        col_learn, col_hiring = st.columns(2)
        
        with col_learn:
            st.markdown("#### 🎯 Top Skills to Learn")
            top_skills = advice.get("top_skills_to_learn", [])
            if top_skills:
                for skill in top_skills:
                    st.markdown(f'<div class="list-bullet">💡 {skill}</div>', unsafe_allow_html=True)
            else:
                st.write("No missing skills to prioritize.")
                
        with col_hiring:
            st.markdown("#### 💼 Hiring Readiness Assessment")
            st.write(advice.get("hiring_readiness_assessment", ""))
            
        st.markdown("#### 🗺️ Recommended Learning Sequence")
        sequence = advice.get("learning_sequence", [])
        if sequence:
            for step in sequence:
                st.markdown(f'<div class="list-bullet">🏁 {step}</div>', unsafe_allow_html=True)
        else:
            st.write("No learning steps generated.")
