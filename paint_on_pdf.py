from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas
from io import BytesIO
import os

def paint_white_area_on_pages(pdf_path, output_path, start_page=12,  height=2 * 72):
    """
    Modify the specified range of pages in the PDF, painting a white area at the bottom.
    Args:
        pdf_path (str): Path to the original PDF.
        output_path (str): Path to save the modified PDF.
        start_page (int): Starting page number (1-based).
        end_page (int): Ending page number (1-based).
        height (float): Height of the white rectangle in points (1 inch = 72 points).
    """
    # Read the PDF
    reader = PdfFileReader(open(pdf_path, "rb"))
    writer = PdfFileWriter()
    end_page = reader.getNumPages()

    for i in range(reader.numPages):
        page = reader.getPage(i)
        if start_page - 1 <= i <= end_page - 1:
            # Calculate page dimensions
            page_width = float(page.mediaBox.getUpperRight_x()) - float(page.mediaBox.getLowerLeft_x())
            page_height = float(page.mediaBox.getUpperRight_y()) - float(page.mediaBox.getLowerLeft_y())

            # Paint the specified area white
            packet = BytesIO()
            can = canvas.Canvas(packet, pagesize=(page_width, page_height))
            can.setFillColorRGB(0, 0, 0)  # Black color (updated as per earlier discussion)
            can.rect(0, 0, page_width, height, stroke=0, fill=1)
            can.save()
            packet.seek(0)

            # Overlay the new content
            overlay_pdf = PdfFileReader(packet)
            overlay_page = overlay_pdf.getPage(0)
            page.mergePage(overlay_page)

        # Add the modified or unmodified page to the writer
        writer.addPage(page)

    # Save the output PDF
    with open(output_path, "wb") as f:
        writer.write(f)
    if os.path.exists(output_path):
        os.remove(pdf_path)
        return True
    else:
        return False



# paint_white_area_on_pages(pdf_path, output_path, start_page=12, end_page=20)
