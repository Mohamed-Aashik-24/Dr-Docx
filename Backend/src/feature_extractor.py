import re
import numpy as np
from typing import List, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

class FeatureExtractor:
    FEATURE_NAMES = [
        "word_count", "char_count", "uppercase_ratio", "is_all_caps",
        "starts_with_number", "matches_chapter_pattern", "matches_section_pattern",
        "matches_subsection_pattern", "matches_figure_pattern", "matches_table_pattern",
        "contains_year", "contains_citation_bracket", "ends_with_period",
        "sentence_count", "avg_word_length", "is_bold", "is_italic",
        "font_size_normalized", "is_empty", "position_ratio", "starts_with_bullet",
        "line_count", "contains_et_al", "matches_reference_pattern", "contains_email"
    ]

    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=200, stop_words='english')
        self.is_fitted = False

    def extract_structural_features(self, text: str, is_bold: bool = False, is_italic: bool = False, font_size: Optional[float] = None, position_ratio: float = 0.5) -> np.ndarray:
        word_count = len(text.split())
        char_count = len(text)
        uppercase_ratio = sum(1 for c in text if c.isupper()) / max(char_count, 1)
        
        has_alpha = any(c.isalpha() for c in text)
        is_all_caps = 1.0 if text.upper() == text and text.strip() != '' and has_alpha else 0.0
        
        starts_with_number = 1.0 if re.match(r'^\s*\d', text) else 0.0
        matches_chapter_pattern = 1.0 if re.match(r'^\s*(CHAPTER|Chapter)\s+\d+', text) else 0.0
        matches_section_pattern = 1.0 if re.match(r'^\s*\d+\.\d+\s+\w', text) else 0.0
        matches_subsection_pattern = 1.0 if re.match(r'^\s*\d+\.\d+\.\d+\s+\w', text) else 0.0
        matches_figure_pattern = 1.0 if re.match(r'^\s*(Figure|Fig\.?)\s+\d+', text, re.I) else 0.0
        matches_table_pattern = 1.0 if re.match(r'^\s*(Table|Tbl\.?)\s+\d+', text, re.I) else 0.0
        
        contains_year = 1.0 if re.search(r'\b(19|20)\d{2}\b', text) else 0.0
        contains_citation_bracket = 1.0 if re.search(r'\[\d+\]', text) else 0.0
        ends_with_period = 1.0 if text.strip().endswith('.') else 0.0
        
        sentence_count = sum(text.count(sep) for sep in ['. ', '? ', '! ']) + 1 if text.strip() else 0
        words = text.split()
        avg_word_length = sum(len(w) for w in words) / max(len(words), 1)
        
        bold_feat = 1.0 if is_bold else 0.0
        italic_feat = 1.0 if is_italic else 0.0
        font_size_normalized = font_size / 20.0 if font_size else 0.5
        is_empty = 1.0 if text.strip() == '' else 0.0
        
        starts_with_bullet = 1.0 if re.match(r'^\s*([•\-*▪]|\d+\.|[a-zA-Z]\)|[ivx]+\.)', text) else 0.0
        line_count = text.count('\n') + 1
        
        contains_et_al = 1.0 if 'et al' in text.lower() else 0.0
        
        is_ref = re.match(r'^\s*\[\d+\]', text) is not None or (contains_year > 0 and (contains_et_al > 0 or contains_citation_bracket > 0))
        matches_reference_pattern = 1.0 if is_ref else 0.0
        contains_email = 1.0 if '@' in text else 0.0

        features = [
            word_count, char_count, uppercase_ratio, is_all_caps, starts_with_number,
            matches_chapter_pattern, matches_section_pattern, matches_subsection_pattern,
            matches_figure_pattern, matches_table_pattern, contains_year,
            contains_citation_bracket, ends_with_period, sentence_count, avg_word_length,
            bold_feat, italic_feat, font_size_normalized, is_empty, position_ratio,
            starts_with_bullet, line_count, contains_et_al, matches_reference_pattern, contains_email
        ]
        return np.array(features, dtype=float)

    def fit_tfidf(self, texts: List[str]) -> None:
        self.vectorizer.fit(texts)
        self.is_fitted = True

    def transform_tfidf(self, text: str) -> np.ndarray:
        if not self.is_fitted:
            return np.zeros(200, dtype=float)
        return self.vectorizer.transform([text]).toarray()[0]

    def get_feature_vector(self, text: str, is_bold: bool = False, is_italic: bool = False, font_size: Optional[float] = None, position_ratio: float = 0.5) -> np.ndarray:
        struct_feats = self.extract_structural_features(text, is_bold, is_italic, font_size, position_ratio)
        if self.is_fitted:
            tfidf_feats = self.transform_tfidf(text)
            return np.concatenate([struct_feats, tfidf_feats])
        return struct_feats

    def get_feature_vectors_batch(self, items: List[dict]) -> np.ndarray:
        struct_list = []
        texts = []
        for item in items:
            text = item.get('text', '')
            texts.append(text)
            struct_list.append(self.extract_structural_features(
                text=text,
                is_bold=item.get('is_bold', False),
                is_italic=item.get('is_italic', False),
                font_size=item.get('font_size'),
                position_ratio=item.get('position_ratio', 0.5)
            ))
        struct_arr = np.array(struct_list, dtype=float)
        if self.is_fitted:
            tfidf_arr = self.vectorizer.transform(texts).toarray()
            return np.hstack([struct_arr, tfidf_arr])
        return struct_arr

    def save_vectorizer(self, path: str) -> None:
        joblib.dump(self.vectorizer, path)

    def load_vectorizer(self, path: str) -> None:
        self.vectorizer = joblib.load(path)
        self.is_fitted = True
