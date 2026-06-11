"""Parses Harry Potter PDF books page-by-page and builds a structured XML corpus.
Uses the schema tags: <id>, <livre>, <date>, <rubric>, <author>, <text>, <contact>.
No <title> field is generated, as requested.
"""

import os
import re
import unicodedata
from lxml import etree
import pypdf

# Metadata for each book
HP_METADATA = {
    1: {"date": "26/06/1997", "rubric": "l'école des sorciers"},
    2: {"date": "02/07/1998", "rubric": "la chambre des secrets"},
    3: {"date": "08/07/1999", "rubric": "le prisonnier d'azkaban"},
    4: {"date": "08/07/2000", "rubric": "la coupe de feu"},
    5: {"date": "21/06/2003", "rubric": "l'ordre du phénix"},
    6: {"date": "16/07/2005", "rubric": "le prince de sang-mêlé"},
    7: {"date": "21/07/2007", "rubric": "les reliques de la mort"}
}

def detect_book_num(filename: str) -> int:
    """Helper to detect book number from filename (e.g. harry-potter-3-... -> 3)"""
    match = re.search(r'(?:harry-potter-)?(\d)', filename.lower())
    if match:
        num = int(match.group(1))
        if 1 <= num <= 7:
            return num
    return None

class PDFCorpusParser:
    """Parses PDF Harry Potter books and builds an XML corpus."""
    
    def __init__(self, input_dir: str):
        self.input_dir = input_dir
        self.corpus = etree.Element('corpus')

    def parse(self) -> etree.Element:
        """Reads all PDFs, extracts text from pages, and appends XML documents."""
        if not os.path.exists(self.input_dir):
            raise FileNotFoundError(f"Input directory {self.input_dir} not found.")
            
        pdf_files = [f for f in os.listdir(self.input_dir) if f.endswith(".pdf")]
        # Sort files by book number
        pdf_files.sort(key=lambda x: detect_book_num(x) or 99)
        
        for filename in pdf_files:
            book_num = detect_book_num(filename)
            if not book_num:
                print(f"[WARN] Could not detect book number for: {filename}. Skipping.")
                continue
                
            metadata = HP_METADATA[book_num]
            filepath = os.path.join(self.input_dir, filename)
            print(f"Parsing: {filename} (Book {book_num})...")
            
            try:
                reader = pypdf.PdfReader(filepath)
                num_pages = len(reader.pages)
                
                for page_idx in range(num_pages):
                    page_num = page_idx + 1
                    doc_id = book_num * 1000 + page_num  # Unique numeric ID (e.g. 1042 for Book 1, Page 42)
                    
                    page = reader.pages[page_idx]
                    text = page.extract_text() or ""
                    
                    # Clean and normalize text
                    text = unicodedata.normalize("NFC", text).strip()
                    if not text:
                        continue
                        
                    doc_node = etree.SubElement(self.corpus, 'document')
                    
                    etree.SubElement(doc_node, 'id').text = str(doc_id)
                    etree.SubElement(doc_node, 'livre').text = str(book_num)
                    etree.SubElement(doc_node, 'date').text = metadata["date"]
                    etree.SubElement(doc_node, 'rubric').text = metadata["rubric"]
                    etree.SubElement(doc_node, 'author').text = "J.K. Rowling"
                    etree.SubElement(doc_node, 'text').text = text
                    # Contact and images removed from corpus as requested
                    
            except Exception as e:
                print(f"[ERROR] Failed to parse {filename}: {e}")
                
        return self.corpus

    def save(self, filepath: str):
        """Saves the XML tree to the specified file path."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        tree = etree.ElementTree(self.corpus)
        tree.write(filepath, encoding="utf-8", xml_declaration=True, pretty_print=True)
        print(f"XML corpus saved successfully to: {filepath}")

if __name__ == "__main__":
    import sys
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    input_dir = os.path.join(base_dir, "data", "input")
    output_xml = os.path.join(base_dir, "data", "output", "TD1", "xml.xml")
    
    parser = PDFCorpusParser(input_dir)
    parser.parse()
    parser.save(output_xml)
