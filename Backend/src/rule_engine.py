import re
from typing import Optional, Tuple
from src.config import ElementType
from src.parser import ParsedElement

class RuleEngine:
    def _get_heading_keywords(self) -> set:
        return {
            'INTRODUCTION', 'CONCLUSION', 'ABSTRACT', 'METHODOLOGY',
            'RESULTS', 'DISCUSSION', 'REFERENCES', 'BACKGROUND',
            'SUMMARY', 'ACKNOWLEDGEMENTS', 'APPENDIX', 'CONTENTS', 'INDEX',
            'ABOUT THE AUTHOR', 'PREFACE', 'FOREWORD'
        }

    def classify(self, element: ParsedElement, position_ratio: float) -> Optional[Tuple[ElementType, float]]:
        text = element.text
        stripped_text = text.strip()
        words = stripped_text.split()
        style_name = (element.style_name or '').lower()
        
        # Blank
        if not stripped_text:
            return (ElementType.BLANK, 1.0)

        # About the Author Heading
        if re.match(r'^\s*(About\s+the\s+Author|About\s+the\s+Authors|Author\s+Bio|AUTHOR\s+BIO)\s*$', stripped_text, re.IGNORECASE):
            return (ElementType.ABOUT_AUTHOR_HEADING, 0.98)

        # Abstract Heading
        if re.match(r'^\s*(Abstract|ABSTRACT)\s*$', stripped_text):
            return (ElementType.ABSTRACT_HEADING, 0.98)

        # Table of Contents Heading
        if re.match(r'^\s*(Table\s+of\s+Contents|Contents)\s*$', stripped_text, re.IGNORECASE):
            return (ElementType.TOC_HEADING, 0.98)

        # Index Heading
        if re.match(r'^\s*(INDEX|Index|Subject\s+Index)\s*$', stripped_text):
            return (ElementType.INDEX_HEADING, 0.95)

        # Reference Heading
        if re.match(r'^\s*(References?|Bibliography|Works\s+Cited)\s*$', stripped_text, re.IGNORECASE):
            return (ElementType.REFERENCE_HEADING, 0.95)
            
        # TOC / Index page number entry (e.g. "Chapter 1\t15" or "1.  The Dawn...\t12")
        if '\t' in text and re.search(r'\t\d+\s*$', text):
            return (ElementType.TOC_ENTRY, 0.98)

        # Word Paragraph Style Explicit Rules (Heading 1, Heading 2, Heading 3)
        if 'heading 1' in style_name:
            if re.match(r'^\s*(Table\s+of\s+Contents|Contents)', stripped_text, re.I):
                return (ElementType.TOC_HEADING, 0.98)
            return (ElementType.CHAPTER_HEADING, 0.95)
        if 'heading 2' in style_name:
            return (ElementType.SECTION_HEADING, 0.95)
        if 'heading 3' in style_name:
            return (ElementType.SUBSECTION_HEADING, 0.95)

        # Explicit Chapter heading with number/prefix
        if re.match(r'^\s*(CHAPTER|Chapter)\s+\d+', text) or \
           re.match(r'^\s*(CHAPTER|Chapter)\s+(ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN)', text):
            return (ElementType.CHAPTER_HEADING, 0.95)
            
        # All-caps or title-case short heading keywords
        if element.is_all_caps and len(words) <= 8:
            if any(kw in stripped_text.upper() for kw in self._get_heading_keywords()):
                return (ElementType.CHAPTER_HEADING, 0.90)
                
        # Numbered Section heading (e.g., "1.1 Section")
        if re.match(r'^\s*\d+\.\d+\s+\w', text):
            return (ElementType.SECTION_HEADING, 0.95)
            
        # Numbered Subsection heading (e.g., "1.1.1 Subsection")
        if re.match(r'^\s*\d+\.\d+\.\d+\s+\w', text):
            return (ElementType.SUBSECTION_HEADING, 0.95)
            
        # MCQ Heading
        if re.search(r'^\s*(Multiple\s+Choice\s+Questions?|MCQs?|Review\s+Questions?)\s*(\(MCQs?\))?\s*$', text, re.IGNORECASE):
            return (ElementType.MCQ_HEADING, 0.98)
            
        # MCQ Answer
        if re.match(r'^\s*Answer\s*:\s*[a-dA-D]', text, re.IGNORECASE):
            return (ElementType.MCQ_ANSWER, 0.98)
            
        # MCQ Option
        if re.match(r'^\s*([a-d]\)|\([a-d]\)|[A-D]\.)\s', text):
            return (ElementType.MCQ_OPTION, 0.92)

        # Figure caption
        if re.match(r'^\s*(Figure|Fig\.?)\s+\d+', text):
            return (ElementType.FIGURE_CAPTION, 0.95)
            
        # Table caption
        if re.match(r'^\s*(Table|Tbl\.?)\s+\d+', text):
            return (ElementType.TABLE_CAPTION, 0.95)
            
        # Reference entry
        if re.match(r'^\s*\[\d+\]', text) or (re.search(r'(19|20)\d{2}', text) and len(words) > 5 and ('et al' in text.lower() or 'journal' in text.lower() or 'pp.' in text.lower() or 'vol.' in text.lower())):
            return (ElementType.REFERENCE_ENTRY, 0.90)
            
        # List item
        if text.lstrip().startswith(('•', '-', '*', '▪', '–')) or \
           (re.match(r'^\s*(\d+\.|[a-z]\)|[ivx]+\.)\s', text) and len(words) < 30 and not re.search(r'^\s*\d+\.\s+(Which|What|How|Why|In |The )', text, re.IGNORECASE)):
            return (ElementType.LIST_ITEM, 0.9)
            
        # Author
        if position_ratio < 0.05 and ('@' in text or re.search(r'Department|University|Institute|College|Author:|Published by|Engineer|Scientist|Professor', text, re.IGNORECASE)):
            return (ElementType.AUTHOR, 0.85)
            
        # Title
        if position_ratio < 0.02 and (element.is_bold or element.is_all_caps or style_name == 'title') and 3 <= len(words) <= 25:
            return (ElementType.TITLE, 0.85)

        # Unnumbered Chapter/Section Heading heuristic:
        # Bold or All Caps, 2 <= word_count <= 10, no ending punctuation (., ?, !)
        if position_ratio > 0.03 and len(words) >= 2 and len(words) <= 10 and (element.is_bold or element.is_all_caps):
            if not stripped_text.endswith(('.', '?', '!', ':', ';', ',')):
                return (ElementType.CHAPTER_HEADING, 0.85)

        return None
