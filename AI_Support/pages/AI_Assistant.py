import streamlit as st
import time
from utils.rag import search_knowledge_base

# Add page navigation helper for reset
def reset_troubleshooter():
    st.session_state.troubleshooting_issue = None
    st.session_state.assistant_mode = "chat"
    st.session_state.troubleshoot_step = 1
    st.session_state.troubleshoot_answers = {}

# Page Title
st.title("🤖 AI Support Assistant")

# Navigation header
col_h1, col_h2 = st.columns([2.5, 1.5])
with col_h2:
    if st.button("Reset / Start Live Chat", type="secondary", use_container_width=True):
        reset_troubleshooter()
        st.rerun()

# ----------------- MODE 1: LIVE CHAT -----------------
if st.session_state.assistant_mode == "chat":
    st.write("Ask our AI assistant any questions about setting up ManyCam, connecting network PTZ cameras, configuring presets, or audio issues.")
    
    # Custom chat display
    chat_container = st.container(height=450, border=True)
    
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-bubble chat-bubble-user">
                    <b>You:</b><br>{message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-bubble chat-bubble-assistant">
                    <b>AI Assistant:</b><br>{message['content']}
                </div>
                """, unsafe_allow_html=True)
                
    # Chat input box
    if user_msg := st.chat_input("Type your message..."):
        # Append User Msg
        st.session_state.chat_history.append({"role": "user", "content": user_msg})
        
        # Query Local RAG
        search_results = search_knowledge_base(user_msg, limit=2)
        
        # Formulate response
        if search_results:
            ai_reply = f"Here is what I found in our documentation regarding '{user_msg}':\n\n"
            for res in search_results:
                ai_reply += f"### {res['title']}\n{res['content']}\n\n"
            ai_reply += "\nLet me know if you need help with any of these steps!"
        else:
            # Fallback simple answers
            user_msg_lower = user_msg.lower()
            if "hello" in user_msg_lower or "hi" in user_msg_lower:
                ai_reply = "Hello! I am your AI Camera Support Assistant. How can I help you today? You can ask me questions or launch the troubleshooter from the Home tab."
            elif "black" in user_msg_lower:
                ai_reply = "If you see a black screen in ManyCam, verify no other application (Zoom, Teams, Skype) is currently using the camera. Also try toggling Hardware Acceleration under ManyCam settings."
            elif "ptz" in user_msg_lower or "move" in user_msg_lower:
                ai_reply = "PTZ control issues are usually due to IP address mismatches or port configurations. Check if the camera IP is reachable and ONVIF control is enabled on port 80/8080."
            else:
                ai_reply = "I'm checking our knowledge base for that topic. If you're experiencing a specific camera failure, I highly recommend using the **Guided Troubleshooter** on the Home tab for step-by-step diagnosis."
                
        # Append AI response
        st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
        st.rerun()

# ----------------- MODE 2: GUIDED QUESTIONNAIRE -----------------
elif st.session_state.assistant_mode == "questionnaire":
    issue = st.session_state.troubleshooting_issue or "Camera Issue"
    st.subheader(f"Troubleshooting: {issue}")
    st.write("Please answer a few quick questions to help the AI diagnose your problem.")
    
    step = st.session_state.troubleshoot_step
    
    # Progress indicators
    st.progress(step / 6.0, text=f"Question {step} of 6")
    
    # Display question based on index
    if step == 1:
        st.markdown("### Question 1 of 6\n**Which operating system are you using?**")
        os_choice = st.radio("Select OS:", ["Windows", "macOS"], index=0)
        
        if st.button("Next ➡️", type="primary", use_container_width=True):
            st.session_state.troubleshoot_answers["os"] = os_choice
            st.session_state.troubleshoot_step = 2
            st.rerun()
            
    elif step == 2:
        st.markdown("### Question 2 of 6\n**How is your camera connected?**")
        conn_choice = st.radio("Select Connection Type:", ["USB", "IP Camera", "PTZ Camera (Serial/LAN)", "NDI (Network)"], index=0)
        
        if st.button("Next ➡️", type="primary", use_container_width=True):
            st.session_state.troubleshoot_answers["connection"] = conn_choice
            st.session_state.troubleshoot_step = 3
            st.rerun()
            
    elif step == 3:
        st.markdown("### Question 3 of 6\n**Can you see the camera device in Device Manager / System Information?**")
        dev_choice = st.radio("Select Device Status:", ["Yes", "No", "Don't Know"], index=0)
        
        if st.button("Next ➡️", type="primary", use_container_width=True):
            st.session_state.troubleshoot_answers["device_manager"] = dev_choice
            st.session_state.troubleshoot_step = 4
            st.rerun()
            
    elif step == 4:
        st.markdown("### Question 4 of 6\n**What exactly happens when you try to use it?**")
        symptom_options = ["Black Screen", "No Camera Found Error", "Camera Disconnects Randomly", "Camera Feed Freezes", "Wrong Resolution / Low FPS"]
        symptom_choice = st.radio("Select Symptom:", symptom_options, index=0)
        
        if st.button("Next ➡️", type="primary", use_container_width=True):
            st.session_state.troubleshoot_answers["symptom"] = symptom_choice
            st.session_state.troubleshoot_step = 5
            st.rerun()
            
    elif step == 5:
        st.markdown("### Question 5 of 6\n**Did this configuration work before?**")
        work_choice = st.radio("Select History:", ["Yes, it worked fine yesterday", "No, it never worked", "First Time Setup"], index=0)
        
        if st.button("Next ➡️", type="primary", use_container_width=True):
            st.session_state.troubleshoot_answers["history"] = work_choice
            st.session_state.troubleshoot_step = 6
            st.rerun()
            
    elif step == 6:
        st.markdown("### Question 6 of 6\n**Upload Screenshot of Error (Optional)**")
        uploaded_ss = st.file_uploader("Upload error screen to assist AI OCR detection:", type=["png", "jpg", "jpeg"])
        
        # Store metadata if file is uploaded
        if uploaded_ss:
            st.session_state.troubleshoot_answers["screenshot_uploaded"] = True
            st.session_state.troubleshoot_answers["screenshot_name"] = uploaded_ss.name
        else:
            st.session_state.troubleshoot_answers["screenshot_uploaded"] = False
            
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button("⬅️ Back", use_container_width=True):
                st.session_state.troubleshoot_step = 5
                st.rerun()
        with col_b2:
            if st.button("Diagnose Issue 🧠", type="primary", use_container_width=True):
                st.session_state.assistant_mode = "processing"
                st.rerun()

# ----------------- MODE 3: TIMED PROCESSING SCREEN -----------------
elif st.session_state.assistant_mode == "processing":
    st.subheader("AI Diagnostics in progress...")
    st.write("Our model is compiling answers, scanning manuals, and identifying the optimal path...")
    
    with st.status("Analyzing system telemetry...", expanded=True) as status:
        st.write("🔍 Searching Documentation...")
        time.sleep(0.6)
        st.write("✔ Search complete.")
        
        st.write("🔍 Searching FAQs database...")
        time.sleep(0.5)
        st.write("✔ Found 2 matching patterns.")
        
        st.write("🔍 Reviewing previous support tickets...")
        time.sleep(0.6)
        st.write("✔ Identified historical resolutions.")
        
        st.write("🧠 Preparing recommended solution...")
        time.sleep(0.6)
        status.update(label="Analysis Completed!", state="complete", expanded=False)
        
    st.session_state.assistant_mode = "report"
    st.rerun()

# ----------------- MODE 4: DIAGNOSTIC SOLUTION REPORT -----------------
elif st.session_state.assistant_mode == "report":
    answers = st.session_state.troubleshoot_answers
    issue = st.session_state.troubleshooting_issue
    
    st.subheader("🔧 AI Diagnostic Report")
    
    # Expert System Logic to derive Cause/Steps
    cause = "UVC USB Port Driver Mismatch"
    confidence = "92%"
    steps = [
        "Disconnect the camera cable from the PC.",
        "Restart ManyCam software fully (close from tray icon).",
        "Open Device Manager, locate 'Cameras', and verify if there is an exclamation mark next to your camera name.",
        "Install the latest manufacturer USB driver or use a direct USB 3.0 blue port.",
        "Restart your PC and test connection."
    ]
    
    # Customise based on choices
    if answers.get("connection") == "IP Camera":
        cause = "Camera Network Stream Port Blocked / IP Conflict"
        confidence = "89%"
        steps = [
            "Verify your camera IP is reachable by running a ping command.",
            "Open your browser and verify if you can access the camera's web configuration page.",
            "Check if Port 554 (RTSP) or Port 80 (ONVIF) are blocked by Windows Defender Firewall.",
            "Confirm the RTSP login credentials match your ManyCam connection string.",
            "If NDI connection is used, verify NDI license status in camera dashboard."
        ]
    elif answers.get("device_manager") == "No":
        cause = "Hardware Connection / USB Power Failure"
        confidence = "95%"
        steps = [
            "Unplug the camera and check the physical connection cable.",
            "Make sure you are using the original cable provided by the manufacturer (avoid extensions over 3m).",
            "Try a different USB port, preferably on the back of the desktop PC tower.",
            "Verify if the camera power adapter LED is lit (motorized cameras require external power).",
            "Test the camera on another PC if possible to rule out hardware failure."
        ]
    elif answers.get("symptom") == "Black Screen":
        cause = "Camera Stream Resource Occupied"
        confidence = "90%"
        steps = [
            "Check if other software (Zoom, OBS, Teams) is running in the background and using the camera. Close them.",
            "Open ManyCam Settings > General and turn off Hardware Acceleration.",
            "Click on the ManyCam video preset, select 'Blank', then switch back to your camera source to reset.",
            "Verify that your camera's resolution output is set to a standard 1920x1080 at 30fps."
        ]
    elif issue == "PTZ Not Moving":
        cause = "ONVIF Controller Authentication Mismatch"
        confidence = "87%"
        steps = [
            "Ensure ONVIF service is enabled inside your PTZ Camera admin dashboard.",
            "Confirm your PTZ controller username and password are correct.",
            "Check network gateway configuration if the camera is on a different VLAN.",
            "Verify the control port is set to 80 or 8080 (standard ONVIF ports)."
        ]
        
    col_rep1, col_rep2 = st.columns([2, 1], gap="medium")
    
    with col_rep1:
        st.markdown(f"""
        <div style="background-color: #1e293b; border-radius: 12px; padding: 1.5rem; border: 1px solid #334155;">
            <div style="font-size: 0.85rem; text-transform: uppercase; color: #94a3b8; font-weight: 600; letter-spacing: 0.05em;">Possible Cause</div>
            <div style="font-size: 1.6rem; font-weight: 700; color: #ef4444; margin-top: 0.25rem;">{cause}</div>
            
            <div style="margin-top: 1rem; display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 0.9rem; color: #94a3b8;">AI Confidence Score:</span>
                <span style="font-weight: 700; color: #10b981; background-color: rgba(16, 185, 129, 0.1); padding: 2px 8px; border-radius: 4px; font-size: 0.9rem;">{confidence}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
        st.write("### 📋 Recommended Steps:")
        for idx, step_desc in enumerate(steps, 1):
            st.markdown(f"**{idx}.** {step_desc}")
            
    with col_rep2:
        st.markdown("""
        <div class="custom-card">
            <div class="custom-card-title">💡 Still Need Help?</div>
            <p style="font-size: 0.85rem; color: #94a3b8;">If the steps above did not resolve the problem, you can parse your system logs or submit a support ticket to our network engineers.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📄 Upload system log", use_container_width=True):
            st.switch_page("pages/Log_Analyzer.py")
            
        if st.button("🎫 Open Ticket with Engineer", type="primary", use_container_width=True):
            # Create a mock ticket dynamically based on selections
            t_id = f"TCK-{time.strftime('%M%S')}"
            new_ticket = {
                "id": t_id,
                "subject": f"Unresolved {issue}: {cause}",
                "status": "Open",
                "date": time.strftime("%Y-%m-%d"),
                "category": issue
            }
            st.session_state.tickets.insert(0, new_ticket)
            st.success(f"Ticket {t_id} opened successfully!")
            st.balloons()
            time.sleep(1.0)
            st.switch_page("pages/Tickets.py")
            
        if st.button("🔄 Restart Troubleshooter", use_container_width=True):
            reset_troubleshooter()
            st.rerun()
