import pathlib
from enum import Enum
from dataclasses import dataclass
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

class ElementType(Enum):
    """Document element types for classification."""
    TITLE = "title"
    AUTHOR = "author"
    CHAPTER_HEADING = "chapter_heading"
    SECTION_HEADING = "section_heading"
    SUBSECTION_HEADING = "subsection_heading"
    BODY = "body"
    FIGURE_CAPTION = "figure_caption"
    TABLE_CAPTION = "table_caption"
    REFERENCE_HEADING = "reference_heading"
    REFERENCE_ENTRY = "reference_entry"
    LIST_ITEM = "list_item"
    MCQ_HEADING = "mcq_heading"
    MCQ_QUESTION = "mcq_question"
    MCQ_OPTION = "mcq_option"
    MCQ_ANSWER = "mcq_answer"
    TOC_HEADING = "toc_heading"
    TOC_ENTRY = "toc_entry"
    INDEX_HEADING = "index_heading"
    INDEX_ENTRY = "index_entry"
    ABSTRACT_HEADING = "abstract_heading"
    ABOUT_AUTHOR_HEADING = "about_author_heading"
    TABLE = "table"
    FIGURE = "figure"
    BLANK = "blank"

@dataclass
class FormattingConfig:
    font_name: str = 'Times New Roman'
    body_font_size = Pt(12)
    heading1_font_size = Pt(16)       # Heading 1: 16 pt, Bold
    subheading_font_size = Pt(12)     # Subheading: 12 pt, Bold
    heading2_font_size = Pt(12)       # Section Heading: 12 pt, Bold
    heading3_font_size = Pt(12)       # Subsection Heading: 12 pt, Bold
    caption_font_size = Pt(10)
    reference_font_size = Pt(10)
    line_spacing: float = 1.5
    first_line_indent = Cm(1.27)
    top_margin = Cm(1.52)
    bottom_margin = Cm(1.52)
    left_margin = Cm(1.97)
    right_margin = Cm(1.96)
    text_color = RGBColor(0, 0, 0)
    body_alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    heading_alignment = WD_ALIGN_PARAGRAPH.LEFT
    caption_alignment = WD_ALIGN_PARAGRAPH.CENTER

DEFAULT_CONFIG = FormattingConfig()

PROJECT_ROOT = pathlib.Path(__file__).parent.parent
MODEL_DIR = PROJECT_ROOT / 'models'
MODEL_PATH = MODEL_DIR / 'document_classifier.pkl'
VECTORIZER_PATH = MODEL_DIR / 'tfidf_vectorizer.pkl'
CONFIDENCE_THRESHOLD = 0.6
