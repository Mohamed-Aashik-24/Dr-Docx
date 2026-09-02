#!/usr/bin/env python
"""Simple runner for the DOCX formatter."""
import sys
import os

def main():
    if len(sys.argv) < 2:
        print('Usage: python run.py <input.docx> [output.docx]')
        print('       python run.py --train')
        print('       python run.py --analyze <input.docx>')
        sys.exit(1)
    
    if sys.argv[1] == '--train':
        from src.classifier import DocumentClassifier
        classifier = DocumentClassifier()
        results = classifier.train()
        acc = results.get('accuracy', 0.0) if isinstance(results, dict) else 0.0
        print(f"Training complete! Accuracy: {acc:.4f}")
        return
    
    if sys.argv[1] == '--analyze':
        if len(sys.argv) < 3:
            print('Usage: python run.py --analyze <input.docx>')
            sys.exit(1)
        from src.parser import DocxParser
        from src.structure_recognizer import StructureRecognizer
        parser = DocxParser()
        recognizer = StructureRecognizer()
        doc = parser.parse(sys.argv[2])
        results = recognizer.recognize(doc)
        for r in results:
            print(f'[{r.element_type.value:20s}] (conf={r.confidence:.2f}, src={r.source}) {getattr(r.element, "text", "[TABLE]")[:80]}')
        return
    
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else input_path.replace('.docx', '_formatted.docx')
    
    from src.parser import DocxParser
    from src.structure_recognizer import StructureRecognizer
    from src.generator import DocxGenerator
    import time
    
    print(f'Processing: {input_path}')
    start = time.time()
    
    parser = DocxParser()
    doc = parser.parse(input_path)
    print(f'  Parsed {len(doc.elements)} elements')
    
    recognizer = StructureRecognizer()
    classified = recognizer.recognize(doc)
    print(f'  Classified {len(classified)} elements')
    
    generator = DocxGenerator()
    generator.generate(classified, output_path)
    
    elapsed = time.time() - start
    print(f'  Done in {elapsed:.2f}s -> {output_path}')

if __name__ == '__main__':
    main()
