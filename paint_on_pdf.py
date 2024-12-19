from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from io import BytesIO
import os

def paint_white_area_on_pages(pdf_path, output_path, start_page=12, height=2 * 72):
    """
    Modify the specified range of pages in the PDF, painting a white area at the bottom.
    Args:
        pdf_path (str): Path to the original PDF.
        output_path (str): Path to save the modified PDF.
        start_page (int): Starting page number (1-based).
        height (float): Height of the white rectangle in points (1 inch = 72 points).
    """
    # Open the PDF file
    with open(pdf_path, "rb") as pdf_file:
        reader = PdfReader(pdf_file)
        writer = PdfWriter()
        end_page = len(reader.pages)

        for i in range(end_page):
            page = reader.pages[i]
            if start_page - 1 <= i < end_page:
                # Calculate page dimensions
                page_width = float(page.mediabox.upper_right[0]) - float(page.mediabox.lower_left[0])
                page_height = float(page.mediabox.upper_right[1]) - float(page.mediabox.lower_left[1])

                # Paint the specified area (white) at the bottom
                packet = BytesIO()
                can = canvas.Canvas(packet, pagesize=(page_width, page_height))
                can.setFillColorRGB(1, 1, 1)  # White color (change to black if needed)
                can.rect(0, 0, page_width, height, stroke=0, fill=1)
                can.save()
                packet.seek(0)

                # Create an overlay from the white rectangle
                overlay_pdf = PdfReader(packet)
                overlay_page = overlay_pdf.pages[0]
                page.merge_page(overlay_page)  # Merge with the current page

            # Add the modified or unmodified page to the writer
            writer.add_page(page)

        # Save the output PDF
        with open(output_path, "wb") as f:
            writer.write(f)

        # Remove the original PDF if the output is successfully created
        if os.path.exists(output_path):
            return True
        else:
            return False


