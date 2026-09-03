import io
import os

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from .models import EmployeeBadge

NAVY = colors.HexColor("#1e2a5e")
GOLD = colors.HexColor("#c9a227")
SLATE = colors.HexColor("#475569")

NISR_LOGO_PATH = os.path.join(os.path.dirname(__file__), "static", "certificates", "nisr-logo.png")


def download_badge_certificate(request, badge_id):
    """Generate a certificate for an earned badge, rendered as a one-page landscape PDF
    (border, seal, elegant typography) instead of a plain-text file, so it's presentable/printable."""

    employee_badge = get_object_or_404(EmployeeBadge, id=badge_id, employee=request.user)

    buffer = io.BytesIO()
    page_size = landscape(A4)
    width, height = page_size
    pdf = canvas.Canvas(buffer, pagesize=page_size)

    # Background
    pdf.setFillColor(colors.white)
    pdf.rect(0, 0, width, height, fill=1, stroke=0)

    # Double border
    margin = 24
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(3)
    pdf.rect(margin, margin, width - 2 * margin, height - 2 * margin, fill=0, stroke=1)
    pdf.setStrokeColor(GOLD)
    pdf.setLineWidth(1)
    pdf.rect(margin + 8, margin + 8, width - 2 * (margin + 8), height - 2 * (margin + 8), fill=0, stroke=1)

    # Corner flourishes
    corner = 26
    inset = margin + 8
    for cx, cy, sx, sy in [
        (inset, height - inset, 1, -1),
        (width - inset, height - inset, -1, -1),
        (inset, inset, 1, 1),
        (width - inset, inset, -1, 1),
    ]:
        pdf.setStrokeColor(GOLD)
        pdf.setLineWidth(2)
        pdf.line(cx, cy, cx + sx * corner, cy)
        pdf.line(cx, cy, cx, cy + sy * corner)

    top_text_y = height - margin - 78

    # NISR logo, centered above the title
    logo_h = 0
    if os.path.exists(NISR_LOGO_PATH):
        try:
            logo_image = ImageReader(NISR_LOGO_PATH)
            iw, ih = logo_image.getSize()
            logo_h = 56
            logo_w = logo_h * iw / ih
            pdf.drawImage(
                logo_image,
                width / 2 - logo_w / 2,
                top_text_y + 4,
                width=logo_w,
                height=logo_h,
                mask="auto",
                preserveAspectRatio=True,
            )
        except Exception:
            logo_h = 0

    if logo_h:
        top_text_y -= logo_h + 14

    # Title
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 30)
    pdf.drawCentredString(width / 2, top_text_y, "CERTIFICATE OF ACHIEVEMENT")

    pdf.setStrokeColor(GOLD)
    pdf.setLineWidth(2)
    pdf.line(width / 2 - 90, top_text_y - 14, width / 2 + 90, top_text_y - 14)

    # "This certifies that"
    pdf.setFillColor(SLATE)
    pdf.setFont("Helvetica-Oblique", 14)
    pdf.drawCentredString(width / 2, top_text_y - 52, "This certifies that")

    # Employee name
    pdf.setFillColor(NAVY)
    pdf.setFont("Times-BoldItalic", 34)
    pdf.drawCentredString(width / 2, top_text_y - 96, employee_badge.employee.full_name)
    pdf.setStrokeColor(SLATE)
    pdf.setLineWidth(0.75)
    name_width = pdf.stringWidth(employee_badge.employee.full_name, "Times-BoldItalic", 34)
    underline_half = max(name_width / 2 + 20, 120)
    pdf.line(width / 2 - underline_half, top_text_y - 105, width / 2 + underline_half, top_text_y - 105)

    # "has successfully earned the ... badge"
    pdf.setFillColor(SLATE)
    pdf.setFont("Helvetica-Oblique", 14)
    pdf.drawCentredString(width / 2, top_text_y - 134, "has successfully earned the")

    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 21)
    pdf.drawCentredString(width / 2, top_text_y - 164, f'"{employee_badge.badge.name}" Badge')

    # Awarded date
    pdf.setFillColor(SLATE)
    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(
        width / 2, top_text_y - 192, f"Awarded on {employee_badge.awarded_at.strftime('%B %d, %Y')}"
    )

    # Decorative seal/medal with the NISR slogan - fills the lower-middle space and gives the
    # certificate an "official" feel
    seal_cx = width / 2
    seal_cy = 150
    outer_r = 54
    inner_r = 46

    pdf.setFillColor(NAVY)
    tail_w = 18
    ribbon = pdf.beginPath()
    ribbon.moveTo(seal_cx - tail_w, seal_cy - 20)
    ribbon.lineTo(seal_cx - tail_w - 6, seal_cy - 70)
    ribbon.lineTo(seal_cx - 4, seal_cy - 50)
    ribbon.lineTo(seal_cx + 4, seal_cy - 50)
    ribbon.lineTo(seal_cx + tail_w + 6, seal_cy - 70)
    ribbon.lineTo(seal_cx + tail_w, seal_cy - 20)
    ribbon.close()
    pdf.drawPath(ribbon, fill=1, stroke=0)

    pdf.setFillColor(GOLD)
    pdf.circle(seal_cx, seal_cy, outer_r, fill=1, stroke=0)
    pdf.setFillColor(NAVY)
    pdf.circle(seal_cx, seal_cy, inner_r, fill=1, stroke=0)

    pdf.setFillColor(GOLD)
    pdf.setFont("Helvetica-Bold", 7)
    pdf.drawCentredString(seal_cx, seal_cy + 9, "IF YOU DON'T COUNT,")
    pdf.drawCentredString(seal_cx, seal_cy - 4, "YOU DON'T COUNT")
    pdf.setFont("Helvetica", 5.5)
    pdf.drawCentredString(seal_cx, seal_cy - 17, "\u2014 NISR")

    # Badge icon, if the badge has one and it can be read from disk - drawn small, top-right of
    # the seal, so it doesn't collide with any of the fixed text/seal positions above
    icon = employee_badge.badge.icon
    if icon:
        try:
            icon.open("rb")
            image = ImageReader(icon)
            icon_size = 42
            pdf.drawImage(
                image,
                width - margin - 8 - 20 - icon_size,
                margin + 8 + 20,
                width=icon_size,
                height=icon_size,
                mask="auto",
                preserveAspectRatio=True,
            )
        except Exception:
            pass
        finally:
            try:
                icon.close()
            except Exception:
                pass

    # Footer
    footer_y = margin + 30
    pdf.setStrokeColor(colors.HexColor("#cbd5e1"))
    pdf.setLineWidth(0.75)
    pdf.line(margin + 40, footer_y + 16, width - margin - 40, footer_y + 16)

    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawCentredString(width / 2, footer_y, "National Institute of Statistics of Rwanda")
    pdf.setFillColor(SLATE)
    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(width / 2, footer_y - 14, "Information Security Training Program")

    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    filename = f"{employee_badge.badge.name}_certificate.pdf"
    return FileResponse(buffer, as_attachment=True, filename=filename, content_type="application/pdf")