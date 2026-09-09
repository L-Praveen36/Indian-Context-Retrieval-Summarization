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


def preprocess_image_for_ocr(image: Image.Image) -> Image.Image:
    """
    Cleans up a raw photograph using OpenCV to look like a scanned document.
    Uses Adaptive Gaussian Thresholding instead of global Otsu so that 
    images with dark edges, vignettes, or uneven lighting are handled properly.
    """
    # Convert PIL Image to OpenCV format (NumPy array)
    cv_img = np.array(image.convert('RGB'))
    cv_img = cv_img[:, :, ::-1].copy()  # RGB to BGR

    # 1. Convert to Grayscale
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

    # 2. Resize if massive (but keep more detail than before — 2500px limit)
    height, width = gray.shape
    if max(height, width) > 2500:
        scale = 2500 / max(height, width)
        gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

    # 3. Denoise (Median Blur) — removes tiny speckles like rust, dust, marble cracks
    denoised = cv2.medianBlur(gray, 3)

    # 4. Adaptive Gaussian Thresholding
    #    Unlike global Otsu (which picks ONE threshold for the whole image),
    #    this calculates a separate threshold for every 15x15 pixel neighborhood.
    #    This means dark corners/vignettes don't destroy the text in bright areas.
    adaptive_thresh = cv2.adaptiveThreshold(
        denoised, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        blockSize=15,  # Size of the local neighborhood
        C=8            # Constant subtracted from the local mean
    )

    return Image.fromarray(adaptive_thresh)


def _count_real_characters(text: str) -> int:
    """
    Counts how many real letters/numbers are in the OCR output.
    Used to compare which PSM mode gave the best result.
    """
    import re
    # Count Latin letters, digits, and Devanagari characters (U+0900 to U+097F)
    matches = re.findall(r'[a-zA-Z0-9\u0900-\u097F]', text)
    return len(matches)


def _run_ocr_with_config(image: Image.Image, lang: str, psm: int) -> str:
    """
    Runs Tesseract on a preprocessed image with a specific PSM mode.
    """
    config = f'--oem 3 --psm {psm}'
    try:
        return pytesseract.image_to_string(image, lang=lang, config=config)
    except Exception:
        return ""


def run_tesseract_ocr(file_path: str) -> str:
    """
    Runs Tesseract OCR on an image or scanned PDF.
    Tries multiple Page Segmentation Modes (PSM) and picks the best result.
    """
    ext = os.path.splitext(file_path)[1].lower()

    # hin+eng to support both Devanagari and Latin scripts
    lang_config = 'hin+eng'

    if ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
        try:
            image = Image.open(file_path)

            # Run our OpenCV preprocessing pipeline
            processed = preprocess_image_for_ocr(image)

            # Strategy: Try multiple PSM modes and keep the best result.
            # PSM 3 = Fully automatic page segmentation (good for documents)
            # PSM 6 = Assume a single uniform block of text (good for signs/posters)
            # PSM 4 = Assume a single column of variable-size text (good for quotes)
            best_text = ""
            best_score = 0

            for psm in [3, 6, 4]:
                text = _run_ocr_with_config(processed, lang_config, psm)
                score = _count_real_characters(text)
                if score > best_score:
                    best_score = score
                    best_text = text

            return best_text

        except Exception as e:
            print(f"Error running OCR on image: {e}")
            return ""

    elif ext == '.pdf':
        try:
            doc = fitz.open(file_path)
            full_text = []

            for i in range(len(doc)):
                page = doc[i]
                # Render page at 2x zoom for better OCR quality
                zoom = 2.0
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)

                # Convert pixmap to PIL Image
                mode = "RGBA" if pix.alpha else "RGB"
                img = Image.frombytes(mode, (pix.width, pix.height), pix.samples)

                # Preprocess and run OCR
                processed = preprocess_image_for_ocr(img)
                text = _run_ocr_with_config(processed, lang_config, 3)
                full_text.append(text)

            return '\n'.join(full_text)
        except Exception as e:
            print(f"Error running OCR on PDF: {e}")
            return ""

    else:
        print(f"Unsupported file format for OCR: {ext}")
        return ""
