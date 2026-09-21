# pip install jiwer
from jiwer import cer, wer

def calculate_error_rates(ground_truth, ocr_output):
    error_cer = cer(ground_truth, ocr_output)
    error_wer = wer(ground_truth, ocr_output)
    
    cer_percent = round(error_cer * 100, 2)
    wer_percent = round(error_wer * 100, 2)
    
    print("=== OCR EVALUATION METRICS ===")
    print(f"Ground Truth : {ground_truth}")
    print(f"OCR Output   : {ocr_output}")
    print("-" * 30)
    print(f"Character Error Rate (CER) : {cer_percent}%")
    print(f"Word Error Rate (WER)      : {wer_percent}%\n")
    
    return cer_percent, wer_percent

if __name__ == '__main__':
    ground_truth = "राम कैसे थे? राम को क्यों भगवान मानते हैं लोग?"
    tesseract_output = "राम कै सेथे? राम को JयL भगवान मानतेहSलोग?"
    calculate_error_rates(ground_truth, tesseract_output)
