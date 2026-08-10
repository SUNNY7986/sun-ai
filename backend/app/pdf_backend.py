from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os


def generate_pdf_report(analysis, filename):
    os.makedirs("reports", exist_ok=True)

    pdf_path = os.path.join("reports", filename)

    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>SUN AI</b>", styles["Title"]))
    story.append(Paragraph("AI Cybersecurity Analysis Report", styles["Heading2"]))
    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(
        Paragraph(
            f"<b>Risk Level:</b> {analysis['risk_level']}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Attack Type:</b> {analysis['attack_type']}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Summary:</b><br/>{analysis['summary']}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Recommendations:</b><br/>{analysis['recommendations']}",
            styles["BodyText"]
        )
    )

    doc.build(story)

    return pdf_path