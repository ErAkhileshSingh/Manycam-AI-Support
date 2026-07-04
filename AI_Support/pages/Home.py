import streamlit as st

# Injecting the styles (global but just in case we call it to ensure alignment)
# Title banner
st.markdown("""
<div class="main-header">
    <h1>Smart Camera Support Portal</h1>
    <p>Troubleshoot motorized PTZ Cameras & ManyCam software instantly using AI</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 👋 Welcome!")
st.write("How can I help you today? Select one of our automated diagnostic pathways or start a chat with our virtual engineer.")

col1, col2 = st.columns([1.1, 0.9], gap="large")

with col1:
    # Card 1: Chat with AI
    st.markdown("""
    <div class="custom-card">
        <div class="custom-card-title">🤖 Chat with AI Assistant</div>
        <p style="font-size: 0.9rem; color: #94a3b8;">Describe your issue in natural language. Our assistant scans active user guides, manuals, and ticket history.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        chat_input = st.text_input("Type your issue...", placeholder="My camera shows a black screen in ManyCam...", key="home_chat_input")
        if st.button("Ask AI", type="primary", use_container_width=True):
            if chat_input.strip() != "":
                # Prefill chat history with user's question
                st.session_state.chat_history.append({"role": "user", "content": chat_input})
                # Simulate AI response immediately for conversational experience
                from utils.rag import search_knowledge_base
                search_results = search_knowledge_base(chat_input, limit=2)
                ai_reply = ""
                if search_results:
                    ai_reply = f"I scanned the documentation regarding '{chat_input}'. Here is what I found:\n\n"
                    for res in search_results:
                        ai_reply += f"**From {res['title']}:**\n{res['content'][:250]}...\n\n"
                    ai_reply += "\nDoes this help? Let me know if you need more details!"
                else:
                    ai_reply = f"I see you're having an issue: '{chat_input}'. Let me check on that. Could you clarify if you are using Windows or macOS, and how your camera is connected?"
                    
                st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
                st.session_state.assistant_mode = "chat"
                st.switch_page("pages/AI_Assistant.py")
            else:
                st.warning("Please type an issue first.")

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

    # Card 2: Guided Troubleshooter
    st.markdown("""
    <div class="custom-card">
        <div class="custom-card-title">🔍 Guided Troubleshooter</div>
        <p style="font-size: 0.9rem; color: #94a3b8;">Select your problem category below to run an interactive step-by-step diagnostic questionnaire.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        problem_options = [
            "Camera Not Detected",
            "Black Screen",
            "PTZ Not Moving",
            "Audio Issue",
            "Streaming Issue",
            "Connection Problem",
            "License Issue"
        ]
        selected_problem = st.radio("Choose your problem:", problem_options, index=0)
        
        if st.button("Continue", use_container_width=True):
            st.session_state.troubleshooting_issue = selected_problem
            st.session_state.assistant_mode = "questionnaire"
            st.session_state.troubleshoot_step = 1
            st.session_state.troubleshoot_answers = {}
            st.switch_page("pages/AI_Assistant.py")

with col2:
    # Card 3: Camera Diagnosis
    st.markdown("""
    <div class="custom-card">
        <div class="custom-card-title">🎥 Run Camera Diagnosis</div>
        <p style="font-size: 0.9rem; color: #94a3b8;">Quickly test if your PTZ network camera is reachable on your LAN subnet and verify key streaming ports.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        camera_ip = st.text_input("Camera IP address:", placeholder="e.g. 192.168.1.100", value=st.session_state.diagnose_ip)
        if st.button("Diagnose", use_container_width=True):
            if camera_ip.strip() != "":
                st.session_state.diagnose_ip = camera_ip
                st.switch_page("pages/Camera_Diagnosis.py")
            else:
                st.warning("Please enter an IP address.")

    # Card 4: Quick Uploads
    st.markdown("""
    <div class="custom-card">
        <div class="custom-card-title">📤 Diagnostic Uploads</div>
        <p style="font-size: 0.9rem; color: #94a3b8;">Directly submit logs or system screenshot files for quick AI summary analysis.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_u1, col_u2 = st.columns(2)
    with col_u1:
        if st.button("📷 Upload Screenshot", use_container_width=True):
            st.switch_page("pages/Screenshot_Analyzer.py")
    with col_u2:
        if st.button("📄 Upload Log File", use_container_width=True):
            st.switch_page("pages/Log_Analyzer.py")

    # Card 5: Recent FAQs
    st.markdown("""
    <div class="custom-card">
        <div class="custom-card-title">💡 Recent FAQs & Topics</div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        faqs = [
            ("Camera not detected", "Why is my camera not detected?"),
            ("PTZ preset not working", "Why is my PTZ preset not working?"),
            ("RTSP connection failed", "What should I do if the RTSP connection failed?"),
            ("Audio not coming", "Why is there no audio coming from my stream?")
        ]
        
        for display_name, search_term in faqs:
            if st.button(f"• {display_name}", key=f"faq_btn_{display_name}", use_container_width=True):
                st.session_state.kb_search_query = search_term
                st.switch_page("pages/Knowledge_Base.py")
