"""Vector database manager for storing and retrieving document embeddings using Chroma and Gemini.
"""

import os
from typing import List
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

class RAGVectorStore:
    """Manages the creation, persistence, and loading of the Chroma vector store."""
    
    def __init__(self, persist_dir: str, model_name: str = "models/gemini-embedding-001"):
        self.persist_dir = persist_dir
        self.model_name = model_name
        self.embeddings = GoogleGenerativeAIEmbeddings(model=self.model_name)

    def create_store(self, documents: List[Document], st_logger=None) -> Chroma:
        """Creates a new Chroma vector store from documents and persists it to disk."""
        msg = f"🌐 Génération des embeddings via Gemini API et sauvegarde locale dans : {self.persist_dir}..."
        if st_logger:
            st_logger(msg)
        else:
            print(msg)
            
        vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_dir
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
        """Checks if a persisted vector store already exists on disk."""
        # Chroma stores its index database in index files (like chroma.sqlite3) in the directory
        sqlite_file = os.path.join(self.persist_dir, "chroma.sqlite3")
        return os.path.exists(sqlite_file) or (os.path.exists(self.persist_dir) and len(os.listdir(self.persist_dir)) > 0)
