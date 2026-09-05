import os
from router import route_document
from extractor import extract_text_direct
from ocr_baseline import run_tesseract_ocr
from detector import detect_script, detect_language

def extract_and_prepare(document_path: str) -> dict:
    """
    Main entry point for Task 3 text extraction.
    Takes a document path, routes it, extracts text, and detects metadata.
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
    
    # Clean up trailing whitespaces
    text = text.strip() if text else ""
    
    # Step 3: Detect Script and Language (Now that we have text!)
    script = detect_script(text)
    language = detect_language(text)
    
    # Step 4: Package the output
    result = {
        "source_file": os.path.basename(document_path),
        "extraction_method": route,
        "detected_script": script,
        "detected_language": language,
        "text_preview": text[:200] + ("..." if len(text) > 200 else ""),
        "text_length": len(text)
    }
    
    return result

if __name__ == "__main__":
    # Create some dummy test files if data folder is empty
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    test_html = os.path.join(data_dir, 'sample.html')
    
    if not os.path.exists(test_html):
        with open(test_html, 'w', encoding='utf-8') as f:
            f.write("<html><body><h1>Hello World</h1><p>This is a test document in English.</p><p>नमस्ते दुनिया</p></body></html>")
    
    print("Testing the pipeline...")
    test_image = os.path.join(data_dir, '2_test.png')
    result = extract_and_prepare(test_image)
    for k, v in result.items():
        print(f"{k}: {v}")
    print("\nNext steps: Place PDFs and Images in the 'data' folder and test them!")

    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(result["text_preview"])
