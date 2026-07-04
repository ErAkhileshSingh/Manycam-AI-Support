import streamlit as st
import time
import io
from PIL import Image, ImageDraw
from utils.vision import analyze_screenshot

st.title("📷 Screenshot Analyzer")
st.write("Upload an error screenshot (e.g., from ManyCam UI or Windows Device Manager) to run OCR scanning for error warnings.")

col_upload, col_results = st.columns([1, 1.2], gap="large")

# Utility function to generate mock images on the fly for testing
def generate_mock_image(theme="no_camera"):
    # Create image canvas
    img = Image.new("RGB", (640, 360), color="#1e293b")
    draw = ImageDraw.Draw(img)
    
    if theme == "no_camera":
        # Draw error box
        draw.rectangle([(80, 100), (560, 260)], fill="#0f172a", outline="#ef4444", width=3)
        draw.text((220, 140), "⚠️ WARNING", fill="#ef4444")
        draw.text((200, 180), "No active camera detected.", fill="#f8fafc")
        draw.text((150, 210), "Please check your connection and try again.", fill="#94a3b8")
    else:
        # Draw black screen
        draw.rectangle([(0, 0), (640, 360)], fill="#000000", outline="#ef4444", width=5)
        draw.text((270, 170), "⬛ Black Screen", fill="#f8fafc")
        
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    # Mock upload wrapper
    class MockUploadedFile:
        def __init__(self, name, data):
            self.name = name
            self.data = data
        def read(self):
            return self.data
        
    return MockUploadedFile(f"{theme}_error_screenshot.png", img_byte_arr)

with col_upload:
    st.subheader("Upload Screenshot")
    uploaded_image = st.file_uploader("Upload error image:", type=["png", "jpg", "jpeg"])
    
    st.write("---")
    st.write("💡 **No image handy?** Try one of our pre-configured error mockups:")
    
    col_demo1, col_demo2 = st.columns(2)
    with col_demo1:
        use_no_cam_demo = st.button("🔌 No Camera Found", use_container_width=True)
    with col_demo2:
        use_black_screen_demo = st.button("⬛ Black Screen", use_container_width=True)

with col_results:
    st.subheader("AI Vision Diagnostics")
    
    target_image_file = None
    if uploaded_image is not None:
        target_image_file = uploaded_image
    elif use_no_cam_demo:
        target_image_file = generate_mock_image("no_camera")
    elif use_black_screen_demo:
        target_image_file = generate_mock_image("black_screen")
        
    if target_image_file:
        # Display the image
        st.image(target_image_file, caption="Analyzing: " + target_image_file.name, use_container_width=True)
        
        with st.spinner("Executing OCR scan and visual analysis..."):
            time.sleep(0.9)
            vision_results = analyze_screenshot(target_image_file)
            
        if not vision_results["success"]:
            st.error(vision_results["error"])
        else:
            st.success("OCR Scanning Complete!")
            
            # Display findings
            st.markdown(f"""
            <div style="background-color: #1e293b; border-radius: 12px; padding: 1.25rem; border: 1px solid #334155;">
                <div style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; font-weight: 600;">Detected Issue Signature:</div>
                <div style="font-size: 1.35rem; font-weight: 700; color: #f59e0b; margin-top: 0.25rem;">{vision_results['detected_issue']}</div>
                <div style="margin-top: 0.5rem; font-size: 0.85rem; color: #94a3b8;">
                    Confidence: <span style="color: #10b981; font-weight: 600;">{vision_results['confidence']}</span> | 
                    Dimensions: {vision_results['dimensions']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Reasons
            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
            st.write("### 🚨 Probable Reasons:")
            for reason in vision_results["reasons"]:
                st.markdown(f"• {reason}")
                
            # Recommendations
            st.write("### 🛠️ Step-by-Step Fixes:")
            for idx, rec in enumerate(vision_results["recommendations"], 1):
                st.markdown(f"**{idx}.** {rec}")
    else:
        st.info("Upload an image file or choose one of the demo buttons to trigger image diagnostics.")
