from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


class PdfGenerator:
    def generate_certificate_pdf(
        self, certificate_uuid: str, student_name: str, course_title: str, issued_at: str
    ) -> bytes:
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)

        pdf.setFont("Helvetica-Bold", 24)
        pdf.drawCentredString(300, 770, "Certificate of Completion")

        pdf.setFont("Helvetica", 14)
        pdf.drawCentredString(300, 710, "This certifies that")

        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawCentredString(300, 680, student_name)

        pdf.setFont("Helvetica", 14)
        pdf.drawCentredString(300, 650, "has successfully completed")

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawCentredString(300, 620, course_title)

        pdf.setFont("Helvetica", 12)
        pdf.drawCentredString(300, 580, f"Issued at: {issued_at}")
        pdf.drawCentredString(300, 560, f"Certificate UUID: {certificate_uuid}")

        pdf.showPage()
        pdf.save()

        buffer.seek(0)
        return buffer.read()
