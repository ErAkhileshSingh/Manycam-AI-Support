import streamlit as st
import time
from utils.diagnosis import run_camera_diagnostics

st.title("🎥 Camera Diagnosis")
st.write("Perform a live network diagnostic ping and port scan on your motorized PTZ or IP camera.")

col_input, col_results = st.columns([1, 1.2], gap="large")

with col_input:
    st.subheader("PTZ Camera Health Check")
    
    ip_input = st.text_input("Camera IP Address", value=st.session_state.diagnose_ip, placeholder="e.g. 192.168.1.100")
    # Store IP back into session state
    st.session_state.diagnose_ip = ip_input
    
    username = st.text_input("ONVIF Username", placeholder="admin")
    password = st.text_input("ONVIF Password", type="password", placeholder="••••••••")
    
    start_diag = st.button("Start Diagnosis ⚡", type="primary", use_container_width=True)

with col_results:
    st.subheader("Diagnostic Results")
    
    if start_diag:
        if ip_input.strip() == "":
            st.warning("Please enter a Camera IP address first.")
        else:
            with st.spinner("Executing network checks..."):
                # Simulate loading steps
                time.sleep(0.8)
                diag_result = run_camera_diagnostics(ip_input, username, password)
                
            if not diag_result.get("success", True):
                st.error(diag_result.get("error", "Failed to run diagnostics."))
            else:
                # 1. Reachable check
                r_status = "diag-success" if diag_result["reachable"] else "diag-fail"
                r_icon = "✔" if diag_result["reachable"] else "✖"
                st.markdown(f"""
                <div class="diag-item {r_status}">
                    <span>{r_icon}</span>
                    <span>Camera Reachable ({ip_input})</span>
                </div>
                """, unsafe_allow_html=True)
                
                # 2. ONVIF check
                o_status = "diag-success" if diag_result["onvif_active"] else "diag-fail"
                o_icon = "✔" if diag_result["onvif_active"] else "✖"
                st.markdown(f"""
                <div class="diag-item {o_status}">
                    <span>{o_icon}</span>
                    <span>ONVIF Available (Port 80/8080)</span>
                </div>
                """, unsafe_allow_html=True)
                
                # 3. RTSP check
                rt_status = "diag-success" if diag_result["rtsp_active"] else "diag-fail"
                rt_icon = "✔" if diag_result["rtsp_active"] else "✖"
                st.markdown(f"""
                <div class="diag-item {rt_status}">
                    <span>{rt_icon}</span>
                    <span>RTSP Video Stream Active (Port 554)</span>
                </div>
                """, unsafe_allow_html=True)
                
                # 4. Firmware check (outdated means warning/fail)
                fw_status = "diag-fail" if diag_result["firmware_outdated"] else "diag-success"
                fw_icon = "✖" if diag_result["firmware_outdated"] else "✔"
                fw_label = "Firmware Outdated" if diag_result["firmware_outdated"] else "Firmware Up to Date"
                st.markdown(f"""
                <div class="diag-item {fw_status}">
                    <span>{fw_icon}</span>
                    <span>{fw_label}</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Recommendations block
                st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
                st.markdown("""
                <div style="background-color: #151c2c; border: 1px solid #273752; padding: 1.25rem; border-radius: 8px;">
                    <div style="font-weight: 600; color: #f8fafc; margin-bottom: 0.5rem;">AI Recommendation:</div>
                """, unsafe_allow_html=True)
                
                st.write(diag_result["recommendation"])
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Enter camera IP settings and click 'Start Diagnosis' to fetch status telemetry.")
