import streamlit as st
from config.config import Config
from agents.resume_agent import ResumeAnalyzerAgent

st.set_page_config(
    page_title="CareerPilot AI - Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# Custom Premium Styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        
        .page-title {
            background: linear-gradient(135deg, #4E54C8 0%, #8F94FB 100%);
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
        
        .metric-card {
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            color: white;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        }
        
        .section-header {
            font-size: 1.3rem;
            font-weight: 600;
            color: #2D3748;
            margin-top: 1.5rem;
            margin-bottom: 0.8rem;
            border-left: 4px solid #4E54C8;
            padding-left: 0.5rem;
        }
        
        .list-bullet {
            padding: 0.5rem;
            background-color: #F8F9FA;
            color : #495057;
            border-left: 3px solid #6B7280;
            margin-bottom: 0.5rem;
            border-radius: 0 4px 4px 0;
        }
        
        .badge {
            background-color: #EDF2F7;
            color: #2D3748;
            border-radius: 9999px;
            padding: 0.3rem 0.8rem;
            font-size: 0.85rem;
            font-weight: 500;
            display: inline-block;
            margin: 0.2rem;
        }
        
        .keyword-badge {
            background-color: #FEFCBF;
            color: #744210;
            border-radius: 9999px;
            padding: 0.3rem 0.8rem;
            font-size: 0.85rem;
            font-weight: 500;
            display: inline-block;
            margin: 0.2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Main Title & Subtitle
st.markdown('<h1 class="page-title">📄 Resume Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Analyze your resume, score your ATS compatibility, and identify improvement opportunities.</p>', unsafe_allow_html=True)

# Verify API configuration
is_config_valid, config_msg = Config.validate()
if not is_config_valid:
    st.error(f"⚠️ Configuration Warning: {config_msg}")
    st.info("Please set your `GROQ_API_KEY` in the `.env` file to enable AI parsing and feedback.")
else:
    # Form for resume upload
    st.markdown("### 1. Upload Resume")
    uploaded_file = st.file_uploader("Upload your resume in PDF format:", type=["pdf"])
    
    if uploaded_file is not None:
        # Prevent parsing on every click by storing in session state
        if 'analysis_results' not in st.session_state or st.session_state.get('uploaded_filename') != uploaded_file.name:
            with st.spinner("Analyzing resume... This includes PDF text extraction, profile parsing, and ATS auditing."):
                try:
                    agent = ResumeAnalyzerAgent()
                    results = agent.analyze_resume(uploaded_file)
                    st.session_state['analysis_results'] = results
                    st.session_state['uploaded_filename'] = uploaded_file.name
                    st.success("✅ Analysis completed successfully!")
                except Exception as e:
                    st.error(f"Error during analysis: {str(e)}")
                    st.session_state['analysis_results'] = None
        
        results = st.session_state.get('analysis_results')
        
        if results:
            parsed_data = results["parsed_data"]
            completeness_score = results["completeness_score"]
            missing_sections = results["missing_sections"]
            ats_analysis = results["ats_analysis"]
            
            # 2. ATS Analysis & Metrics
            st.markdown("### 2. Analysis Scores")
            
            ats_score = ats_analysis.get("ats_score", 70)
            readability_score = ats_analysis.get("readability_score", 70)
            
            # Render custom styled cards
            st.markdown(f"""
                <div style="display: flex; gap: 1rem; justify-content: space-around; margin-bottom: 2rem; flex-wrap: wrap;">
                    <div style="flex: 1; min-width: 250px; text-align: center; background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%); padding: 1.5rem; border-radius: 12px; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                        <div style="font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">ATS Compatibility</div>
                        <div style="font-size: 3rem; font-weight: 700; margin-top: 0.5rem;">{ats_score}/100</div>
                    </div>
                    <div style="flex: 1; min-width: 250px; text-align: center; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 1.5rem; border-radius: 12px; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                        <div style="font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Completeness</div>
                        <div style="font-size: 3rem; font-weight: 700; margin-top: 0.5rem;">{completeness_score}/100</div>
                    </div>
                    <div style="flex: 1; min-width: 250px; text-align: center; background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); padding: 1.5rem; border-radius: 12px; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                        <div style="font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Readability</div>
                        <div style="font-size: 3rem; font-weight: 700; margin-top: 0.5rem;">{readability_score}/100</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # 3. Missing Sections
            st.markdown("### 3. Missing Sections")
            if missing_sections:
                st.warning("The following key sections were missing or not detected in your resume:")
                cols = st.columns(len(missing_sections))
                for idx, section in enumerate(missing_sections):
                    with cols[idx]:
                        st.markdown(f"""
                            <div style="background-color: #FFF5F5; border: 1px solid #FEB2B2; padding: 0.8rem; border-radius: 8px; text-align: center; color: #C53030; font-weight: 600; margin-bottom: 1rem;">
                                ⚠️ {section}
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.success("✅ Great job! Your resume contains all critical structural sections.")
            
            st.markdown("---")
            
            # Tabs for detailed layout
            tab1, tab2 = st.tabs(["📋 Extracted Information", "💡 AI Career Feedback"])
            
            with tab1:
                # Left-right layouts
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.markdown('<div class="section-header">Contact Details</div>', unsafe_allow_html=True)
                    st.write(f"**Name:** {parsed_data.get('name', 'N/A')}")
                    st.write(f"**Email:** {parsed_data.get('email', 'N/A')}")
                    st.write(f"**Phone:** {parsed_data.get('phone', 'N/A')}")
                    
                    st.markdown('<div class="section-header">Skills Extracted</div>', unsafe_allow_html=True)
                    skills = parsed_data.get("skills", [])
                    if skills:
                        badges_html = "".join([f'<span class="badge">{skill}</span>' for skill in skills])
                        st.markdown(badges_html, unsafe_allow_html=True)
                    else:
                        st.info("No skills detected.")
                        
                    st.markdown('<div class="section-header">Certifications</div>', unsafe_allow_html=True)
                    certs = parsed_data.get("certifications", [])
                    if certs:
                        for cert in certs:
                            st.markdown(f'<div class="list-bullet">🏆 {cert}</div>', unsafe_allow_html=True)
                    else:
                        st.info("No certifications detected.")
                
                with c2:
                    st.markdown('<div class="section-header">Experience</div>', unsafe_allow_html=True)
                    exp_list = parsed_data.get("experience", [])
                    if exp_list:
                        for exp in exp_list:
                            st.subheader(f"{exp.get('role')} at {exp.get('company')}")
                            st.caption(exp.get('duration', 'Duration N/A'))
                            st.write(exp.get('description', ''))
                            st.markdown("---")
                    else:
                        st.info("No work experience detected.")
                        
                    st.markdown('<div class="section-header">Projects</div>', unsafe_allow_html=True)
                    proj_list = parsed_data.get("projects", [])
                    if proj_list:
                        for proj in proj_list:
                            st.markdown(f"**{proj.get('title')}**")
                            st.write(proj.get('description', ''))
                            st.markdown("---")
                    else:
                        st.info("No projects detected.")
                        
                    st.markdown('<div class="section-header">Education</div>', unsafe_allow_html=True)
                    edu_list = parsed_data.get("education", [])
                    if edu_list:
                        for edu in edu_list:
                            st.markdown(f"🎓 **{edu.get('degree')}**")
                            st.write(f"{edu.get('institution')} ({edu.get('year')})")
                            st.markdown("---")
                    else:
                        st.info("No education details detected.")
            
            with tab2:
                st.markdown('<div class="section-header">Candidate Profile Summary</div>', unsafe_allow_html=True)
                st.write(ats_analysis.get("resume_summary", ""))
                
                col_strengths, col_weaknesses = st.columns(2)
                
                with col_strengths:
                    st.markdown('<div class="section-header" style="border-left-color: #48BB78;">Strengths</div>', unsafe_allow_html=True)
                    strengths = ats_analysis.get("strengths", [])
                    if strengths:
                        for strength in strengths:
                            st.markdown(f'<div class="list-bullet" style="border-left-color: #48BB78;">💪 {strength}</div>', unsafe_allow_html=True)
                    else:
                        st.info("No strengths generated.")
                
                with col_weaknesses:
                    st.markdown('<div class="section-header" style="border-left-color: #ED8936;">Weak Areas</div>', unsafe_allow_html=True)
                    weak_areas = ats_analysis.get("weak_areas", [])
                    if weak_areas:
                        for weakness in weak_areas:
                            st.markdown(f'<div class="list-bullet" style="border-left-color: #ED8936;">⚠️ {weakness}</div>', unsafe_allow_html=True)
                    else:
                        st.info("No weak areas identified.")
                
                st.markdown('<div class="section-header">Missing Keywords & Terms</div>', unsafe_allow_html=True)
                st.write("Consider incorporating these keywords to increase search relevance:")
                keywords = ats_analysis.get("missing_keywords", [])
                if keywords:
                    keywords_html = "".join([f'<span class="keyword-badge">{kw}</span>' for kw in keywords])
                    st.markdown(keywords_html, unsafe_allow_html=True)
                else:
                    st.info("No missing keywords identified.")
                
                st.markdown('<div class="section-header">Actionable Content Suggestions</div>', unsafe_allow_html=True)
                suggestions = ats_analysis.get("improvement_suggestions", [])
                if suggestions:
                    for sug in suggestions:
                        st.markdown(f'<div class="list-bullet">✏️ {sug}</div>', unsafe_allow_html=True)
                else:
                    st.info("No suggestions generated.")
                
                st.markdown('<div class="section-header">ATS Layout & Formatting Suggestions</div>', unsafe_allow_html=True)
                ats_suggestions = ats_analysis.get("ats_optimization_suggestions", [])
                if ats_suggestions:
                    for ats_sug in ats_suggestions:
                        st.markdown(f'<div class="list-bullet">⚙️ {ats_sug}</div>', unsafe_allow_html=True)
                else:
                    st.info("No ATS layout suggestions generated.")
