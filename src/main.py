import os
from router import route_document
from extractor import extract_text_direct
from ocr_baseline import run_tesseract_ocr
from detector import detect_script, detect_language
from normalizer import normalize_text

def extract_and_prepare(document_path: str) -> dict:
    """
    Main entry point for Task 3 text extraction.
    Takes a document path, routes it, extracts text, normalizes it, and detects metadata.
    """
    print(f"--- Processing: {os.path.basename(document_path)} ---")
    
    # Step 1: Detect and route
    route = route_document(document_path)
    print(f"Route determined: {route}")
    
    # Step 2: Extract Text
    text = ""
    if route == 'DIRECT_EXTRACTION':
        text = extract_text_direct(document_path)
    elif route == 'OCR_REQUIRED':
        text = run_tesseract_ocr(document_path)
    
    # Step 3: Normalize Text (Unicode NFC, fix formatting, strip artifacts)
    text = normalize_text(text)
    
    # Step 3: Detect Script and Language (Now that we have text!)
    script = detect_script(text)
    language = detect_language(text)
    
    # Step 4: Package the output
    result = {
        "source_file": os.path.basename(document_path),
        "extraction_method": route,
        "detected_script": script,
        "detected_language": language,
        "full_text": text,
        "text_preview": text[:200] + ("..." if len(text) > 200 else ""),
        "text_length": len(text)
    }
    
    return result

if __name__ == "__main__":
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    
    if not os.path.exists(data_dir):
        print(f"Error: Could not find the data directory at {data_dir}")
    else:
        print(f"Starting batch processing for all files in: {data_dir}\n")
        
        # Open separate master files for different categories
        with open("batch_ocr_results.txt", "w", encoding="utf-8") as img_out, \
             open("batch_html_results.txt", "w", encoding="utf-8") as html_out, \
             open("batch_pdf_results.txt", "w", encoding="utf-8") as pdf_out:
            
            # Walk through all subfolders (images, html, pdfs, etc.)
            for root, _, files in os.walk(data_dir):
                for filename in files:
                    ext = filename.lower()
                    
                    # Determine which file to write to based on extension
                    if ext.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                        out_file = img_out
                        file_type = "Image"
                    elif ext.endswith(('.html', '.htm')):
                        out_file = html_out
                        file_type = "HTML"
                    elif ext.endswith('.pdf'):
                        out_file = pdf_out
                        file_type = "PDF"
                    else:
                        continue  # Skip unsupported files
                        
                    file_path = os.path.join(root, filename)
                    
                    try:
                        result = extract_and_prepare(file_path)
                        
                        # Print a short summary to the console
                        print(f"Finished [{file_type}]: {filename} -> Script: {result['detected_script']}")
                        
                        # Write the full details into the respective batch review file
                        out_file.write(f"=== File: {filename} ===\n")
                        out_file.write(f"Folder: {os.path.basename(root)}\n")
                        out_file.write(f"Language: {result['detected_language']} | Script: {result['detected_script']}\n")
                        out_file.write(f"Extraction Method: {result['extraction_method']}\n")
                        out_file.write(f"Text Extracted:\n{result['full_text']}\n")
                        out_file.write("="*50 + "\n\n")
                        
                    except Exception as e:
                        print(f"Error processing {filename}: {e}")
                        
        print("\nBatch processing complete! Output files generated:")
        print("- batch_ocr_results.txt (for Images)")
        print("- batch_html_results.txt (for HTML)")
        print("- batch_pdf_results.txt (for PDFs)")
