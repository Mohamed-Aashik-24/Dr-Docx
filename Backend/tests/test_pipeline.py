import unittest
import os
import sys
import tempfile
import numpy as np
import torch

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import ElementType, FormattingConfig, DEFAULT_CONFIG
from src.feature_extractor import FeatureExtractor
from src.rule_engine import RuleEngine
from data.training_data import generate_training_data
from src.neural_model import DocumentElementNetwork
from src.classifier import DocumentClassifier
from src.parser import DocxParser, ParsedElement, ParsedTable
from src.structure_recognizer import StructureRecognizer
from src.formatter import DocumentFormatter
from src.generator import DocxGenerator


class TestConfig(unittest.TestCase):
    def test_element_type_enum(self):
        self.assertEqual(ElementType.TITLE.value, "title")
        self.assertEqual(ElementType.CHAPTER_HEADING.value, "chapter_heading")
        self.assertEqual(ElementType.BODY.value, "body")
        self.assertEqual(ElementType.FIGURE_CAPTION.value, "figure_caption")
        
    def test_formatting_config_defaults(self):
        config = FormattingConfig()
        self.assertEqual(config.font_name, "Times New Roman")
        self.assertEqual(config.line_spacing, 1.5)


class TestFeatureExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = FeatureExtractor()
        
    def test_chapter_all_caps(self):
        features = self.extractor.extract_structural_features("CHAPTER 1", is_bold=True)
        self.assertEqual(features[3], 1.0)
        self.assertEqual(features[5], 1.0)
        
    def test_figure_pattern(self):
        features = self.extractor.extract_structural_features("Figure 1: Test architecture", is_italic=True)
        self.assertEqual(features[8], 1.0)
        
    def test_tfidf(self):
        texts = ["CHAPTER 1 Introduction", "Figure 1 Architecture", "Body text content for study"]
        self.extractor.fit_tfidf(texts)
        vec = self.extractor.get_feature_vector("CHAPTER 2 Methodology", is_bold=True)
        self.assertIsInstance(vec, np.ndarray)
        self.assertGreater(len(vec), 25)


class TestRuleEngine(unittest.TestCase):
    def setUp(self):
        self.engine = RuleEngine()
        
    def test_chapter_heading(self):
        elem = ParsedElement(text="CHAPTER 1", index=5, is_bold=True)
        res = self.engine.classify(elem, 0.1)
        self.assertIsNotNone(res)
        self.assertEqual(res[0], ElementType.CHAPTER_HEADING)
        
    def test_section_heading(self):
        elem = ParsedElement(text="1.1 Introduction", index=6, is_bold=True)
        res = self.engine.classify(elem, 0.1)
        self.assertIsNotNone(res)
        self.assertEqual(res[0], ElementType.SECTION_HEADING)
        
    def test_figure_caption(self):
        elem = ParsedElement(text="Figure 1: Proposed Architecture", index=15, is_italic=True)
        res = self.engine.classify(elem, 0.3)
        self.assertIsNotNone(res)
        self.assertEqual(res[0], ElementType.FIGURE_CAPTION)
        
    def test_blank(self):
        elem1 = ParsedElement(text="", index=0)
        elem2 = ParsedElement(text="   ", index=1)
        self.assertEqual(self.engine.classify(elem1, 0.0)[0], ElementType.BLANK)
        self.assertEqual(self.engine.classify(elem2, 0.0)[0], ElementType.BLANK)
        
    def test_body(self):
        elem = ParsedElement(text="This is standard academic body text discussing the experiments.", index=10)
        res = self.engine.classify(elem, 0.5)
        self.assertIsNone(res)


class TestTrainingData(unittest.TestCase):
    def test_generate_data(self):
        data = generate_training_data()
        self.assertGreaterEqual(len(data), 3000)
        labels = [item[2] for item in data]
        unique_labels = set(labels)
        self.assertIn("chapter_heading", unique_labels)
        self.assertIn("section_heading", unique_labels)
        self.assertIn("body", unique_labels)
        self.assertIn("figure_caption", unique_labels)
        self.assertIn("reference_entry", unique_labels)


class TestNeuralModel(unittest.TestCase):
    def test_construction_and_forward(self):
        input_size = 225
        num_classes = 15
        model = DocumentElementNetwork(input_size=input_size, num_classes=num_classes)
        x = torch.randn(8, input_size)
        logits = model(x)
        self.assertEqual(logits.shape, (8, num_classes))


class TestDocumentClassifier(unittest.TestCase):
    def test_train_and_predict(self):
        # Force CPU for test reproducibility
        classifier = DocumentClassifier(device="cpu")
        res = classifier.train(epochs=3, batch_size=32)
        
        self.assertIn("accuracy", res)
        self.assertIn("validation_accuracy", res)
        self.assertIn("macro_f1", res)
        self.assertIn("num_samples", res)
        self.assertIn("num_features", res)
        self.assertEqual(res["model_type"], "PyTorch MLP")
        self.assertEqual(res["device"], "cpu")
        self.assertTrue(classifier.is_trained())

        # Test single item prediction
        elem_type, conf = classifier.predict("CHAPTER 1 Introduction", is_bold=True, font_size=16.0)
        self.assertIsInstance(elem_type, ElementType)
        self.assertIsInstance(conf, float)
        self.assertGreaterEqual(conf, 0.0)
        self.assertLessEqual(conf, 1.0)

        # Test batch prediction
        items = [
            {"text": "1.1 Background", "is_bold": True, "font_size": 14.0, "position_ratio": 0.1},
            {"text": "This is a body paragraph.", "is_bold": False, "font_size": 12.0, "position_ratio": 0.5}
        ]
        batch_results = classifier.predict_batch(items)
        self.assertEqual(len(batch_results), 2)
        for t, c in batch_results:
            self.assertIsInstance(t, ElementType)
            self.assertIsInstance(c, float)
            self.assertGreaterEqual(c, 0.0)
            self.assertLessEqual(c, 1.0)

        # Test save and load
        save_res = classifier.load()
        self.assertTrue(save_res)
        self.assertTrue(classifier.is_trained())

    def test_missing_model_file_load(self):
        classifier = DocumentClassifier(device="cpu")
        # Artificially test with non-existent path
        import src.config as cfg
        original_pt = cfg.PYTORCH_MODEL_PATH
        cfg.PYTORCH_MODEL_PATH = cfg.MODEL_DIR / "non_existent_model_file.pt"
        try:
            res = classifier.load()
            self.assertFalse(res)
            self.assertFalse(classifier.is_trained())
        finally:
            cfg.PYTORCH_MODEL_PATH = original_pt


class TestEndToEnd(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.input_path = os.path.join(self.temp_dir.name, "input.docx")
        self.output_path = os.path.join(self.temp_dir.name, "output.docx")
        self._create_test_docx(self.input_path)
        
    def tearDown(self):
        self.temp_dir.cleanup()
        
    def _create_test_docx(self, path):
        from docx import Document
        doc = Document()
        doc.add_paragraph('Test Research Paper Title')
        doc.add_paragraph('John Doe, University of Testing')
        doc.add_paragraph('CHAPTER 1')
        doc.add_paragraph('Introduction')
        doc.add_paragraph('This is a body paragraph with enough text to be classified as body content. ' * 5)
        doc.add_paragraph('1.1 Background')
        doc.add_paragraph('This section provides background information. ' * 8)
        doc.add_paragraph('Figure 1: Test Architecture Diagram')
        doc.add_paragraph('Table 1: Comparison Results')
        table = doc.add_table(rows=3, cols=3)
        for i, row in enumerate(table.rows):
            for j, cell in enumerate(row.cells):
                cell.text = f'Cell {i},{j}'
        doc.add_paragraph('References')
        doc.add_paragraph('[1] Smith, J. (2024). Test Paper. Journal of Testing, 1(1), 1-10.')
        doc.add_paragraph('[2] Doe, A. (2023). Another Paper. Conference on Testing, 20-25.')
        doc.save(path)
        
    def test_full_pipeline(self):
        # Train classifier with small epochs for fast unit test
        classifier = DocumentClassifier(device="cpu")
        classifier.train(epochs=3, batch_size=32)
        
        # Parse
        parser = DocxParser()
        parsed_doc = parser.parse(self.input_path)
        self.assertGreater(len(parsed_doc.elements), 5)
        
        # Recognize
        recognizer = StructureRecognizer()
        classified = recognizer.recognize(parsed_doc)
        self.assertEqual(len(classified), len(parsed_doc.elements))
        
        # Generate
        generator = DocxGenerator()
        generator.generate(classified, self.output_path)
        
        self.assertTrue(os.path.exists(self.output_path))
        from docx import Document
        out_doc = Document(self.output_path)
        self.assertGreater(len(out_doc.paragraphs), 0)

    def test_blank_space_suppression(self):
        # Create doc with 5 consecutive blank lines
        blank_doc_path = os.path.join(self.temp_dir.name, "blank_input.docx")
        blank_out_path = os.path.join(self.temp_dir.name, "blank_output.docx")
        
        from docx import Document
        doc = Document()
        doc.add_paragraph("Paragraph 1")
        doc.add_paragraph("")
        doc.add_paragraph("   ")
        doc.add_paragraph("\n")
        doc.add_paragraph("\t")
        doc.add_paragraph("Paragraph 2")
        doc.save(blank_doc_path)
        
        parser = DocxParser()
        parsed_doc = parser.parse(blank_doc_path)
        recognizer = StructureRecognizer()
        classified = recognizer.recognize(parsed_doc)
        
        generator = DocxGenerator()
        generator.generate(classified, blank_out_path)
        
        out_doc = Document(blank_out_path)
        # Should have far fewer paragraphs than original because 4 blanks are collapsed
        self.assertLess(len(out_doc.paragraphs), len(parsed_doc.elements))


if __name__ == '__main__':
    unittest.main()
