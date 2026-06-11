from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

def create_proposal_pdf(proposal_text, project_name):
    pdf_folder = "static/generated_pdfs"

    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)

    file_name = f"{project_name.replace(' ', '_')}.pdf"

    pdf_path = os.path.join(pdf_folder, file_name)

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    content = []

    title = Paragraph(
        "Software Project Proposal",
        styles['Title']
    )

    content.append(title)
    content.append(Spacer(1, 20))

    proposal = Paragraph(
        proposal_text.replace("\n", "<br/>"),
        styles['BodyText']
    )

    content.append(proposal)

    doc.build(content)

    return file_name
