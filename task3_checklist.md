# Task 3: English & Devanagari OCR & Text Preparation - Progress Checklist

## Phase 1: Classical Baseline 
- [x] **Project Setup**
  - [x] Define module boundaries and repository structure.
  - [x] Configure virtual environment and base dependencies.
- [x] **Direct Text Extraction**
  - [x] HTML Parsing (BeautifulSoup) with boilerplate/tag stripping.
  - [x] Native PDF Extraction (PyMuPDF) for digital documents.
- [x] **Classical OCR Pipeline**
  - [x] Tesseract OCR integration with `hin`, `san`, and `eng` language packs.
  - [x] Multi-PSM Strategy (Page Segmentation Modes 3, 6, 4) for varying text blocks.
- [x] **Advanced OpenCV Preprocessing**
  - [x] Grayscale conversion and Adaptive Resizing.
  - [x] Median Blur Denoising (removing speckles/noise).
  - [x] 3-Path Strategy: Global Otsu Thresholding (for uniform lighting).
  - [x] 3-Path Strategy: Adaptive Gaussian Thresholding (for uneven lighting/vignettes).
  - [x] Quality Scoring mechanism to automatically select the best preprocessing path.
- [x] **Text Normalization**
  - [x] Unicode NFC Normalization (critical for composing Devanagari matras).
  - [x] OCR artifact cleanup (stripping false borders `|`, `=`, `-` and junk lines).
  - [x] Line break repair and whitespace collapse.
- [x] **Script & Language Detection**
  - [x] Unicode block regex detection (Latin vs. Devanagari vs. Mixed).
  - [x] Integration with `langdetect` for baseline ISO codes.
  - [x] Custom linguistic heuristics (Double Danda, Halants).
  - [x] Hindi stopword analysis to prevent Sanskrit false-positives.
- [x] **Pipeline Orchestration**
  - [x] Automated router based on file extension and PDF text-layer density.
  - [x] Batch processing script capable of handling the entire `data/` directory.
  - [x] Categorized output routing (`batch_ocr_results.txt`, `html_results`, `pdf_results`).

## Phase 2: Neural Architecture & Final Integration (Post-Mid-Eval)
- [ ] **Advanced Text Detection & Layout Analysis**
  - [ ] Implement CRAFT (Character Region Awareness) to localize text in complex backgrounds.
  - [ ] Implement LayoutLM for multi-column newspaper and table reading-order extraction.
- [ ] **Transformer-based Recognition (Replacing Tesseract)**
  - [ ] Integrate TrOCR to resolve the 60% WER caused by Devanagari spacebar and Shirorekha failures.
- [ ] **Near-Duplicate Detection (Optimization)**
  - [ ] Implement MinHash (Locality-Sensitive Hashing) to detect and destroy duplicate payloads from Task 2.
- [ ] **Task 4 Handoff & Pipeline Hardening**
  - [x] Finalize standard JSON schema output format (Metadata + Provenance).
  - [x] Establish evaluation metrics (CER = 21%, WER = 60%).
  - [ ] Build automated webhook/API handoff to seamlessly feed the JSONs to Task 4 Vector Database.
