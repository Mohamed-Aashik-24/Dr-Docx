import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
import time
import sys

from src.parser import DocxParser
from src.classifier import DocumentClassifier
from src.structure_recognizer import StructureRecognizer
from src.generator import DocxGenerator

class FormatterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('DOCX Publication Formatter')
        
        tk.Label(root, text='ML-Based DOCX Publication Formatter', font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        # Input Frame
        in_frame = tk.Frame(root)
        in_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(in_frame, text='Input:').pack(side=tk.LEFT)
        self.in_var = tk.StringVar()
        tk.Entry(in_frame, textvariable=self.in_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        tk.Button(in_frame, text='Browse', command=self._browse_in).pack(side=tk.LEFT)
        
        # Output Frame
        out_frame = tk.Frame(root)
        out_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(out_frame, text='Output:').pack(side=tk.LEFT)
        self.out_var = tk.StringVar()
        tk.Entry(out_frame, textvariable=self.out_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        tk.Button(out_frame, text='Browse', command=self._browse_out).pack(side=tk.LEFT)
        
        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text='Format Document', font=('Helvetica', 12, 'bold'), bg='green', fg='white', command=self._start_format).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text='Train Model', command=self._start_train).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text='Analyze Structure', command=self._start_analyze).pack(side=tk.LEFT, padx=5)
        
        self.progress = ttk.Progressbar(root, mode='indeterminate')
        self.progress.pack(fill=tk.X, padx=10, pady=5)
        
        self.log_text = tk.Text(root, height=15)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.status_var = tk.StringVar(value='Ready')
        tk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W).pack(fill=tk.X, side=tk.BOTTOM)

    def _log(self, message: str):
        self.log_text.insert(tk.END, message + '\\n')
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def _browse_in(self):
        path = filedialog.askopenfilename(filetypes=[('Word Documents', '*.docx')])
        if path:
            self.in_var.set(path)
            if not self.out_var.get():
                self.out_var.set(path.replace('.docx', '_formatted.docx'))

    def _browse_out(self):
        path = filedialog.asksaveasfilename(defaultextension='.docx', filetypes=[('Word Documents', '*.docx')])
        if path:
            self.out_var.set(path)

    def _start_format(self):
        threading.Thread(target=self._format_document, daemon=True).start()

    def _start_train(self):
        threading.Thread(target=self._train_model, daemon=True).start()

    def _start_analyze(self):
        threading.Thread(target=self._analyze_document, daemon=True).start()

    def _format_document(self):
        input_path = self.in_var.get()
        output_path = self.out_var.get()
        
        if not input_path:
            messagebox.showerror('Error', 'Please select an input file.')
            return
            
        self.progress.start()
        self.status_var.set('Formatting...')
        try:
            self._log(f'Parsing {input_path}...')
            parser = DocxParser()
            doc = parser.parse(input_path)
            self._log(f'Parsed {len(doc.elements)} elements')
            
            self._log('Classifying elements...')
            recognizer = StructureRecognizer()
            classified = recognizer.recognize(doc)
            self._log(f'Classified {len(classified)} elements')
            
            self._log('Generating output document...')
            generator = DocxGenerator()
            generator.generate(classified, output_path)
            
            self._log(f'Success! Saved to {output_path}')
            self.status_var.set('Done')
        except Exception as e:
            self._log(f'Error: {str(e)}')
            self.status_var.set('Error')
            messagebox.showerror('Error', str(e))
        finally:
            self.progress.stop()

    def _train_model(self):
        self.progress.start()
        self.status_var.set('Training model...')
        try:
            self._log('Training ML model...')
            classifier = DocumentClassifier()
            results = classifier.train()
            self._log(f'Training complete! Results: {results}')
            self.status_var.set('Ready')
        except Exception as e:
            self._log(f'Error: {str(e)}')
            self.status_var.set('Error')
        finally:
            self.progress.stop()

    def _analyze_document(self):
        input_path = self.in_var.get()
        if not input_path:
            messagebox.showerror('Error', 'Please select an input file.')
            return
            
        self.progress.start()
        self.status_var.set('Analyzing...')
        try:
            self._log(f'Analyzing {input_path}...')
            parser = DocxParser()
            doc = parser.parse(input_path)
            recognizer = StructureRecognizer()
            classified = recognizer.recognize(doc)
            
            for r in classified:
                text = getattr(r.element, "text", "[TABLE]")[:60]
                self._log(f'[{r.element_type.value}] (conf={r.confidence:.2f}, src={r.source}) {text}')
            self.status_var.set('Ready')
        except Exception as e:
            self._log(f'Error: {str(e)}')
            self.status_var.set('Error')
        finally:
            self.progress.stop()

def launch_gui():
    root = tk.Tk()
    app = FormatterGUI(root)
    root.mainloop()

if __name__ == '__main__':
    launch_gui()
