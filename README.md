# Fingerprint Quality Assessment & Scoring Pipeline (FP-03)

A multi-metric image quality evaluation pipeline built in Python and OpenCV. Designed for contactless phone-camera fingerprint captures to ensure biometric suitability prior to downstream minutiae extraction and matching.

## 🌟 Key Features
- **5 Quality Check Metrics:** Blur (Laplacian Variance), Brightness, Glare, ROI Coverage, and Ridge Clarity (Gabor Filters).
- **Composite Quality Score (0–100):** Weighted index categorizing captures into PASS ($\ge 60$) or REJECT ($< 60$).
- **Actionable User Guidance:** Real-time user guidance on retake actions (e.g., hold steady, adjust lighting).
- **Streamlit Web Dashboard:** Interactive UI featuring live file upload, individual pass/fail badges, and threshold calibration sliders.

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone [https://github.com/RajaRajan71/fingerprint-quality-assessment.git](https://github.com/RajaRajan71/fingerprint-quality-assessment.git)
cd fingerprint-quality-assessment
python -m venv myenv
myenv\Scripts\activate  # On Windows
pip install -r requirements.txt
