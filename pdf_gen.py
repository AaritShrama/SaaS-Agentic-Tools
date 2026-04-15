from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

def generate_pdf(data: dict) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph(data["name"], styles["Title"]))
    elements.append(Paragraph(f"Date: {data['date']}", styles["Normal"]))
    elements.append(Spacer(1, 20))

    # Table
    table_data = [["Item", "Amount"]]  # header row
    for item in data["items"]:
        table_data.append([item["name"], str(item["amount"])])

    table = Table(table_data, colWidths=[350, 150])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID",       (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING",    (0, 0), (-1, -1), 8, 8),
    ]))
    elements.append(table)

    doc.build(elements)
    return buffer.getvalue()