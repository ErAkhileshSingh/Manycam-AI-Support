import streamlit as st
import time
st.title("🎫 Support Tickets")
st.write("Manage your ongoing support tickets or file a new query directly to our support engineers.")
col_list, col_create = st.columns([1.3, 0.8], gap="large")
with col_list:
    st.subheader("Your Support Tickets")
    
    if not st.session_state.tickets:
        st.info("You do not have any active support tickets.")
    else:
        for ticket in st.session_state.tickets:
            # Color coding status
            color = "#ef4444" # red for open
            if ticket["status"] == "Resolved":
                color = "#10b981" # green
            elif ticket["status"] == "Pending":
                color = "#3b82f6" # blue
                
            st.markdown(f"""
            <div style="background-color: #151c2c; border: 1px solid #273752; padding: 1.25rem; border-radius: 8px; margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-family: monospace; color: #94a3b8; font-size: 0.85rem; font-weight: 600;">{ticket["id"]}</span>
                    <span style="background-color: rgba(0,0,0,0.2); color: {color}; border: 1px solid {color}44; font-size: 0.8rem; font-weight: 700; padding: 2px 8px; border-radius: 4px;">{ticket["status"]}</span>
                </div>
                <h4 style="margin-top: 0.5rem; margin-bottom: 0.25rem; color: #f8fafc; font-size: 1.1rem; font-weight: 600;">{ticket["subject"]}</h4>
                <div style="font-size: 0.8rem; color: #64748b; display: flex; gap: 12px; margin-top: 0.5rem;">
                    <span>📅 Created: {ticket["date"]}</span>
                    <span>📂 Category: {ticket["category"]}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Interactive detail block
            with st.expander("View Message History / Engineer Response"):
                st.markdown(f"**Issue Description:**")
                st.write(f"Telemetry logs and screenshot submitted. Issue relates to '{ticket['category']}' setup.")
                st.markdown("---")
                if ticket["status"] == "Resolved":
                    st.markdown("**🧑‍💻 Engineer Response (Resolved):**")
                    st.success("Hi, we checked your camera's USB endpoint. It was a UVC descriptor conflict. Reinstalling the Windows default camera driver resolved this problem. Let us know if you need anything else!")
                elif ticket["status"] == "Open":
                    st.markdown("**🧑‍💻 System Notification:**")
                    st.info("Ticket created. A ManyCam support engineer has been assigned and will reply within 2 hours. Keep ManyCam running to allow remote diagnostics if required.")
with col_create:
    st.subheader("Open a New Ticket")
    
    with st.container(border=True):
        subject = st.text_input("Subject", placeholder="e.g. PTZ camera preset settings not saving")
        category = st.selectbox("Category", [
            "Camera Not Detected", 
            "Black Screen", 
            "PTZ Not Moving", 
            "Audio Issue", 
            "Streaming Issue", 
            "Connection Problem", 
            "License Issue"
        ])
        description = st.text_area("Provide detail description:", placeholder="Explain what steps you have already tried...", height=120)
        
        submit_btn = st.button("Submit Ticket 📩", type="primary", use_container_width=True)
        
        if submit_btn:
            if subject.strip() == "" or description.strip() == "":
                st.warning("Please fill out both Subject and Description fields.")
            else:
                with st.spinner("Submitting ticket..."):
                    time.sleep(0.8)
                    t_id = f"TCK-{time.strftime('%M%S')}"
                    new_t = {
                        "id": t_id,
                        "subject": subject,
                        "status": "Open",
                        "date": time.strftime("%Y-%m-%d"),
                        "category": category
                    }
                    st.session_state.tickets.insert(0, new_t)
                    st.success(f"Ticket {t_id} filed successfully! Our engineers will review it shortly.")
                    st.rerun()
