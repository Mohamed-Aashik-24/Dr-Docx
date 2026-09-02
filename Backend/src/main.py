import argparse
import sys
import os
import time
from pathlib import Path
from src.parser import DocxParser
from src.classifier import DocumentClassifier
from src.structure_recognizer import StructureRecognizer
from src.generator import DocxGenerator
from src.config import ElementType

def main():
    parser = argparse.ArgumentParser(description='ML-Based DOCX Formatter')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # format command
    fmt_parser = subparsers.add_parser('format', help='Format a DOCX file')
    fmt_parser.add_argument('input', help='Input DOCX file path')
    fmt_parser.add_argument('-o', '--output', help='Output DOCX file path')
    
    # train command
    subparsers.add_parser('train', help='Train the ML model')
    
    # analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze document structure')
    analyze_parser.add_argument('input', help='Input DOCX file path')
    
    args = parser.parse_args()
    
    if args.command == 'format':
        input_path = args.input
        output_path = args.output or input_path.replace('.docx', '_formatted.docx')
        
        print(f'Processing: {input_path}')
        start = time.time()
        
        parser_obj = DocxParser()
        doc = parser_obj.parse(input_path)
        print(f'  Parsed {len(doc.elements)} elements')
        
        recognizer = StructureRecognizer()
        classified = recognizer.recognize(doc)
        print(f'  Classified {len(classified)} elements')
        
        counts = {}
        for ce in classified:
            counts[ce.element_type] = counts.get(ce.element_type, 0) + 1
        for etype, count in counts.items():
            print(f'    - {etype.value}: {count}')
        
        generator = DocxGenerator()
        generator.generate(classified, output_path)
        
        elapsed = time.time() - start
        print(f'  Done in {elapsed:.2f}s -> {output_path}')
        
    elif args.command == 'train':
        classifier = DocumentClassifier()
        results = classifier.train()
        print(f"Training complete! Results: {results}")
        
    elif args.command == 'analyze':
        parser_obj = DocxParser()
        doc = parser_obj.parse(args.input)
        recognizer = StructureRecognizer()
        classified = recognizer.recognize(doc)
        
        for r in classified:
            text = getattr(r.element, "text", "[TABLE]")[:80]
            print(f'[{r.element_type.value:20s}] (conf={r.confidence:.2f}, src={r.source}) {text}')
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
