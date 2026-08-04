import streamlit as st
import cv2
import numpy as np
import quality_assessment as qa

st.set_page_config(page_title="Fingerprint Quality Gate", layout="wide")

st.title("Fingerprint Quality Assessment & Scoring Pipeline")
st.markdown("Evaluate phone camera contactless fingerprint captures before processing.")

# Sidebar Controls for Threshold Calibration
st.sidebar.header("Threshold Calibration")

blur_thresh = st.sidebar.slider("Blur Threshold (Min Laplacian Var)", 1.0, 25.0, 8.0, 0.5)
bright_min = st.sidebar.slider("Min Brightness", 0, 200, 130)
bright_max = st.sidebar.slider("Max Brightness", 150, 255, 220)
glare_thresh = st.sidebar.slider("Glare Threshold (Max Fraction)", 0.001, 0.05, 0.002, 0.001)

st.sidebar.subheader("ROI Area Coverage Band")
roi_min = st.sidebar.slider("ROI Min Fraction", 0.10, 0.90, 0.70, 0.05)
roi_max = st.sidebar.slider("ROI Max Fraction", 0.50, 1.00, 0.82, 0.05)

st.sidebar.subheader("Ridge Clarity Gabor Variance")
ridge_min = st.sidebar.slider("Min Ridge Score", 10000, 120000, 85000, 5000)
ridge_max = st.sidebar.slider("Max Ridge Score", 50000, 200000, 105000, 5000)

custom_thresholds = {
    "blur": blur_thresh,
    "bright_min": float(bright_min),
    "bright_max": float(bright_max),
    "glare": glare_thresh,
    "roi_min": roi_min,
    "roi_max": roi_max,
    "ridge_min": float(ridge_min),
    "ridge_max": float(ridge_max),
}

# Image Upload
uploaded_file = st.file_uploader("Upload a fingerprint capture", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Convert uploaded file to OpenCV format
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # Run Quality Gate Pipeline
    res = qa.quality_gate(image_bgr, thresholds=custom_thresholds)

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.image(cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB), caption="Uploaded Image", use_container_width=True)
    with col2:
        score = res["composite_score"]
        status_color = "green" if res["passed"] else "red"
        status_text = "PASS" if res["passed"] else "REJECT"

        st.markdown(
            f"<h2 style='color: {status_color};'>Overall Result: {status_text} ({score}/100)</h2>",
            unsafe_allow_html=True
        )
        st.info(f"**Guidance:** {res['guidance']}")

        st.subheader("Individual Quality Metrics")

        def badge(condition):
            return "✅ PASS" if condition else "❌ FAIL"

        # Blur
        b_pass = not res["blur"]["is_blurry"]
        st.write(f"**Blur Check:** {badge(b_pass)} — Score: `{res['blur']['blur_score']}` (Threshold: >={blur_thresh})")

        # Brightness
        br_pass = not (res["brightness"]["too_dark"] or res["brightness"]["too_bright"])
        st.write(f"**Brightness Check:** {badge(br_pass)} — Value: `{res['brightness']['brightness']}` (Range: {bright_min}–{bright_max})")

        # Glare
        g_pass = not res["glare"]["has_glare"]
        st.write(f"**Glare Check:** {badge(g_pass)} — Fraction: `{res['glare']['glare_fraction']*100:.2f}%` (Max: {glare_thresh*100:.2f}%)")

        # ROI
        r_pass = res["roi"]["roi_complete"]
        st.write(f"**ROI Coverage:** {badge(r_pass)} — Fraction: `{res['roi']['roi_fraction']*100:.1f}%` (Band: {roi_min*100:.0f}%–{roi_max*100:.0f}%)")

        # Ridge Clarity
        rg_pass = res["ridge"]["ridges_clear"]
        st.write(f"**Ridge Clarity:** {badge(rg_pass)} — Gabor Var: `{res['ridge']['ridge_score']}` (Band: {ridge_min}–{ridge_max})")