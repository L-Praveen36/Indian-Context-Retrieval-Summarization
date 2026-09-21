import os
import sys

# Add src to python path so we can import from main
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from main import extract_and_prepare

# Target directories
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'DATA_NEW'))

html_dir = os.path.join(base_dir, 'html')
pdf_dir = os.path.join(base_dir, 'pdf')
img_dir = os.path.join(base_dir, 'img')

def process_folder(folder_path, output_file_name):
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return
        
    output_path = os.path.join(base_dir, output_file_name)
    print(f"\nProcessing {folder_path} -> Output to: {output_path}")
    
    with open(output_path, 'w', encoding='utf-8') as out_file:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                try:
                    result = extract_and_prepare(file_path)
                    
                    # Write the full details
                    out_file.write(f"=== File: {filename} ===\n")
                    out_file.write(f"Language: {result['detected_language']} | Script: {result['detected_script']}\n")
                    out_file.write(f"Extraction Method: {result['extraction_method']}\n")
                    out_file.write(f"Text Extracted:\n{result['full_text']}\n")
                    out_file.write("="*50 + "\n\n")
                    
                except Exception as e:
                    print(f"Error processing {filename}: {e}")

if __name__ == '__main__':
    process_folder(html_dir, 'html_results.txt')
    process_folder(pdf_dir, 'pdf_results.txt')
    process_folder(img_dir, 'img_results.txt')
    print("\nAll done! Output files are saved in the DATA_NEW folder.")
