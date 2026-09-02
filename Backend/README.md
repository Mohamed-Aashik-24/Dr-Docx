# Dr Docx

Dr Docx is an ML-based offline DOCX-to-publication formatting system. It automatically parses raw `.docx` files, classifies document elements (like headings, body text, figures, tables) using machine learning and heuristic rules, and applies publication-standard formatting.

## Features
- Parse DOCX files and extract text, images, and tables.
- Machine Learning classification of document elements.
- Rule-based heuristic fallback for high confidence elements.
- Applies standard publication formatting automatically.
- Completely offline operation (no internet, no APIs, no LLMs).

## Installation

```bash
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

## Usage

### CLI
```bash
python -m src.main input.docx output.docx
```

### Supported Element Types
| Element Type | Description |
|---|---|
| TITLE | Document title |
| AUTHOR | Author names and affiliations |
| CHAPTER_HEADING | Main chapter headings |
| SECTION_HEADING | Section headings (e.g., 1.1) |
| SUBSECTION_HEADING | Subsection headings (e.g., 1.1.1) |
| BODY | Standard body text |
| FIGURE_CAPTION | Captions for figures |
| TABLE_CAPTION | Captions for tables |
| REFERENCE_HEADING | Heading for references section |
| REFERENCE_ENTRY | Individual reference entries |
| LIST_ITEM | Bulleted or numbered list items |
| TABLE | Tables |
| FIGURE | Images and figures |
| BLANK | Empty lines |

## Formatting Specification
- **Font:** Times New Roman
- **Line Spacing:** 1.5
- **Margins:** Top/Bottom: 1.52cm, Left: 1.97cm, Right: 1.96cm
- **Body Font Size:** 12pt
- **Heading 1 Font Size:** 16pt
- **Heading 2 Font Size:** 14pt

## Architecture
- `src/parser.py`: Parses raw DOCX files, extracting runs, styles, images, and tables.
- `src/rule_engine.py`: Applies robust heuristics based on regex to classify clear-cut document parts (captions, headings, references).
- `src/config.py`: Single source of truth for element types, models paths, and default styles.

## How the ML Works
For elements not caught by the `RuleEngine`, the system uses `scikit-learn`. Text elements are converted using a pre-trained TF-IDF vectorizer and evaluated with an offline classification model. Predictions surpassing confidence thresholds apply the formatting corresponding to their classified label.
