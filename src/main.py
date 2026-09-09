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
        "text_preview": text[:200] + ("..." if len(text) > 200 else ""),
        "text_length": len(text)
    }
    
    return result

if __name__ == "__main__":
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    images_dir = os.path.join(data_dir, 'images')
    
    if not os.path.exists(images_dir):
        print(f"Error: Could not find the images directory at {images_dir}")
    else:
        print(f"Starting batch OCR processing for images in: {images_dir}\n")
        
        # Open a master file to save all results for easy review
        with open("batch_ocr_results.txt", "w", encoding="utf-8") as out_file:
            
            # Walk through all subfolders (mixed, hindi, english, etc.)
            for root, _, files in os.walk(images_dir):
                for filename in files:
                    # Filter for image files only
                    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                        file_path = os.path.join(root, filename)
                        
                        try:
                            result = extract_and_prepare(file_path)
                            
                            # Print a short summary to the console
                            print(f"Finished: {filename} -> Script: {result['detected_script']}")
                            
                            # Write the full details into our batch review file
                            out_file.write(f"=== File: {filename} ===\n")
                            out_file.write(f"Folder: {os.path.basename(root)}\n")
                            out_file.write(f"Language: {result['detected_language']} | Script: {result['detected_script']}\n")
                            out_file.write(f"Text Extracted:\n{result['text_preview']}\n")
                            out_file.write("="*50 + "\n\n")
                            
                        except Exception as e:
                            print(f"Error processing {filename}: {e}")
                            
        print("\nBatch processing complete! Open 'batch_ocr_results.txt' to review all the extracted text.")
