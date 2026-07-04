import streamlit as st
from utils.rag import search_knowledge_base, load_documents
st.title("📚 Knowledge Base")
st.write("Search user manuals, setup guides, and troubleshooting procedures for PTZ Cameras and ManyCam.")
# Fetch pre-filled search query from FAQ redirect if exists
search_query = st.text_input(
    "Search Documentation:", 
    value=st.session_state.kb_search_query, 
    placeholder="e.g. RTSP setup, black screen, presets..."
)
# Clear FAQ search state after using it once
st.session_state.kb_search_query = ""
col_search, col_result = st.columns([1, 1.5], gap="large")
with col_search:
    st.subheader("Articles")
    
    # Run search or load default document list
    if search_query.strip() != "":
        results = search_knowledge_base(search_query)
        st.caption(f"Found {len(results)} matches for '{search_query}':")
    else:
        results = load_documents()
        st.caption("Browse all available documentation sections:")
    if not results:
        st.info("No matching articles found. Try using keywords like 'PTZ', 'RTSP', 'driver', or 'black'.")
    else:
        # Create interactive list of articles
        selected_article = None
        for idx, doc in enumerate(results):
            # Format title nicely
            disp_title = doc['title']
            if st.button(f"📄 {disp_title}", key=f"doc_{idx}", use_container_width=True):
                st.session_state.selected_doc_index = idx
                st.session_state.selected_doc_list = results
                
        # Default selection to first result if not chosen
        if "selected_doc_index" not in st.session_state or st.session_state.selected_doc_index >= len(results):
            st.session_state.selected_doc_index = 0
            st.session_state.selected_doc_list = results
with col_result:
    st.subheader("Reading Pane")
    
    # Render selected article
    if results and "selected_doc_index" in st.session_state:
        idx = st.session_state.selected_doc_index
        # Safeguard if list changes
        active_list = getattr(st.session_state, 'selected_doc_list', results)
        if idx < len(active_list):
            doc = active_list[idx]
            
            st.markdown(f"""
            <div style="background-color: #1e293b; border-radius: 12px; padding: 1.5rem; border: 1px solid #334155; margin-bottom: 1rem;">
                <div style="font-size: 0.8rem; color: #6366f1; font-weight: 600; text-transform: uppercase;">Doc Location: data/{doc['source']}</div>
                <h2 style="margin-top: 0.5rem; margin-bottom: 0.5rem; font-size: 1.5rem; font-weight: 700; color: #f8fafc;">{doc['title']}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(doc['content'])
        else:
            st.info("Select an article on the left to read the documentation.")
    else:
        st.info("Select an article on the left to read the documentation.")