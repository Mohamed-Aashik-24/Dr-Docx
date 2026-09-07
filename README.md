# ML-Based DOCX Publication Formatter

An end-to-end, **100% offline Machine Learning & Rule-Engine Pipeline** for transforming unformatted manuscript documents (`.docx`) into publication-ready books, textbooks, and academic papers following strict publishing standards.

Includes a **Python Flask Backend API** powering a modern **React + Vite Frontend Dashboard**.

---

## 🌟 Key Features

### 🧠 Intelligent Machine Learning & Structure Recognition
- **Hybrid Classification Engine**: Combines a Random Forest classifier (TF-IDF + 25 structural features) with heuristic rules and contextual post-processing.
- **Recognized Element Types**:
  - `TITLE`, `AUTHOR`, `CHAPTER_HEADING`, `SECTION_HEADING`, `SUBSECTION_HEADING`
  - `BODY`, `LIST_ITEM`, `FIGURE`, `FIGURE_CAPTION`, `TABLE`, `TABLE_CAPTION`
  - `TOC_HEADING`, `TOC_ENTRY`, `INDEX_HEADING`, `INDEX_ENTRY`
  - `REFERENCE_HEADING`, `REFERENCE_ENTRY`, `ABSTRACT_HEADING`, `ABOUT_AUTHOR_HEADING`
  - `MCQ_HEADING`, `MCQ_QUESTION`, `MCQ_OPTION`, `MCQ_ANSWER`
- **Unnumbered Heading Detection**: Automatically detects chapter headings even when section numbers (e.g., `1.1`) are absent.

### 📐 Automated Publication Formatting
- **Typography & Spacing**:
  - **Body & Lists**: Strict 1.5 line spacing, Times New Roman 12pt, justified alignment, 1.27 cm first-line indent.
  - **Headings**: Deep Academic Blue (`#1F4E78`), 16pt/14pt/12pt bold, left-aligned with page breaks before chapters.
  - **Special Titles**: Center-aligned 16pt bold for *Table of Contents*, *References*, *Index*, *Abstract*, *About the Author*, and *MCQ Headings*.
- **Title Page & Author**:
  - Main author name formatted on Front Page alone (20pt Bold Centered).
  - Page break before *About the Author* bio section.
- **Dual-Sided Footer**:
  - **Left**: Author Name & Book Title (`Author | Title`).
  - **Right**: Dynamic Word `PAGE` field (right-aligned via tab stops).
- **Interactive MCQ Normalization**:
  - MCQ questions automatically converted to Normal Sentence Case (preserving acronyms like `AIOps`, `CDN`, `WAF`, `ZTNA`).
  - Option prefixes automatically capitalized (`A)`, `B)`, `C)`, `D)`).
- **Auto-Tables & Bulleting**:
  - Table of Contents and Index entries rendered into clean 2-column tables.
  - Dash/hyphen list items converted to standardized bullet points (`•`).

---

## 🏗️ System Architecture

```
                                  ┌───────────────────────────────┐
                                  │      React + Vite Frontend     │
                                  │    (http://localhost:3000)    │
                                  └───────────────┬───────────────┘
                                                  │ HTTP / API (Proxy)
                                                  ▼
                                  ┌───────────────────────────────┐
                                  │       Flask API Server        │
                                  │    (http://localhost:5000)    │
                                  └───────────────┬───────────────┘
                                                  │
                 ┌────────────────────────────────┴────────────────────────────────┐
                 ▼                                 ▼                               ▼
       ┌───────────────────┐             ┌───────────────────┐           ┌───────────────────┐
       │   DocxParser      │             │StructureRecognizer│           │  DocxGenerator    │
       │ (Element Extract) │ ──────────► │(ML + Rule Engine) │ ────────► │(DocX Formatting)  │
       └───────────────────┘             └───────────────────┘           └───────────────────┘
```

---

## 📁 Project Structure

```
.
├── Backend/
│   ├── api.py                   # Flask API Server (Routes: /api/format, /api/analyze, /api/train, /api/settings)
│   ├── run.py                   # CLI entry point for format, train, and analyze commands
│   ├── requirements.txt         # Python dependencies (python-docx, scikit-learn, flask, etc.)
│   ├── src/
│   │   ├── config.py            # Central ElementType enum & FormattingConfig dataclass
│   │   ├── parser.py            # DocxParser for extracting paragraphs, tables, and inline images
│   │   ├── feature_extractor.py # Extract 25 structural features + TF-IDF vectors
│   │   ├── rule_engine.py       # Heuristic & pattern classification rules
│   │   ├── classifier.py        # RandomForestClassifier wrapper with cross-validation
│   │   ├── structure_recognizer.py # 2-pass recognizer (Rules -> ML -> Contextual Rules)
│   │   ├── formatter.py         # Paragraph & table styling logic (margins, font, spacing, blue headings)
│   │   ├── generator.py         # DocxGenerator building output document
│   │   └── gui.py               # Tkinter desktop GUI
│   ├── data/
│   │   └── training_data.py     # Synthetic & template dataset generator (~5,000 samples)
│   └── models/
│       ├── document_classifier.pkl  # Trained Random Forest model
│       └── tfidf_vectorizer.pkl     # Fitted TF-IDF vectorizer
├── Frontend/
│   ├── package.json             # Node dependencies (React 19, Vite, Tailwind CSS, Lucide)
│   ├── vite.config.ts           # Vite server configuration with API proxy to port 5000
│   └── src/
│       ├── App.tsx              # Main React application layout & navigation
│       ├── components/
│       │   ├── FormatView.tsx   # Manuscript upload & auto-download UI
│       │   ├── AnalyzeView.tsx  # Interactive structure classification inspector
│       │   ├── TrainView.tsx    # One-click ML model retraining panel
│       │   ├── SettingsPanel.tsx# Dynamic typography & margin preferences
│       │   └── Sidebar.tsx      # Sidebar navigation
│       └── types.ts             # TypeScript definitions
├── start_backend.bat            # One-click script to start Flask server
└── start_frontend.bat           # One-click script to start React Vite frontend
```

---

## ⚡ Quick Start & Installation

### Prerequisites
- **Python 3.10+** installed
- **Node.js 18+** installed

---

### Step 1: Automated Offline Launch (Recommended)

1. **Start the Backend API Server**:
   Double-click `start_backend.bat` or run:
   ```cmd
   .\start_backend.bat
   ```
   *(Server starts at `http://localhost:5000`)*

2. **Start the Frontend Web App**:
   Double-click `start_frontend.bat` or run:
   ```cmd
   .\start_frontend.bat
   ```
   *(UI opens at `http://localhost:3000`)*

---

### Step 2: Manual Installation (Optional)

#### Backend Setup
```bash
cd Backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
python api.py
```

#### Frontend Setup
```bash
cd Frontend
npm install
npm run dev
```

---

## 💻 Command Line Interface (CLI) Usage

You can also run the formatting engine directly from the command line without the web interface:

```bash
# Format a manuscript
python run.py input_manuscript.docx formatted_output.docx

# Retrain the ML model
python run.py --train

# Analyze document structure without saving
python run.py --analyze input_manuscript.docx
```

---

## 🔌 API Endpoints Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Health check and model status |
| `POST` | `/api/format` | Upload `.docx` file, receive formatted `.docx` download |
| `POST` | `/api/analyze` | Upload `.docx` file, receive JSON list of element classifications |
| `POST` | `/api/train` | Retrain ML model and return accuracy metrics |
| `GET` | `/api/settings` | Retrieve current formatting configuration |
| `POST` | `/api/settings` | Update font name, line spacing, or margins |

---

## 📄 License

This project is licensed under the **MIT License**.

```text
MIT License

Copyright (c) 2026 Mohamed Aashik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
