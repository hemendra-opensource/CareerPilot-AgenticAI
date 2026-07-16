import streamlit as st
from config.config import Config
from utils.groq_client import GroqClient

# Set up Streamlit Page Configuration
st.set_page_config(
    page_title="CareerPilot AI - Multi-Agent Career Mentor",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium Styling
st.markdown("""
    <style>
        /* Custom Font Imports and Colors */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        
        /* Main title styling */
        .main-title {
            background: linear-gradient(135deg, #6C63FF 0%, #3F3D56 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.8rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        
        .subtitle {
            font-size: 1.1rem;
            color: #6C757D;
            margin-bottom: 2rem;
        }
        
        /* Premium Card style */
        .status-card {
            border-radius: 12px;
            padding: 1.5rem;
            background: #FFFFFF;
            color: #495057;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            border-left: 5px solid #6C63FF;
            margin-bottom: 1.5rem;
        }
        
        .status-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: #3F3D56;
            margin-bottom: 0.5rem;
        }
        
        /* Feature Grid styling */
        .feature-box {
            background-color: #F8F9FA;
            color: #495057;
            border-radius: 8px;
            padding: 1.2rem;
            border: 1px solid #E9ECEF;
            height: 100%;
            transition: all 0.3s ease;
        }
        .feature-box:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            border-color: #6C63FF;
        }
    </style>
""", unsafe_allow_html=True)

# App Sidebar
st.sidebar.image("assets/logo.png", width=120)

st.sidebar.title("CareerPilot AI")
st.sidebar.markdown("---")
st.sidebar.subheader("System Configuration")
st.sidebar.write(f"**Default Model:** `{Config.GROQ_MODEL}`")

# Check config validity
is_config_valid, config_msg = Config.validate()
if is_config_valid:
    st.sidebar.success("✅ Config Status: Ready")
else:
    st.sidebar.error("❌ Config Status: Missing API Key")

st.sidebar.markdown("---")
st.sidebar.caption("CareerPilot AI System - Phase 1 Foundation")

# App Main Content
st.markdown('<h1 class="main-title">CareerPilot AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Multi-Agent Career Mentor System — Step into the future of professional guidance.</p>', unsafe_allow_html=True)

# System Status Dashboard
st.markdown("### 🛠️ System Overview")
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
        <div class="status-card">
            <div class="status-title">API Configuration Status</div>
            <p><strong>Environment:</strong> loaded successfully</p>
            <p><strong>Key Present:</strong> {"Yes (Hidden)" if Config.GROQ_API_KEY else "No"}</p>
            <p><strong>Validation Note:</strong> {config_msg}</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    if is_config_valid:
        st.markdown("""
            <div class="status-card" style="border-left-color: #28A745;">
                <div class="status-title">Core Multi-Agent Modules</div>
                <p>System foundation is active. Agents will be orchestrated in Phase 2.</p>
                <p><strong>Ready for deployment:</strong> Yes</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="status-card" style="border-left-color: #DC3545;">
                <div class="status-title">Action Required</div>
                <p>Please copy the <code>.env.example</code> file to <code>.env</code> in the root directory and add your <code>GROQ_API_KEY</code>.</p>
                <p>You can get a key from the Groq Console.</p>
            </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# API Verification Tool
st.markdown("### 🧪 Groq Connection Validator")
if is_config_valid:
    prompt = st.text_input("Enter a test prompt to send to Groq API:", "Explain the concept of 'Agentic AI' in one sentence.")
    
    if st.button("Test Connection", type="primary"):
        with st.spinner("Connecting to Groq API..."):
            client = GroqClient()
            success, msg = client.test_connection()
            
            if success:
                st.success(msg)
                # Run the actual response generation
                st.markdown("**Test Prompt Response:**")
                response = client.generate_response(prompt)
                st.info(response)
            else:
                st.error(msg)
else:
    st.warning("⚠️ Groq connection test is disabled. Please configure your API key in the `.env` file first.")

# System Blueprint for User Reference
st.markdown("### 🗺️ System Capabilities (Upcoming Phases)")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
        <div class="feature-box">
            <h4>📄 Resume & Skill Analysis</h4>
            <p>Parse PDF resumes using PyPDF2, extract core skills, and perform gap analysis comparing your profile against market standards.</p>
        </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown("""
        <div class="feature-box">
            <h4>🗺️ Personalized Roadmaps</h4>
            <p>Generate step-by-step career path roadmaps complete with timelines, structured learning topics, and interview preparation exercises.</p>
        </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown("""
        <div class="feature-box">
            <h4>📊 Report Engine</h4>
            <p>Generate styled, comprehensive final PDF reports using ReportLab with all recommendations and milestones ready for download.</p>
        </div>
    """, unsafe_allow_html=True)
