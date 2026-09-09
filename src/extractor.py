import pymupdf as fitz  # PyMuPDF
from bs4 import BeautifulSoup
import os

def extract_text_direct(file_path: str) -> str:
    """
    Extracts text directly from HTML or text-based PDFs.
    """
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext in ['.html', '.htm']:
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            
            # Remove website boilerplate (navigation, footers, scripts, styles, sidebars)
            junk_tags = ['script', 'style', 'nav', 'footer', 'header', 'aside', 'noscript']
            for element in soup(junk_tags):
                element.decompose()
                
            # Extract clean text and remove extra whitespace
            text = soup.get_text(separator='\n')
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            return '\n'.join(lines)
            
    elif ext == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
            
    elif ext == '.pdf':
        try:
            doc = fitz.open(file_path)
            full_text = []
            for page in doc:
                full_text.append(page.get_text())
            return '\n'.join(full_text)
        except Exception as e:
            print(f"Error extracting PDF directly: {e}")
            return ""
            
    else:
        print(f"Unsupported file format for direct extraction: {ext}")
        return ""
