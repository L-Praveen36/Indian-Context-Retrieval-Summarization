# Task 3: English + Devanagari OCR & Text Preparation

> **Indian-Context-Aware Multilingual and Multimodal Web Retrieval & Summarization**

This module is responsible for extracting clean, machine-readable text from heterogeneous web-scraped documents — including HTML pages, text-PDFs, scanned PDFs, and photographed text — in both **English** and **Devanagari** (Hindi/Sanskrit) scripts.

---

## 📌 Overview

Task 2 (Web Retrieval) downloads raw files from the web and hands them to this module. Task 3 takes whatever file it receives, automatically determines the extraction strategy, pulls the text out, normalizes it, and detects the script and language — producing clean text passages ready for downstream summarization (Task 4).

### Pipeline Architecture

```
Input Document
       │
       ▼
┌─────────────┐
│   Router     │  Analyzes file type & PDF text layers
│  (router.py) │  to determine extraction strategy
└──────┬───────┘
       │
       ├── HTML / Text-PDF ──► Direct Extraction (extractor.py)
       │                        └─ BeautifulSoup / PyMuPDF
       │
       └── Image / Scanned PDF ──► OCR Baseline (ocr_baseline.py)
                                    ├─ OpenCV Preprocessing
                                    │   ├─ Grayscale Conversion
                                    │   ├─ Adaptive Resizing
                                    │   ├─ Median Blur Denoising
                                    │   └─ Adaptive Gaussian Thresholding
                                    └─ Tesseract OCR (hin+eng)
                                        └─ Multi-PSM Strategy (PSM 3, 6, 4)
       │
       ▼
┌──────────────┐
│  Normalizer   │  Unicode NFC normalization (critical for Devanagari),
│(normalizer.py)│  line-break repair, OCR artifact cleanup
└──────┬────────┘
       │
       ▼
┌──────────────┐
│  Detector     │  Script detection (Latin / Devanagari / Mixed)
│ (detector.py) │  Language detection (English / Hindi / Sanskrit)
└──────┬────────┘
       │
       ▼
  Output JSON
  {source_file, extraction_method, detected_script, detected_language, text_preview, text_length}
```

---

## 🗂️ Project Structure

```
TASK-3_BTP/
├── src/
│   ├── main.py              # Pipeline orchestrator & batch processor
│   ├── router.py            # Routes documents to correct extraction path
│   ├── extractor.py         # Direct text extraction (HTML, text-PDFs)
│   ├── ocr_baseline.py      # Tesseract OCR with OpenCV preprocessing
│   ├── normalizer.py        # Unicode normalization & artifact cleanup
│   └── detector.py          # Script & language detection
│
├── data/
│   ├── html/                # Test HTML files
│   │   ├── english/
│   │   ├── hindi/
│   │   ├── mixed/
│   │   └── sanskrit/
│   └── images/              # Test images for OCR
│       ├── english/
│       ├── hindi/
│       ├── mixed/
│       └── sanskrit/
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites

- **Python 3.10+**
- **Tesseract OCR** with Hindi and English language packs

### 1. Install Tesseract OCR

Download and install from: https://github.com/UB-Mannheim/tesseract/wiki

During installation, make sure to select the following additional language packs:
- `Hindi` (hin)
- `Sanskrit` (san)
- `Devanagari` (script/Devanagari)

> **Note:** If Tesseract is not in your system PATH, uncomment and update the path in `src/ocr_baseline.py`:
> ```python
> pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
> ```

### 2. Set Up the Python Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install opencv-python numpy
```

---

## 🚀 Usage

### Process a Single Document

Edit the `target_file` path in `src/main.py` and run:

```bash
python src/main.py
```

### Batch Process All Images

The current `main.py` is configured to batch-process all images in `data/images/`. Simply run:

```bash
python src/main.py
```

Results are saved to `batch_ocr_results.txt` for easy review.

### Use as a Module (API)

```python
from src.main import extract_and_prepare

result = extract_and_prepare("path/to/document.html")
# or
result = extract_and_prepare("path/to/image.jpg")
# or
result = extract_and_prepare("path/to/scanned.pdf")

print(result)
# {
#     "source_file": "document.html",
#     "extraction_method": "DIRECT_EXTRACTION",
#     "detected_script": "Mixed",
#     "detected_language": "Hindi",
#     "text_preview": "...",
#     "text_length": 1234
# }
```

---

## 🔧 How It Works

### Routing (`router.py`)
| File Type | Strategy |
|---|---|
| `.html`, `.htm`, `.txt` | Direct Extraction |
| `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff` | OCR Required |
| `.pdf` (with text layer) | Direct Extraction |
| `.pdf` (scanned / image-only) | OCR Required |

### HTML Extraction (`extractor.py`)
- Strips boilerplate elements (`<nav>`, `<footer>`, `<header>`, `<aside>`, `<script>`, `<style>`)
- Extracts clean body text using BeautifulSoup

### OCR Baseline (`ocr_baseline.py`)
The classical (non-transformer) OCR pipeline uses:

1. **OpenCV Adaptive Gaussian Thresholding** — Calculates a separate brightness threshold for every 15×15 pixel neighborhood, handling uneven lighting, dark vignettes, and colored backgrounds that global thresholding (Otsu) fails on.
2. **Median Blur Denoising** — Removes speckles, dust, and texture noise (e.g., marble cracks, rust spots on signs).
3. **Adaptive Resizing** — Scales oversized camera photographs down to a resolution Tesseract can process effectively.
4. **Multi-PSM Strategy** — Runs Tesseract with three different Page Segmentation Modes (PSM 3, 6, 4) and automatically selects the result with the highest count of real characters. This ensures signs, documents, and quotes are all handled optimally.

### Normalization (`normalizer.py`)
- **Unicode NFC Normalization** — Critical for Devanagari script, where combining characters (matras) must be properly composed for downstream search and summarization.
- **OCR Artifact Cleanup** — Strips border hallucinations (`|`, `=`, `-`) and filters out junk lines where >60% of characters are noise symbols.
- **Line Break Repair** — Collapses excessive whitespace and blank lines.

### Detection (`detector.py`)
- **Script Detection** — Regex-based detection of Latin (a-z, A-Z) and Devanagari (U+0900–U+097F) Unicode ranges.
- **Language Detection** — Uses the `langdetect` library to identify English, Hindi, Sanskrit, and other Devanagari-script languages.

---

## 📊 Supported Formats

| Format | Script Support | Method |
|---|---|---|
| HTML pages | English, Hindi, Sanskrit, Mixed | BeautifulSoup parsing |
| Text PDFs | English, Hindi, Sanskrit, Mixed | PyMuPDF text extraction |
| Scanned PDFs | English, Hindi, Mixed | Tesseract OCR |
| Photographs (JPG/PNG) | English, Hindi, Mixed | OpenCV + Tesseract OCR |

---

## ⚠️ Known Limitations (Classical Baseline)

1. **Text over complex photographic backgrounds** (e.g., quotes overlaid on landscape images) — Tesseract struggles because thresholding cannot cleanly separate semi-transparent text from a detailed background.
2. **Tiny text in large architectural photographs** — When text occupies a small fraction of the image (e.g., a sign on a building), the OCR engine reads the surrounding structures as noise.
3. **Morphological line removal is incompatible with Devanagari** — Standard border-removal techniques (OpenCV morphological operations) destroy the Shirorekha (the horizontal headline connecting Devanagari characters).

These limitations are the core motivation for the next phase of this project: implementing **Transformer-based OCR models (TrOCR / IndicOCR)** that use vision-encoder-decoder architectures to contextually understand text in photographs.

---

## 🛠️ Dependencies

| Package | Purpose |
|---|---|
| `pytesseract` | Python wrapper for Tesseract OCR engine |
| `opencv-python` | Image preprocessing (thresholding, denoising, resizing) |
| `numpy` | Array operations for OpenCV |
| `PyMuPDF` | PDF text extraction and page rendering |
| `pdfplumber` | PDF analysis |
| `beautifulsoup4` | HTML text extraction |
| `langdetect` | Language identification |

---

## 👥 Contributors

This module is part of a larger collaborative project: **Indian-Context-Aware Multilingual and Multimodal Web Retrieval & Summarization**.

---

## 📄 License

This project is developed as part of an academic B.Tech Project (BTP).
