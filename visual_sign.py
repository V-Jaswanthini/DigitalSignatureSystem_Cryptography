from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
from datetime import datetime
import uuid

def create_overlay(signer_name):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    signature_id = str(uuid.uuid4())[:8]
    c.setFont("Helvetica", 10)
    c.drawString(100, 100, f"Signed by: {signer_name}")
    c.drawString(100, 85, f"Date: {now}")
    c.drawString(100, 70, f"Signature ID: {signature_id}")
    c.save()
    buffer.seek(0)
    return buffer
