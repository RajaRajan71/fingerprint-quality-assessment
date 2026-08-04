from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf(filename="report.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=10
    )
    
    q_style = ParagraphStyle(
        'QuestionStyle',
        parent=styles['Heading2'],
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=10,
        spaceAfter=4
    )
    
    a_style = ParagraphStyle(
        'AnswerStyle',
        parent=styles['BodyText'],
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=8
    )

    story = []
    
    # Title
    story.append(Paragraph("Assignment 4: Fingerprint Quality Assessment Report", title_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=12))
    
    # Q1
    story.append(Paragraph("Q1. What threshold did you set for blur? How did you decide?", q_style))
    q1_ans = ("<b>Answer:</b> The Laplacian variance blur threshold was set to <b>8.0</b> based on empirical "
              "calibration across the dataset. Clear images consistently produced scores between <b>8.29</b> and <b>11.26</b>, "
              "while motion-blurred images consistently dropped below <b>8.0</b> (reaching as low as <b>2.78</b>).")
    story.append(Paragraph(q1_ans, a_style))
    
    # Q2
    story.append(Paragraph("Q2. Which metric was hardest to implement correctly? What went wrong first?", q_style))
    q2_ans = ("<b>Answer:</b> <b>Glare Detection</b> and <b>Ridge Clarity</b> within the region of interest were the most challenging. "
              "Initially, running glare calculations across the whole unmasked frame evaluated normal background highlights as overexposed pixels, "
              "leading to false rejections. Restricting calculations exclusively inside the segmented <b>Finger ROI Mask</b> resolved the issue.")
    story.append(Paragraph(q2_ans, a_style))
    
    # Q3
    story.append(Paragraph("Q3. What is NFIQ2? Why is a score designed for contact scanners not reliable for phone camera images?", q_style))
    q3_ans = ("<b>Answer:</b> <b>NFIQ2</b> (NIST Fingerprint Image Quality 2) is a standard quality scoring tool trained on 500 DPI contact optical/capacitive scanner images. "
              "It is unreliable for contactless phone camera images because phone captures introduce variable distance, focal blur, non-uniform ambient lighting, "
              "and perspective tilt, causing NFIQ2 to penalize otherwise usable contactless captures.")
    story.append(Paragraph(q3_ans, a_style))
    
    # Q4
    story.append(Paragraph("Q4. Name 3 other quality problems you'd add checks for in a real deployment.", q_style))
    q4_ans = ("<b>Answer:</b><br/>"
              "1. <b>Distance & Scale Check:</b> Verifying finger pixel width to ensure the finger is placed at a valid distance.<br/>"
              "2. <b>Perspective & Pitch Angle:</b> Detecting out-of-plane rotation to keep the finger pad parallel to the camera.<br/>"
              "3. <b>Lens Contamination Detection:</b> Identifying smudges, moisture, or grease obscuring ridge detail.")
    story.append(Paragraph(q4_ans, a_style))
    
    # Q5
    story.append(Paragraph("Q5. If a rural agricultural worker's fingerprints are naturally worn, what should the system do differently?", q_style))
    q5_ans = ("<b>Answer:</b><br/>"
              "1. <b>Adaptive Thresholds:</b> Dynamically relax ridge clarity thresholds after failed attempts while applying targeted contrast enhancement (CLAHE).<br/>"
              "2. <b>Multi-Frame Burst Stacking:</b> Capture a rapid sequence of frames to average noise and amplify faint ridge structures.<br/>"
              "3. <b>Alternative Modality Fallback:</b> Automatically offer fallback verification via secondary fingers or facial recognition to prevent biometric exclusion.")
    story.append(Paragraph(q5_ans, a_style))
    
    doc.build(story)
    print("report.pdf generated successfully!")

if __name__ == "__main__":
    generate_pdf()