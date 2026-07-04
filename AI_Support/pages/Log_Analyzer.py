import streamlit as st
import time
from utils.parser import parse_log_file

st.title("📄 Log Analyzer")
st.write("Upload a ManyCam log file (manycam.log) or generic device logs to scan for driver conflicts, connection drops, and setup warnings.")

# Setup demo log example button to make testing easy
demo_log_content = """2026-07-04 12:05:01 [INFO] ManyCam application started. Version 8.2.0.
2026-07-04 12:05:02 [INFO] Loading audio drivers...
2026-07-04 12:05:03 [WARNING] Audio sample rate mismatched for Microphone device. Expected 48000Hz, got 44100Hz.
2026-07-04 12:05:05 [INFO] Initializing video capture engines...
2026-07-04 12:05:06 [ERROR] UVC USB connection failed to handshake with Device ID 04b4:8921.
2026-07-04 12:05:07 [ERROR] Camera driver UVCVideoDriver returned error code 102. Device resource is occupied by another process.
2026-07-04 12:05:10 [INFO] Streaming interface initialized.
2026-07-04 12:05:15 [ERROR] RTMP network socket timeout. Unable to connect to rtmp://live.youtube.com/live2.
"""

col_u, col_r = st.columns([1, 1.2], gap="large")

with col_u:
    st.subheader("Upload Log File")
    uploaded_file = st.file_uploader("Upload manycam.log:", type=["log", "txt"])
    
    # Option to use demo file if user doesn't have one
    use_demo = st.button("Use Mock Log Example (Demo)", use_container_width=True)
    
with col_r:
    st.subheader("Analysis Results")
    
    log_content = None
    if uploaded_file is not None:
        try:
            log_content = uploaded_file.read().decode("utf-8")
        except Exception as e:
            st.error(f"Error reading file: {e}")
    elif use_demo:
        log_content = demo_log_content
        
    if log_content:
        with st.spinner("Parsing logs..."):
            time.sleep(0.7)
            results = parse_log_file(log_content)
            
        # Summary metrics
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("Errors Found", f"🚨 {results['error_count']}")
        with col_m2:
            st.metric("Warnings Found", f"⚠️ {results['warning_count']}")
            
        # Display findings
        st.write("### 🔍 Key Findings:")
        for idx, finding in enumerate(results["findings"], 1):
            st.markdown(f"**{idx}. {finding}**")
            
        # Display recommendations
        st.write("### 💡 Recommended Actions:")
        for rec in results["recommendations"]:
            st.info(rec)
            
        # Display raw error lines in expander
        if results["errors"]:
            with st.expander("Show detailed error lines"):
                for line_num, error_line in results["errors"]:
                    st.code(f"Line {line_num}: {error_line}", language="log")
    else:
        st.info("Upload a log file or click 'Use Mock Log Example' to see the analyzer in action.")
