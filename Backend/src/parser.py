import docx
from docx.oxml.ns import qn
from dataclasses import dataclass
from typing import List, Union, Optional

@dataclass
class ParsedElement:
    text: str
    index: int
    style_name: Optional[str] = None
    is_bold: bool = False
    is_italic: bool = False
    font_size: Optional[float] = None
    is_all_caps: bool = False
    has_image: bool = False
    image_data: Optional[bytes] = None
    image_content_type: Optional[str] = None

@dataclass
class ParsedTable:
    rows: List[List[str]]
    index: int
    num_rows: int
    num_cols: int

@dataclass
class ParsedDocument:
    elements: List[Union[ParsedElement, ParsedTable]]
    filename: str

class DocxParser:
    def _extract_image(self, paragraph) -> tuple[Optional[bytes], Optional[str]]:
        blips = paragraph._element.findall('.//' + qn('a:blip'))
        if blips:
            rId = blips[0].get(qn('r:embed'))
            if rId:
                rel = paragraph.part.rels[rId]
                image_data = rel.target_part.blob
                content_type = rel.target_part.content_type
                return image_data, content_type
        return None, None

    def parse(self, filepath: str) -> ParsedDocument:
        doc = docx.Document(filepath)
        elements = []
        index = 0

        for element in doc.element.body:
            if element.tag == qn('w:p'):
                para = docx.text.paragraph.Paragraph(element, doc)
                text = para.text
                style_name = para.style.name if para.style else None
                
                is_bold = False
                is_italic = False
                font_size = None
                
                if para.runs:
                    all_bold = True
                    for run in para.runs:
                        if run.bold is False and not (para.style and para.style.font.bold):
                            all_bold = False
                        if run.font.size and font_size is None:
                            font_size = run.font.size.pt
                    is_bold = all_bold or bool(para.style and para.style.font.bold)
                else:
                    is_bold = bool(para.style and para.style.font.bold)
                    
                is_all_caps = text.isupper() if text.strip() else False
                image_data, content_type = self._extract_image(para)
                has_image = image_data is not None
                
                parsed_elem = ParsedElement(
                    text=text,
                    index=index,
                    style_name=style_name,
                    is_bold=is_bold,
                    is_italic=is_italic,
                    font_size=font_size,
                    is_all_caps=is_all_caps,
                    has_image=has_image,
                    image_data=image_data,
                    image_content_type=content_type
                )
                elements.append(parsed_elem)
                index += 1
                
            elif element.tag == qn('w:tbl'):
                tbl = docx.table.Table(element, doc)
                rows = []
                for row in tbl.rows:
                    row_data = [cell.text for cell in row.cells]
                    rows.append(row_data)
                    
                num_rows = len(rows)
                num_cols = len(rows[0]) if num_rows > 0 else 0
                
                parsed_tbl = ParsedTable(
                    rows=rows,
                    index=index,
                    num_rows=num_rows,
                    num_cols=num_cols
                )
                elements.append(parsed_tbl)
                index += 1
                
        return ParsedDocument(elements=elements, filename=filepath)
