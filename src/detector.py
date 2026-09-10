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
    Handles English, Hindi, Sanskrit, and mixed-language content.
    Cross-references with script detection for accuracy.
    """
    if not text or not text.strip():
        return "Unknown"
    
    # First, check what scripts are present
    script = detect_script(text)
    
    try:
        # langdetect returns ISO 639-1 codes (e.g., 'en', 'hi', 'mr', 'ne')
        lang_code = detect(text)
        
        # Helper logic to distinguish Sanskrit from Hindi (overriding langdetect)
        is_sanskrit = False
        if script in ["Devanagari", "Mixed"]:
            # 1. Double Danda is virtually exclusive to Sanskrit verses
            has_double_danda = '॥' in text
            
            # 2. Count strong Sanskrit grammatical markers (word-final halants)
            sanskrit_markers = len(re.findall(r'म्\s|त्\s|म्$|त्$|ो5', text))
            
            # 3. Count common Hindi stopwords
            padded = f" {text} ".replace('\n', ' ').replace('।', ' ')
            hindi_words = [' है ', ' और ', ' में ', ' का ', ' की ', ' को ', ' से ', ' कि ', ' यह ', ' वह ', ' एक ', ' हैं ']
            hindi_count = sum(padded.count(w) for w in hindi_words)
            
            # Decision Tree:
            if has_double_danda or sanskrit_markers >= 2:
                is_sanskrit = True
            elif hindi_count >= 2:
                is_sanskrit = False  # Definitely Hindi if it has multiple Hindi stopwords
            elif lang_code == 'sa':
                is_sanskrit = True
            elif text.count('ः') >= 2 and hindi_count == 0:
                is_sanskrit = True

        # Handle Mixed script
        if script == "Mixed":
            if is_sanskrit:
                return "Sanskrit + English"
            # Default to Hindi+English if it has Devanagari but isn't Sanskrit
            return "Hindi + English"
        
        # Handle Single script
        if script == "Devanagari":
            if is_sanskrit:
                return "Sanskrit"
            else:
                return "Hindi"
                
        if lang_code == 'en':
            return "English"
        else:
            return f"Other ({lang_code})"
            
    except LangDetectException:
        return "Unknown"
