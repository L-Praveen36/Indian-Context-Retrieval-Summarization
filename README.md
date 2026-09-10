# Task 3: English and Devanagari OCR & Text Preparation

**Project: Indian-Context-Aware Multilingual and Multimodal Web Retrieval & Summarization**

## Overview: What We Did

This module serves as the 40% vertical slice for the project mid-evaluation. It is a strictly classical (non-neural) baseline pipeline designed to extract clean, machine-readable text from heterogeneous web documents. 

The system accepts documents from the Web Retrieval module (Task 2) and automatically routes them based on file type and structural metadata. It supports English, Hindi, and Sanskrit across HTML pages, digital PDFs, scanned PDFs, and complex photographs. 

Key achievements in this baseline:
1. Built an end-to-end routing and extraction pipeline handling diverse file types natively.
2. Implemented a 3-path OCR preprocessing strategy (Otsu, Adaptive, Raw) to automatically resolve complex lighting and document degradation without relying on deep learning models.
3. Engineered custom linguistic heuristics (e.g., Double Danda, Halant, and Stopword analysis) to reliably distinguish Sanskrit from high-register Hindi, overcoming known limitations in standard language detection libraries.

## Tech Stack

*   **Language:** Python 3.10+
*   **OCR Engine:** Tesseract OCR (with `hin`, `san`, and `eng` language packs)
*   **Computer Vision:** OpenCV, NumPy (for classical image preprocessing)
*   **PDF Processing:** PyMuPDF (`fitz`)
*   **HTML Parsing:** BeautifulSoup4
*   **NLP & Detection:** `langdetect`, Python `re` (Regex)

## Pipeline Architecture

```text
Input Document
       │
       ▼
┌─────────────┐
│   Router    │ Analyzes file type and PDF text layers 
│ (router.py) │ to determine the optimal extraction strategy
└──────┬──────┘
       │
       ├── HTML / Text-PDF ──► Direct Extraction (extractor.py)
       │                       └─ BeautifulSoup / PyMuPDF
       │
       └── Image / Scanned PDF ──► OCR Baseline (ocr_baseline.py)
                                   ├─ 3-Path Preprocessing (Otsu, Adaptive, Raw)
                                   └─ Tesseract OCR (Multi-PSM Strategy)
       │
       ▼
┌──────────────┐
│  Normalizer  │ Unicode NFC normalization (critical for Devanagari),
│(normalizer.py│ line-break repair, and OCR artifact cleanup
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Detector    │ Script detection (Latin / Devanagari / Mixed)
│ (detector.py)│ Language detection (English / Hindi / Sanskrit)
└──────┬───────┘
       │
       ▼
  Output JSON / Batch Text Files
```

## Project Structure

```text
TASK-3_BTP/
├── src/
│   ├── main.py              # Pipeline orchestrator and batch processor
│   ├── router.py            # Routes documents to correct extraction path
│   ├── extractor.py         # Direct text extraction (HTML, text-PDFs)
│   ├── ocr_baseline.py      # Tesseract OCR with 3-path OpenCV preprocessing
│   ├── normalizer.py        # Unicode normalization and artifact cleanup
│   └── detector.py          # Script and language detection with Sanskrit heuristics
├── data/                    # Test documents (HTML, PDFs, Images)
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

## Setup and Installation

### Prerequisites

*   Python 3.10+
*   Tesseract OCR installed locally

### 1. Install Tesseract OCR

Ensure Tesseract is installed and available in your system path.
Download for Windows: https://github.com/UB-Mannheim/tesseract/wiki

Required language packs during installation:
*   `English` (eng)
*   `Hindi` (hin)
*   `Sanskrit` (san)
*   `Devanagari` (script/Devanagari)

### 2. Python Environment

```bash
# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

## Usage

The primary entry point is configured to batch-process all documents in the `data/` directory.

```bash
python src/main.py
```

Upon execution, the script categorizes and processes every file, generating three output reports:
1.  `batch_ocr_results.txt`: Contains extracted text from images.
2.  `batch_html_results.txt`: Contains cleaned text from HTML files.
3.  `batch_pdf_results.txt`: Contains text from both digital and scanned PDFs.

## How It Works

### Routing (`router.py`)
Analyzes the file extension and, for PDFs, checks the density of the embedded text layer to determine if the document requires OCR or can be parsed directly.

### HTML Extraction (`extractor.py`)
Removes structural boilerplate (`<nav>`, `<footer>`, `<script>`, `<style>`, etc.) to isolate the primary body text using BeautifulSoup.

### OCR Baseline (`ocr_baseline.py`)
Applies a 3-path strategy for optimal character recognition:
1.  **Otsu Thresholding:** Global thresholding for uniformly lit signs and scanned documents.
2.  **Adaptive Gaussian Thresholding:** Localized thresholding for uneven lighting, shadows, and vignettes.
3.  **Raw Grayscale:** Unprocessed path for clean digital screenshots.

The engine runs all three paths, evaluates the text quality (prioritizing average word length to filter out background noise artifacts), and automatically selects the highest-fidelity output.

### Normalization (`normalizer.py`)
Applies Unicode NFC normalization to properly compose Devanagari combining characters (matras). It also collapses erratic whitespace and strips common OCR border hallucinations.

### Detection (`detector.py`)
Cross-references script Unicode blocks with statistical language detection. It employs a custom linguistic heuristic—scanning for Hindi stopwords, double dandas, and word-final halants—to reliably distinguish Sanskrit from Hindi, correcting a prominent failure mode in the `langdetect` library.

## Supported Formats

| Format | Script Support | Method |
|---|---|---|
| HTML pages | English, Hindi, Sanskrit, Mixed | BeautifulSoup parsing |
| Text PDFs | English, Hindi, Sanskrit, Mixed | PyMuPDF text extraction |
| Scanned PDFs | English, Hindi, Mixed | OpenCV + Tesseract OCR |
| Photographs (JPG/PNG) | English, Hindi, Mixed | OpenCV + Tesseract OCR |

## Known Limitations (Classical Baseline)

1.  **Text over complex photographic backgrounds:** Tesseract struggles when text is overlaid on highly detailed backgrounds, as classical thresholding cannot effectively isolate semi-transparent or low-contrast text.
2.  **Architectural noise:** When text occupies a minor fraction of a photograph, the OCR engine frequently misinterprets structural background elements as characters.
3.  **Shirorekha degradation:** Standard morphological operations used for border removal often destroy the horizontal headline (Shirorekha) connecting Devanagari characters, causing catastrophic OCR failure.

These limitations are acknowledged and serve as the justification for integrating Transformer-based OCR models (e.g., TrOCR, IndicOCR) in the next phase of the project.

## Contributors

This module is part of a larger collaborative project: **Indian-Context-Aware Multilingual and Multimodal Web Retrieval & Summarization**.

## License

This project is developed as part of an academic B.Tech Project (BTP).
