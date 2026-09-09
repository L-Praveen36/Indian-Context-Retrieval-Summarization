import unicodedata
import re

def normalize_text(text: str) -> str:
    """
    Applies Unicode normalization and cleans up OCR artifacts,
    as explicitly required by the Task 3 Problem Statement.
    """
    if not text:
        return ""

    # 1. Unicode Normalization (NFC is crucial for Devanagari combining characters)
    text = unicodedata.normalize('NFC', text)

    # 2. Repair broken line/paragraph breaks
    text = re.sub(r'\n{3,}', '\n\n', text)

    # 3. OCR Artifact Cleanup — process line by line
    cleaned_lines = []
    for line in text.split('\n'):
        # Strip border artifacts from edges of lines
        line = line.strip(" |=*-~_.:;'\"")

        # Skip lines that are purely junk (no real letters or digits)
        if not re.search(r'[a-zA-Z0-9\u0900-\u097F]', line):
            continue

        # Skip very short lines that are likely noise (single random characters)
        if len(line) <= 2:
            continue

        # Count how many real characters vs junk characters are in this line
        real_chars = len(re.findall(r'[a-zA-Z0-9\u0900-\u097F\s,.\?!]', line))
        total_chars = len(line)

        # If more than 60% of the line is junk symbols, skip it
        if total_chars > 5 and real_chars / total_chars < 0.4:
            continue

        cleaned_lines.append(line)

    text = '\n'.join(cleaned_lines)

    # 4. Clean up extra spaces (multiple spaces/tabs -> single space)
    text = re.sub(r'[ \t]+', ' ', text)

    return text.strip()
