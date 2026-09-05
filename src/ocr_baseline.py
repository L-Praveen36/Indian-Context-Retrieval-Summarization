import os
import pytesseract
from PIL import Image
import pymupdf as fitz # PyMuPDF

# Note for Windows users: 
# You may need to set the tesseract path if it's not in your system PATH.
# Uncomment and update the line below if necessary:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def run_tesseract_ocr(file_path: str) -> str:
    """
    Runs Tesseract OCR on an image or scanned PDF.
    Extracts both English and Devanagari (Hindi/Sanskrit).
    """
    ext = os.path.splitext(file_path)[1].lower()
    
    # We pass 'hin+eng' to support both scripts/languages
    # Note: 'hin' (Hindi) language pack in Tesseract covers Devanagari script well
    # Make sure you have the 'hin' language pack installed for Tesseract!
    lang_config = 'hin+eng'
    
    if ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image, lang=lang_config)
            return text
        except Exception as e:
            print(f"Error running OCR on image: {e}")
            return ""
            
    elif ext == '.pdf':
        try:
            doc = fitz.open(file_path)
            full_text = []
            
            # Iterate through pages, render to image, then OCR
            for i in range(len(doc)):
                page = doc[i]
                # Render page to a pixmap (image)
                # scale up the resolution for better OCR
                zoom = 2.0 
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)
                
                # Convert pixmap to PIL Image
                mode = "RGBA" if pix.alpha else "RGB"
                img = Image.frombytes(mode, (pix.width, pix.height), pix.samples)
                
                # Run OCR
                text = pytesseract.image_to_string(img, lang=lang_config)
                full_text.append(text)
                
            return '\n'.join(full_text)
        except Exception as e:
            print(f"Error running OCR on PDF: {e}")
            return ""
            
    else:
        print(f"Unsupported file format for OCR: {ext}")
        return ""
