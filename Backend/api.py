"""
Flask API server for the ML-Based DOCX Formatting System.
Serves endpoints consumed by the React frontend.

Endpoints:
  GET  /api/health     -> Health check
  POST /api/format     -> Upload DOCX, format it, return formatted DOCX
  POST /api/analyze    -> Upload DOCX, classify elements, return JSON
  POST /api/train      -> Retrain the ML model, return accuracy metrics
  POST /api/settings   -> Update formatting config (font, margins, spacing)
"""

from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import tempfile
import os
import sys
import time
import shutil
import io

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.config import FormattingConfig, DEFAULT_CONFIG
from src.parser import DocxParser, ParsedTable
from src.structure_recognizer import StructureRecognizer
from src.generator import DocxGenerator
from src.classifier import DocumentClassifier
from docx.shared import Pt, Cm

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:3000'])

current_config = FormattingConfig()

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'model_loaded': (
            os.path.exists(os.path.join(BASE_DIR, 'models', 'hybrid_document_model.pt'))
            or os.path.exists(os.path.join(BASE_DIR, 'models', 'document_element_model.pt'))
            or os.path.exists(os.path.join(BASE_DIR, 'models', 'document_classifier.pkl'))
        ),
    })

@app.route('/api/format', methods=['POST'])
def format_document():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded. Please select a .docx file.'}), 400

    file = request.files['file']
    if file.filename == '' or not file.filename.lower().endswith('.docx'):
        return jsonify({'error': 'Invalid file. Only .docx files are supported.'}), 400

    output_name = request.form.get('output_name', 'formatted_' + file.filename)

    temp_dir = tempfile.mkdtemp()
    input_path = os.path.join(temp_dir, file.filename)
    output_path = os.path.join(temp_dir, output_name)

    try:
        file.save(input_path)
        start_time = time.time()

        parser = DocxParser()
        parsed_doc = parser.parse(input_path)

        recognizer = StructureRecognizer()
        classified = recognizer.recognize(parsed_doc)

        generator = DocxGenerator(config=current_config)
        generator.generate(classified, output_path)

        elapsed = round(time.time() - start_time, 2)
        print(f"[API] Formatted {file.filename} -> {output_name} in {elapsed}s ({len(classified)} elements)")

        with open(output_path, 'rb') as f:
            file_bytes = io.BytesIO(f.read())

        return send_file(
            file_bytes,
            as_attachment=True,
            download_name=output_name,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

    finally:
        try:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass

@app.route('/api/analyze', methods=['POST'])
def analyze_document():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded. Please select a .docx file.'}), 400

    file = request.files['file']
    if file.filename == '' or not file.filename.lower().endswith('.docx'):
        return jsonify({'error': 'Invalid file. Only .docx files are supported.'}), 400

    temp_dir = tempfile.mkdtemp()
    input_path = os.path.join(temp_dir, file.filename)

    try:
        file.save(input_path)
        start_time = time.time()

        parser = DocxParser()
        parsed_doc = parser.parse(input_path)

        recognizer = StructureRecognizer()
        classified = recognizer.recognize(parsed_doc)

        elapsed = round(time.time() - start_time, 2)

        results = []
        for i, elem in enumerate(classified):
            if isinstance(elem.element, ParsedTable):
                text = f"[TABLE {elem.element.num_rows}x{elem.element.num_cols}]"
            else:
                text = getattr(elem.element, 'text', '')[:120]

            results.append({
                'id': f'el-{i}',
                'type': elem.element_type.value.upper(),
                'source': elem.source,
                'text': text,
            })

        print(f"[API] Analyzed {file.filename}: {len(results)} elements in {elapsed}s")

        return jsonify({
            'elements': results,
            'total': len(results),
            'elapsed': f'{elapsed}s',
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

    finally:
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass

@app.route('/api/train', methods=['POST'])
def train_model():
    try:
        start_time = time.time()
        classifier = DocumentClassifier()
        result = classifier.train()
        elapsed = round(time.time() - start_time, 2)

        response = {
            'accuracy': result.get('accuracy', 0),
            'samples': result.get('num_samples', 0),
            'features': result.get('num_features', 0),
            'elapsed': f'{elapsed}s',
        }

        print(f"[API] Training complete: accuracy={response['accuracy']:.4f}, "
              f"samples={response['samples']}, features={response['features']}, "
              f"elapsed={elapsed}s")

        return jsonify(response)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/settings', methods=['GET'])
def get_settings():
    return jsonify({
        'font': current_config.font_name,
        'lineSpacing': current_config.line_spacing,
        'marginTop': round(current_config.top_margin.cm, 2),
        'marginBottom': round(current_config.bottom_margin.cm, 2),
        'marginLeft': round(current_config.left_margin.cm, 2),
        'marginRight': round(current_config.right_margin.cm, 2),
    })

@app.route('/api/settings', methods=['POST'])
def update_settings():
    global current_config
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No settings provided'}), 400

    try:
        current_config = FormattingConfig(
            font_name=data.get('font', current_config.font_name),
            line_spacing=data.get('lineSpacing', current_config.line_spacing),
            top_margin=Cm(data.get('marginTop', current_config.top_margin.cm)),
            bottom_margin=Cm(data.get('marginBottom', current_config.bottom_margin.cm)),
            left_margin=Cm(data.get('marginLeft', current_config.left_margin.cm)),
            right_margin=Cm(data.get('marginRight', current_config.right_margin.cm)),
        )

        print(f"[API] Settings updated: font={current_config.font_name}, "
              f"spacing={current_config.line_spacing}, "
              f"margins=({current_config.top_margin.cm:.2f}, {current_config.bottom_margin.cm:.2f}, "
              f"{current_config.left_margin.cm:.2f}, {current_config.right_margin.cm:.2f})")

        return jsonify({'status': 'saved'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("  ML DOCX Formatting API Server")
    print("  http://localhost:5000")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)
