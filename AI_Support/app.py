import streamlit as st

# MUST be the first Streamlit command
st.set_page_config(
    page_title="Smart Camera Support Portal",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session States
if "troubleshooting_issue" not in st.session_state:
    st.session_state.troubleshooting_issue = None
if "assistant_mode" not in st.session_state:
    st.session_state.assistant_mode = "chat"  # "chat" or "questionnaire" or "report"
if "troubleshoot_step" not in st.session_state:
    st.session_state.troubleshoot_step = 1
if "troubleshoot_answers" not in st.session_state:
    st.session_state.troubleshoot_answers = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "👋 Welcome to the Smart Camera Support Portal! I can help you troubleshoot PTZ cameras, ManyCam, audio, or streaming issues. How can I help you today?"}
    ]
if "diagnose_ip" not in st.session_state:
    st.session_state.diagnose_ip = ""
if "kb_search_query" not in st.session_state:
    st.session_state.kb_search_query = ""
if "tickets" not in st.session_state:
    # Pre-populate with a couple of mock tickets
    st.session_state.tickets = [
        {"id": "TCK-8902", "subject": "PTZ Preset Position Drift", "status": "Resolved", "date": "2026-06-28", "category": "PTZ Not Moving"},
        {"id": "TCK-9411", "subject": "ManyCam audio echo on Zoom call", "status": "Open", "date": "2026-07-03", "category": "Audio Issue"}
    ]

# Inject premium custom CSS styles globally
def inject_global_css():
    st.markdown("""
    <style>
        /* Import Inter Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* Glassmorphism Main Banner Header */
        .main-header {
            background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
            padding: 2rem;
            border-radius: 16px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .main-header h1 {
            font-size: 2.2rem;
            font-weight: 700;
            margin: 0;
            padding: 0;
            color: #ffffff !important;
            letter-spacing: -0.025em;
        }
        
        .main-header p {
            font-size: 1.1rem;
            font-weight: 400;
            opacity: 0.9;
            margin-top: 0.5rem;
            margin-bottom: 0;
        }

        /* Custom Cards styling */
        .custom-card {
            background-color: #151c2c;
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid #273752;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            margin-bottom: 1.5rem;
            transition: transform 0.2s ease, border-color 0.2s ease;
        }
        
        .custom-card:hover {
            border-color: #4f46e5;
            transform: translateY(-2px);
        }

        .custom-card-title {
            font-size: 1.25rem;
            font-weight: 600;
            color: #f8fafc;
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* Chat bubbles stylings */
        .chat-bubble {
            padding: 1rem 1.25rem;
            border-radius: 12px;
            margin-bottom: 1rem;
            max-width: 85%;
            line-height: 1.5;
            font-size: 0.95rem;
        }
        
        .chat-bubble-assistant {
            background-color: #1e293b;
            color: #f8fafc;
            border-top-left-radius: 2px;
            border: 1px solid #334155;
            align-self: flex-start;
        }
        
        .chat-bubble-user {
            background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
            color: white;
            border-top-right-radius: 2px;
            align-self: flex-end;
            margin-left: auto;
            box-shadow: 0 4px 10px rgba(99, 102, 241, 0.2);
        }

        /* Diagnostic checklist styles */
        .diag-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.5rem;
            font-weight: 500;
        }
        .diag-success {
            background-color: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.2);
            color: #10b981;
        }
        .diag-fail {
            background-color: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.2);
            color: #ef4444;
        }

        /* Sidebar profile styling */
        .sidebar-brand {
            padding: 1rem 0;
            text-align: center;
            border-bottom: 1px solid #1e293b;
            margin-bottom: 1rem;
        }

        .sidebar-brand-name {
            font-size: 1.15rem;
            font-weight: 700;
            color: #f8fafc;
            letter-spacing: -0.025em;
        }

        /* Custom buttons */
        .stButton>button {
            border-radius: 8px !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
        }
        .stButton>button:hover {
            transform: scale(1.02);
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        }
    </style>
    """, unsafe_allow_html=True)

inject_global_css()

# Configure Sidebar Brand
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-name">🛠️ Smart Camera Support</div>
        <div style="font-size: 0.8rem; color: #64748b; margin-top: 2px;">v1.0.0 (Prototype)</div>
    </div>
    """, unsafe_allow_html=True)

# Define individual Page objects
# Streamlit will resolve these pages dynamically
home_page = st.Page("pages/Home.py", title="Home", icon="🏠", default=True)
ai_assistant_page = st.Page("pages/AI_Assistant.py", title="AI Assistant", icon="🤖")
kb_page = st.Page("pages/Knowledge_Base.py", title="Knowledge Base", icon="📚")
logs_page = st.Page("pages/Log_Analyzer.py", title="Upload Logs", icon="📄")
screenshot_page = st.Page("pages/Screenshot_Analyzer.py", title="Upload Screenshot", icon="📷")
diagnosis_page = st.Page("pages/Camera_Diagnosis.py", title="Camera Diagnosis", icon="🎥")
tickets_page = st.Page("pages/Tickets.py", title="My Tickets", icon="🎫")
settings_page = st.Page("pages/Settings.py", title="Settings", icon="⚙")

# Build navigation menu structure
pg = st.navigation({
    "Navigation": [home_page, ai_assistant_page, kb_page, tickets_page],
    "Tools": [diagnosis_page, logs_page, screenshot_page],
    "Configure": [settings_page]
})

# Run application router
pg.run()
