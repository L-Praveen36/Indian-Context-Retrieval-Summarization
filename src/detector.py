import re
from langdetect import detect, detect_langs, LangDetectException

def detect_script(text: str) -> str:
    """
    Detects whether the text is Latin, Devanagari, or Mixed.
    Devanagari Unicode Block: U+0900 - U+097F
    """
    if not text or not text.strip():
        return "Unknown"
    
    # Check for Devanagari characters
    has_devanagari = bool(re.search(r'[\u0900-\u097F]', text))
    
    # Check for Latin characters (a-z, A-Z)
    has_latin = bool(re.search(r'[a-zA-Z]', text))
    
    if has_devanagari and has_latin:
        return "Mixed"
    elif has_devanagari:
        return "Devanagari"
    elif has_latin:
        return "Latin"
    else:
        return "Other"

def detect_language(text: str) -> str:
    """
    Detects the language of the text.
    Handles English, Hindi, and attempts basic Sanskrit detection.
    """
    if not text or not text.strip():
        return "Unknown"
    
    try:
        # langdetect returns ISO 639-1 codes (e.g., 'en', 'hi', 'mr', 'ne')
        lang_code = detect(text)
        
        if lang_code == 'en':
            return "English"
        elif lang_code == 'hi':
            return "Hindi"
        elif lang_code == 'sa':  # 'sa' is rarely perfectly detected by langdetect
            return "Sanskrit"
        elif lang_code in ['mr', 'ne']: # Marathi, Nepali etc. often share Devanagari
             script = detect_script(text)
             if script == "Devanagari":
                 return f"Other Devanagari ({lang_code})"
             return f"Other ({lang_code})"
        else:
            return f"Other ({lang_code})"
            
    except LangDetectException:
        return "Unknown"
