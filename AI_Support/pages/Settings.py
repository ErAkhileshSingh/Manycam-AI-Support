import streamlit as st

st.title("⚙ Settings")
st.write("Configure connection keys, customize LLM models, edit system instructions, and customize the support portal's behavior.")

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.subheader("Model Configuration")
    
    provider = st.selectbox("LLM Provider", [
        "OpenAI (GPT-4o / GPT-4-mini)", 
        "Google Gemini (Pro / Flash)", 
        "Anthropic Claude 3.5 Sonnet", 
        "Local LLM (Ollama / Llama 3)"
    ])
    
    api_key = st.text_input("API Access Key", type="password", placeholder="sk-proj-••••••••••••••••••••")
    
    selected_model = st.selectbox("Active Model Name", [
        "gpt-4o",
        "gpt-4o-mini",
        "gemini-1.5-pro",
        "gemini-1.5-flash",
        "claude-3-5-sonnet",
        "llama3:8b-instruct-q4"
    ])
    
    temperature = st.slider("Temperature (Creativity)", min_value=0.0, max_value=1.0, value=0.2, step=0.1)

with col_right:
    st.subheader("System Instructions Prompt")
    
    default_prompt = (
        "You are an expert AI Camera Support Engineer for PTZ Cameras and ManyCam streaming software.\n"
        "Your task is to review user problems, query the document indexes, perform step-by-step troubleshooting, "
        "and provide highly technical, actionable recommendations.\n"
        "Never make up commands; if you do not know, suggest opening a support ticket."
    )
    
    st.text_area("System Prompt", value=default_prompt, height=150)
    
    st.subheader("RAG Options")
    st.checkbox("Enable Retrieval-Augmented Generation (RAG)", value=True)
    st.checkbox("Enable Vision OCR scanning for uploaded screenshots", value=True)
    st.checkbox("Pre-parse log uploads for connection parameters", value=True)

# Save confirmation
if st.button("Save Settings 💾", type="primary", use_container_width=True):
    st.success("Configuration settings updated successfully!")
