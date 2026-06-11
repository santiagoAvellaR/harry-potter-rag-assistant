"""RAG Execution Chain for Harry Potter Q&A using LangChain and ChatGoogleGenerativeAI.
"""

from typing import Dict, Any, List
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.documents import Document

DEFAULT_PROMPT_TEMPLATE = """Vous êtes un assistant expert de l'univers de Harry Potter.
Utilisez les extraits de texte suivants fournis comme contexte pour répondre à la question de l'utilisateur.
Si vous ne connaissez pas la réponse ou si le contexte ne la contient pas, dites-le honnêtement ("Je ne sais pas"). Ne tentez pas d'inventer des faits.
Répondez en français de manière claire et concise.

Question: {question}

Contexte (livres de Harry Potter):
{context}

Réponse:"""

class HarryPotterRAGChain:
    """Configures and runs the generation chain for the Harry Potter RAG."""
    
    def __init__(self, vectorstore, model_name: str = "gemini-3.5-flash", temperature: float = 0.2):
        self.vectorstore = vectorstore
        self.model_name = model_name
        self.temperature = temperature
        
        # Initialize the Google Generative AI model
        self.llm = ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=self.temperature
        )
        
        # Configure prompt template
        self.prompt = PromptTemplate.from_template(DEFAULT_PROMPT_TEMPLATE)
        
        # Configure retriever interface (fetch top 4 relevant chunks by default)
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 4})
        
        # Setup generation pipeline
        self.chain = (
            self.prompt
            | self.llm
            | StrOutputParser()
        )

    def _format_docs(self, docs: List[Document]) -> str:
        """Formats a list of Documents into a single block of text."""
        formatted = []
        for i, doc in enumerate(docs, 1):
            source = os.path.basename(doc.metadata.get('source', 'Inconnu'))
            page = doc.metadata.get('page', 'Inconnu')
            formatted.append(f"[Source {i} | Livre: {source}, Page: {page}]\n{doc.page_content}")
        return "\n\n".join(formatted)

    def query(self, question: str) -> Dict[str, Any]:
        """Queries the RAG chain and returns both the answer and the source documents."""
        # 1. Retrieve relevant documents
        source_docs = self.retriever.invoke(question)
        
        # 2. Format context
        context_text = self._format_docs(source_docs)
        
        # 3. Generate answer
        answer = self.chain.invoke({
            "context": context_text,
            "question": question
        })
        
        return {
            "answer": answer,
            "source_documents": source_docs
        }

import os
