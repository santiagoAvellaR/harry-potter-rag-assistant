"""PDF document loader and text splitter for the Harry Potter RAG engine.
"""

import os
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class PDFBookLoader:
    """Handles loading and chunking of PDF books from a directory."""
    
    def __init__(self, directory_path: str, chunk_size: int = 2500, chunk_overlap: int = 500, selected_files: list = None):
        self.directory_path = directory_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.selected_files = selected_files
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ".", " ", ""]
        )

    def load_and_split(self, st_logger=None) -> List[Document]:
        """Loads all PDFs in the directory and returns split documents (chunks)."""
        if not os.path.exists(self.directory_path):
            raise FileNotFoundError(f"Directory {self.directory_path} does not exist.")
            
        if st_logger:
            st_logger(f"🔍 Recherche des PDFs dans : {self.directory_path}...")
        else:
            print(f"Loading PDFs from: {self.directory_path}...")
            
        docs = []
        if self.selected_files is not None:
            pdf_files = [f for f in self.selected_files if f.endswith('.pdf')]
        else:
            pdf_files = [f for f in os.listdir(self.directory_path) if f.endswith('.pdf')]
        
        for idx, pdf_file in enumerate(pdf_files, 1):
            pdf_path = os.path.join(self.directory_path, pdf_file)
            if st_logger:
                st_logger(f"📄 Lecture du PDF ({idx}/{len(pdf_files)}) : {pdf_file}...")
            loader = PyPDFLoader(pdf_path)
            docs.extend(loader.load())
            
        if st_logger:
            st_logger(f"✂️ Total de {len(docs)} pages chargées. Découpage en fragments (chunks)...")
        else:
            print(f"Loaded {len(docs)} pages.")
        
        chunks = self.splitter.split_documents(docs)
        
        if st_logger:
            st_logger(f"✅ Découpage terminé : {len(chunks)} fragments générés.")
        else:
            print(f"Created {len(chunks)} text chunks.")
            
        return chunks

if __name__ == "__main__":
    # Test execution
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    input_dir = os.path.join(base_dir, "data", "input")
    try:
        loader = PDFBookLoader(input_dir)
        # Note: testing only, won't execute full splitting if running as importing module
        print("Loader configured successfully.")
    except Exception as e:
        print(f"Configuration test error: {e}")
