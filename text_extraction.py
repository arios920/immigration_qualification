import pdfplumber  # pdfplumber for PDF reading
from PIL import Image  # image handling
import pytesseract  # pytesseract for Optical Character Recognition (OCR)
import io  # io for handling byte streams

def extract_text(file_content):
    """
    Extract text from the given file content.
    Tries to open as PDF first; if it fails, assumes it's an image and uses OCR.
    """
    try:
        # Try to open as a PDF using pdfplumber
        text = ""
        with pdfplumber.open(io.BytesIO(file_content)) as pdf:
            for page in pdf.pages:
                text += page.extract_text()  # Extract text from each page
        return text
    except Exception:
        # If opening as PDF fails, assume it's an image
        image = Image.open(io.BytesIO(file_content))
        text = pytesseract.image_to_string(image)  # Perform OCR on the image
        return text
