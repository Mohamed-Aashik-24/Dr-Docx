from dataclasses import dataclass
from typing import List, Union, Optional
import re
from src.config import ElementType, CONFIDENCE_THRESHOLD
from src.parser import ParsedElement, ParsedTable, ParsedDocument
from src.classifier import DocumentClassifier
from src.rule_engine import RuleEngine

@dataclass
class ClassifiedElement:
    element: Union[ParsedElement, ParsedTable]
    element_type: ElementType
    confidence: float
    source: str  # 'rule', 'ml', 'context'

class StructureRecognizer:
    def __init__(self):
        self.classifier = DocumentClassifier()
        self.classifier.load()
        self.rule_engine = RuleEngine()

    def recognize(self, document: ParsedDocument) -> List[ClassifiedElement]:
        classified: List[Optional[ClassifiedElement]] = [None] * len(document.elements)
        total_elements = len(document.elements)
        
        ml_pending_indices = []
        ml_pending_items = []
        
        # First pass: Rules and identify items needing ML
        for i, element in enumerate(document.elements):
            if isinstance(element, ParsedTable):
                classified[i] = ClassifiedElement(element, ElementType.TABLE, 1.0, 'rule')
                continue
                
            position_ratio = i / total_elements if total_elements > 0 else 0.0
            
            # Rule engine check
            rule_result = self.rule_engine.classify(element, position_ratio)
            if rule_result and rule_result[1] >= CONFIDENCE_THRESHOLD:
                classified[i] = ClassifiedElement(element, rule_result[0], rule_result[1], 'rule')
            else:
                ml_pending_indices.append(i)
                ml_pending_items.append({
                    'text': element.text,
                    'is_bold': element.is_bold,
                    'is_italic': element.is_italic,
                    'font_size': element.font_size or 12.0,
                    'position_ratio': position_ratio
                })
                
        # Batch ML inference
        if ml_pending_items:
            ml_results = self.classifier.predict_batch(ml_pending_items)
            for idx, (elem_type, conf) in zip(ml_pending_indices, ml_results):
                element = document.elements[idx]
                if conf < CONFIDENCE_THRESHOLD:
                    classified[idx] = ClassifiedElement(element, ElementType.BODY, conf, 'ml')
                else:
                    classified[idx] = ClassifiedElement(element, elem_type, conf, 'ml')
                    
        return self._apply_context_rules(classified)

    def _apply_context_rules(self, classified: List[ClassifiedElement]) -> List[ClassifiedElement]:
        title_found = False
        in_references = False
        in_mcq_block = False
        in_toc_block = False
        
        for i, ce in enumerate(classified):
            if isinstance(ce.element, ParsedTable):
                in_mcq_block = False
                continue
                
            text = getattr(ce.element, 'text', '').strip()
            if not text and not getattr(ce.element, 'has_image', False):
                continue
                
            # FIGURE check
            if getattr(ce.element, 'has_image', False):
                ce.element_type = ElementType.FIGURE
                ce.source = 'context'
                in_mcq_block = False
                continue
                
            # Chapter Heading resets blocks
            if ce.element_type == ElementType.CHAPTER_HEADING:
                in_mcq_block = False
                in_toc_block = False
                in_references = False
                continue
                
            # Table of Contents / Index check
            if ce.element_type in (ElementType.TOC_HEADING, ElementType.INDEX_HEADING):
                in_toc_block = True
                in_mcq_block = False
                continue
                
            if in_toc_block:
                if ce.element_type in (ElementType.CHAPTER_HEADING, ElementType.SECTION_HEADING):
                    in_toc_block = False
                else:
                    ce.element_type = ElementType.TOC_ENTRY
                    ce.source = 'context'
                    continue

            # First non-blank text element -> TITLE
            if not title_found and ce.element_type != ElementType.CHAPTER_HEADING:
                ce.element_type = ElementType.TITLE
                ce.source = 'context'
                title_found = True
                
                # Check for AUTHORS immediately after TITLE
                j = i + 1
                while j < len(classified) and j < i + 6:
                    next_ce = classified[j]
                    if not isinstance(next_ce.element, ParsedTable) and getattr(next_ce.element, 'text', '').strip():
                        if getattr(next_ce.element, 'index', 0) / max(len(classified), 1) < 0.05:
                            next_text = getattr(next_ce.element, 'text', '')
                            if not re.match(r'^(CHAPTER|TABLE OF CONTENTS|CONTENTS|INDEX)', next_text, re.I):
                                next_ce.element_type = ElementType.AUTHOR
                                next_ce.source = 'context'
                    j += 1
                continue
                
            # REFERENCES check
            if ce.element_type == ElementType.REFERENCE_HEADING:
                in_references = True
                in_mcq_block = False
                continue
                
            if in_references:
                ce.element_type = ElementType.REFERENCE_ENTRY
                ce.source = 'context'
                continue
                
            # MCQ Block Handling
            if ce.element_type == ElementType.MCQ_HEADING:
                in_mcq_block = True
                continue
                
            if in_mcq_block:
                if re.match(r'^\s*Answer\s*:\s*[a-dA-D]', text, re.I):
                    ce.element_type = ElementType.MCQ_ANSWER
                    ce.source = 'context'
                elif re.match(r'^\s*([a-d]\)|\([a-d]\)|[A-D]\.)\s', text) or ('\na)' in text or '\nb)' in text):
                    ce.element_type = ElementType.MCQ_OPTION
                    ce.source = 'context'
                elif re.match(r'^\s*\d+[\.\)]\s+', text):
                    ce.element_type = ElementType.MCQ_QUESTION
                    ce.source = 'context'
                continue
                
            # TABLE_CAPTION check
            if i > 0 and isinstance(classified[i-1].element, ParsedTable):
                if text.lower().startswith('table') or text.lower().startswith('tbl'):
                    ce.element_type = ElementType.TABLE_CAPTION
                    ce.source = 'context'
            elif i < len(classified) - 1 and isinstance(classified[i+1].element, ParsedTable):
                if text.lower().startswith('table') or text.lower().startswith('tbl'):
                    ce.element_type = ElementType.TABLE_CAPTION
                    ce.source = 'context'
                    
            # FIGURE_CAPTION check
            if i > 0 and classified[i-1].element_type == ElementType.FIGURE:
                if text.lower().startswith('figure') or text.lower().startswith('fig'):
                    ce.element_type = ElementType.FIGURE_CAPTION
                    ce.source = 'context'
            elif i < len(classified) - 1 and classified[i+1].element_type == ElementType.FIGURE:
                if text.lower().startswith('figure') or text.lower().startswith('fig'):
                    ce.element_type = ElementType.FIGURE_CAPTION
                    ce.source = 'context'
                    
        return classified
