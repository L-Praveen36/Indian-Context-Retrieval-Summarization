# Task 3: English & Devanagari OCR & Text Preparation - Progress Checklist

## Phase 1: Classical Baseline & 40% Vertical Slice (Mid-Evaluation)
- [x] **Project Scaffolding & Setup**
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
- [x] **Mid-Evaluation Deliverables**
  - [x] Professional README with architecture, tech stack, and limitations.
  - [x] Git commits successfully pushed to the `task-3-baseline` branch.

## Phase 2: Neural / Deep Learning OCR Transition (Post-Mid-Eval)
- [ ] **Advanced Text Detection (Addressing limitation #1 & #2)**
  - [ ] Implement CRAFT, EAST, or DBNet to localize text in complex photographic backgrounds.
  - [ ] Implement bounding box cropping for isolated text recognition.
- [ ] **Transformer-based Recognition (Addressing limitation #3)**
  - [ ] Evaluate and integrate TrOCR, IndicOCR, or PaddleOCR for Devanagari.
  - [ ] Robust handling of Devanagari Shirorekha (headline) degradation.
- [ ] **Complex Layout Analysis**
  - [ ] Implement table and multi-column extraction (e.g., LayoutLM).
  - [ ] Reading order sorting (top-to-bottom, left-to-right alignment).
- [ ] **Optimization**
  - [ ] GPU (CUDA) integration for neural model inference speedup.

## Phase 3: Final Integration & Task 4 Handoff
- [ ] **Quality Assurance**
  - [ ] Establish evaluation metrics (Character Error Rate - CER, Word Error Rate - WER).
  - [ ] Benchmark Classical Pipeline vs. Neural Pipeline accuracy.
- [ ] **Pipeline Hardening**
  - [ ] Multiprocessing/Parallelization for bulk document processing.
  - [ ] Advanced error handling for corrupted or inaccessible files.
- [ ] **Summarization Handoff (Task 4)**
  - [ ] Finalize standard JSON schema output format.
  - [ ] Connect Task 3 outputs directly to the Summarization (Task 4) ingestion layer.
