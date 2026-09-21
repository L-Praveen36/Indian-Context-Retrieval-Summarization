import os
import pytesseract
from PIL import Image
import cv2
import numpy as np
import pymupdf as fitz  # PyMuPDF

# Note for Windows users: 
# You may need to set the tesseract path if it's not in your system PATH.
# Uncomment and update the line below if necessary:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def _prepare_gray(image: Image.Image) -> np.ndarray:
    """
    Common first steps: convert to grayscale, resize, and handle dark backgrounds.
    Returns an OpenCV grayscale numpy array.
    """
    cv_img = np.array(image.convert('RGB'))
    cv_img = cv_img[:, :, ::-1].copy()
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

    height, width = gray.shape
    if max(height, width) > 2500:
        scale = 2500 / max(height, width)
        gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

    mean_brightness = np.mean(gray)
    if mean_brightness < 85:
        gray = cv2.bitwise_not(gray)

    return gray


def preprocess_otsu(image: Image.Image) -> Image.Image:
    """
    Preprocessing with Otsu's global thresholding.
    Best for: uniformly lit images (signs, posters, scanned documents).
    """
    gray = _prepare_gray(image)
    denoised = cv2.medianBlur(gray, 3)
    _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return Image.fromarray(thresh)


def preprocess_adaptive(image: Image.Image) -> Image.Image:
    """
    Preprocessing with Adaptive Gaussian thresholding.
    Best for: photographs with uneven lighting, vignettes, dark edges.
    """
    gray = _prepare_gray(image)
    denoised = cv2.medianBlur(gray, 3)
    adaptive_thresh = cv2.adaptiveThreshold(
        denoised, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        blockSize=15,
        C=8
    )
    return Image.fromarray(adaptive_thresh)


def _count_real_characters(text: str) -> int:
    """
    Counts how many real letters/numbers are in the OCR output.
    Used internally by language selection.
    """
    import re
    matches = re.findall(r'[a-zA-Z0-9\u0900-\u097F]', text)
    return len(matches)


def _text_quality_score(text: str) -> float:
    """
    Measures the QUALITY of OCR output, not just the quantity.
    Real text has longer words (avg 3+ chars). Garbage from noisy photographs
    has scattered single characters and very short "words".
    Returns a score where higher = better quality text.
    """
    import re
    words = re.findall(r'[a-zA-Z\u0900-\u097F]{2,}', text)
    
    if not words:
        return 0
    
    avg_len = sum(len(w) for w in words) / len(words)
    return len(words) * avg_len


def _count_devanagari(text: str) -> int:
    """Counts the number of Devanagari characters in the text."""
    import re
    return len(re.findall(r'[\u0900-\u097F]', text))


def _count_latin(text: str) -> int:
    """Counts the number of Latin characters in the text."""
    import re
    return len(re.findall(r'[a-zA-Z]', text))


def _run_ocr_with_config(image: Image.Image, lang: str, psm: int) -> str:
    """
    Runs Tesseract on a preprocessed image with a specific PSM mode.
    """
    config = f'--oem 3 --psm {psm}'
    try:
        return pytesseract.image_to_string(image, lang=lang, config=config)
    except Exception:
        return ""


def _pick_best_language_result(processed: Image.Image) -> str:
    """
    Smart language selection strategy:
    1. Always try hin+eng FIRST (it can handle both scripts).
    2. If the result has real Devanagari content (>10%), use it immediately.
    3. Only try eng-only as a fallback when the text appears purely English,
       to avoid Hindi character hallucinations from background noise.
    """
    best_hin = ""
    best_hin_score = 0
    for psm in [3, 6, 4]:
        text = _run_ocr_with_config(processed, 'hin+eng', psm)
        score = _count_real_characters(text)
        if score > best_hin_score:
            best_hin_score = score
            best_hin = text

    devanagari_count = _count_devanagari(best_hin)
    latin_count = _count_latin(best_hin)
    total = devanagari_count + latin_count

    if total > 0 and devanagari_count / total > 0.10:
        return best_hin

    best_eng = ""
    best_eng_score = 0
    for psm in [3, 6, 4]:
        text = _run_ocr_with_config(processed, 'eng', psm)
        score = _count_real_characters(text)
        if score > best_eng_score:
            best_eng_score = score
            best_eng = text

    if best_eng_score >= best_hin_score * 0.7:
        return best_eng
    else:
        return best_hin


def _process_image_3path(image: Image.Image) -> str:
    """Runs the 3-path OCR strategy on a single image and returns the best text."""
    # PATH 1: Otsu preprocessing
    otsu_img = preprocess_otsu(image)
    result_otsu = _pick_best_language_result(otsu_img)

    # PATH 2: Adaptive preprocessing
    adaptive_img = preprocess_adaptive(image)
    result_adaptive = _pick_best_language_result(adaptive_img)

    # PATH 3: Raw grayscale (no preprocessing)
    raw_gray = image.convert('L')
    result_raw = _pick_best_language_result(raw_gray)

    # Pick the highest quality result
    candidates = [
        (result_otsu, _text_quality_score(result_otsu)),
        (result_adaptive, _text_quality_score(result_adaptive)),
        (result_raw, _text_quality_score(result_raw)),
    ]
    return max(candidates, key=lambda x: x[1])[0]


def run_tesseract_ocr(file_path: str) -> str:
    """
    Runs Tesseract OCR on an image or scanned PDF.
    Tries THREE paths and picks the highest quality result:
      1. Otsu thresholding (best for uniformly lit images)
      2. Adaptive thresholding (best for uneven lighting / vignettes)
      3. Raw grayscale (best for clean digital documents)
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
        try:
            image = Image.open(file_path)
            return _process_image_3path(image)
        except Exception as e:
            print(f"Error running OCR on image: {e}")
            return ""

    elif ext == '.pdf':
        try:
            doc = fitz.open(file_path)
            full_text = []

            for i in range(len(doc)):
                page = doc[i]
                zoom = 2.0
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)

                mode = "RGBA" if pix.alpha else "RGB"
                img = Image.frombytes(mode, (pix.width, pix.height), pix.samples)

                # Run the 3-path OCR strategy on the PDF page image
                text = _process_image_3path(img)
                full_text.append(text)

            return '\n'.join(full_text)
        except Exception as e:
            print(f"Error running OCR on PDF: {e}")
            return ""

    else:
        print(f"Unsupported file format for OCR: {ext}")
        return ""

def run_ocr_with_confidence(image_matrix, lang='hin+eng'):
    """
    Runs Tesseract OCR on an image and calculates the average confidence score.
    Returns: extracted_text, average_confidence, reliability_flag
    """
    from pytesseract import Output
    
    # Ask Tesseract for detailed dictionary output instead of just a string
    ocr_data = pytesseract.image_to_data(image_matrix, lang=lang, output_type=Output.DICT)
    
    valid_words = []
    confidences = []
    
    # Loop through everything Tesseract found
    for i in range(len(ocr_data['text'])):
        word = ocr_data['text'][i].strip()
        conf = int(ocr_data['conf'][i])
        
        # Tesseract outputs a confidence of -1 for empty layout blocks
        # We only want to score actual text words (confidence >= 0)
        if len(word) > 0 and conf >= 0:
            valid_words.append(word)
            confidences.append(conf)
            
    # Rebuild the final text
    extracted_text = " ".join(valid_words)
    
    # Calculate the average confidence of the entire passage
    if len(confidences) > 0:
        avg_confidence = sum(confidences) / len(confidences)
    else:
        avg_confidence = 0.0
        
    # Flag the reliability for Task 4 and Task 5
    if avg_confidence >= 80.0:
        reliability = "HIGH"
    elif avg_confidence >= 60.0:
        reliability = "MEDIUM"
    else:
        reliability = "LOW"
        
    return extracted_text, round(avg_confidence, 2), reliability
