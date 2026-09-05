import os
import pymupdf as fitz  # PyMuPDF

def route_document(file_path: str) -> str:
    """
    Analyzes a document and determines the required extraction path.
    Returns: 'DIRECT_EXTRACTION' or 'OCR_REQUIRED'
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    if ext in ['.html', '.htm', '.txt']:
        return 'DIRECT_EXTRACTION'
    
    if ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
        return 'OCR_REQUIRED'
    
    if ext == '.pdf':
        try:
            # Open PDF with PyMuPDF
            doc = fitz.open(file_path)
            total_text_length = 0
            # Check the first few pages for text
            pages_to_check = min(3, len(doc))
            for i in range(pages_to_check):
                page = doc[i]
                text = page.get_text()
                total_text_length += len(text.strip())
            
            # If the PDF contains sufficient text, it's a text-PDF
            if total_text_length > 50:
                return 'DIRECT_EXTRACTION'
            else:
                return 'OCR_REQUIRED'
        except Exception as e:
            print(f"Error analyzing PDF {file_path}: {e}")
            return 'OCR_REQUIRED'  # Fallback to OCR if PyMuPDF fails
    
    return 'OCR_REQUIRED'  # Default fallback
