# 📸 Contactless Fingerprint Quality Assessment & Scoring Pipeline (FP-03)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://fingerprint-quality-assessment-n8veaekppwahfwkvbcmxwe.streamlit.app/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)](https://opencv.org/)

A real-time, multi-metric image quality evaluation pipeline built in Python and OpenCV. Designed specifically for contactless phone-camera fingerprint captures to ensure biometric usability prior to downstream minutiae extraction and matching.

---

## 🌐 Live Interactive Demo

🔗 **Try the Web Dashboard:** [Fingerprint Quality Gate App](https://fingerprint-quality-assessment-n8veaekppwahfwkvbcmxwe.streamlit.app/)

---

## 📌 Problem & Objective

Traditional fingerprint quality algorithms (such as NIST's NFIQ2) were specifically designed for 500 DPI contact scanners. When applied to smartphone camera captures, they frequently fail due to variable lighting, glare, distance, perspective distortion, and background noise.

This project implements an early-stage **Quality Control (QC) Gate** that inspects contactless smartphone captures in under 300ms, immediately alerting users to retake poor captures before pushing unviable images to compute-heavy biometric models.

---

## 🛠️ Key Features

* **5 Individual Quality Check Metrics:**
  * 🌀 **Blur Detection:** Uses Laplacian Variance to calculate image edge sharpness.
  * 💡 **Brightness Check:** Computes mean pixel luminance to flag under/overexposed frames.
  * ☀️ **Glare Detection:** Identifies highlight clipping caused by harsh direct light or torch sources.
  * 📐 **ROI Completeness:** Estimates finger surface area coverage relative to the full frame.
  * 🔍 **Ridge Clarity:** Applies Gabor filters (ridge-selective filtering) to assess ridge-valley distinction.
* **Composite Scoring System (0–100):** Combines normalized metric scores using weighted parameters into a unified decision index.
  * **Score $\ge 60$**: `PASS` (Ready for biometric pipeline)
  * **Score $< 60$**: `REJECT` (Triggers targeted user retake feedback)
* **Streamlit Interactive UI:** Features real-time parameter tuning via sidebar sliders, instant pass/fail badges, dynamic metric breakdowns, and actionable retake recommendations.

---

## ⚡ Performance Budget

Each stage is optimized for low-latency client-side or edge processing:

| Metric Stage | Method | Target Latency |
| :--- | :--- | :--- |
| **Blur Check** | Laplacian Variance | $< 10\text{ ms}$ |
| **Brightness Check** | Mean Pixel Luminance | $< 5\text{ ms}$ |
| **Glare Check** | High-Value Pixel Ratio | $< 10\text{ ms}$ |
| **ROI Coverage** | Threshold Masking | $< 100\text{ ms}$ |
| **Ridge Clarity** | Gabor Filter Response | $< 150\text{ ms}$ |
| **Total Pipeline** | **Combined QC Gate** | **$< 300\text{ ms}$** |

---

## 📂 Repository Structure

├── quality_assessment.py  # Core metric functions & quality_gate() pipeline
├── quality_app.py         # Interactive Streamlit Web Interface
├── test_quality.py        # Pipeline validation script evaluating 20 test cases
├── make_report.py         # Automated PDF report generator using ReportLab
├── report.pdf             # Technical QC report covering calibration & edge cases
├── requirements.txt       # Deployment dependency configuration
└── README.md              # Project documentation

---

## 🚀 Local Installation & Execution

### 1. Clone & Environment Setup
```bash
# Clone repository
git clone [https://github.com/RajaRajan71/fingerprint-quality-assessment.git](https://github.com/RajaRajan71/fingerprint-quality-assessment.git)
cd fingerprint-quality-assessment

# Create and activate virtual environment
python -m venv myenv

# On Windows:
myenv\Scripts\activate

# On macOS/Linux:
source myenv/bin/activate

# Install dependencies
pip install -r requirements.txt




