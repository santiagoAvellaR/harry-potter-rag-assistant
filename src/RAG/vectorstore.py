"""Vector database manager for storing and retrieving document embeddings using Chroma and Gemini.
"""

import os
from typing import List
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

class RAGVectorStore:
    """Manages the creation, persistence, and loading of the Chroma vector store."""
    
    def __init__(self, persist_dir: str, model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        self.persist_dir = persist_dir
        self.model_name = model_name
        self.embeddings = HuggingFaceEmbeddings(model_name=self.model_name)

    def create_store(self, documents: List[Document], st_logger=None) -> Chroma:
        """Creates a new Chroma vector store from documents and persists it to disk."""
        msg = f"🌐 Génération des embeddings via HuggingFace et sauvegarde locale dans : {self.persist_dir}..."
        if st_logger:
            st_logger(msg)
        else:
            print(msg)
            
        vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_dir,
            collection_metadata={"hnsw:space": "cosine"}
        )
        
        msg2 = "✅ Vector store created and saved successfully."
        if st_logger:
            st_logger(msg2)
        else:
            print(msg2)
            
        return vectorstore

    def load_store(self) -> Chroma:
        """Loads an existing Chroma vector store from disk."""
        if not self.exists():
            raise FileNotFoundError(f"No vector store found at {self.persist_dir}. Please create it first.")
        print(f"Loading Chroma vector store from: {self.persist_dir}...")
        return Chroma(
            persist_directory=self.persist_dir,
            embedding_function=self.embeddings
        )

    def exists(self) -> bool:
        """Checks if a persisted vector store already exists on disk and is non-empty."""
        sqlite_file = os.path.join(self.persist_dir, "chroma.sqlite3")
        if not os.path.exists(sqlite_file):
            return False
        try:
            import sqlite3
            conn = sqlite3.connect(sqlite_file)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM embeddings;")
            count = cursor.fetchone()[0]
            conn.close()
            return count > 0
        except Exception:
            return False
