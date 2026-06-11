"""Evaluation module for RAG performance and hallucination detection using LLM-as-a-judge.
"""

from typing import Dict, Any, List
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.documents import Document

FAITHFULNESS_PROMPT = """Vous êtes un auditeur de qualité d'IA. Votre tâche est d'évaluer si une réponse générée par un modèle d'IA est FIDÈLE au contexte fourni, c'est-à-dire qu'elle ne contient pas d'hallucinations ni d'affirmations inventées qui ne figurent pas dans le contexte.

Contexte fourni:
{context}

Réponse générée:
{answer}

Analysez la réponse phrase par phrase par rapport au contexte. Déterminez si chaque affirmation est étayée par le contexte.
Répondez STRICTEMENT au format JSON suivant:
{{
  "justification": "Expliquez brièvement votre raisonnement (quelles affirmations sont étayées, lesquelles ne le sont pas)",
  "verdict": "FIDELE" ou "HALLUCINATION_PARTIELLE" ou "HALLUCINATION_TOTALE",
  "score": un nombre décimal entre 0.0 (totalement halluciné) et 1.0 (totalement fidèle)
}}"""

ANSWER_RELEVANCE_PROMPT = """Vous êtes un auditeur de qualité d'IA. Votre tâche est d'évaluer si la réponse générée RÉPOND pertinement à la question posée, indépendamment de sa véracité.

Question de l'utilisateur:
{question}

Réponse générée:
{answer}

Répondez STRICTEMENT au format JSON suivant:
{{
  "justification": "Expliquez si la réponse répond directement à la question ou si elle est hors sujet",
  "score": un nombre décimal entre 0.0 (complètement hors sujet) et 1.0 (répond parfaitement à la question)
}}"""

class RAGEvaluator:
    """Evaluates RAG generation and checks for hallucinations using Gemini-as-a-judge."""
    
    def __init__(self, model_name: str = "gemini-3.5-flash"):
        self.model_name = model_name
        self.llm = ChatGoogleGenerativeAI(model=self.model_name, temperature=0.0)
        self.json_parser = JsonOutputParser()
        
        self.faithfulness_chain = PromptTemplate.from_template(FAITHFULNESS_PROMPT) | self.llm | self.json_parser
        self.relevance_chain = PromptTemplate.from_template(ANSWER_RELEVANCE_PROMPT) | self.llm | self.json_parser

    def evaluate(self, question: str, answer: str, source_docs: List[Document]) -> Dict[str, Any]:
        """Runs evaluation for Faithfulness (Hallucination) and Answer Relevance."""
        # Join documents content
        context_text = "\n\n".join(doc.page_content for doc in source_docs)
        
        try:
            # 1. Evaluate Faithfulness / Hallucination
            faithfulness_result = self.faithfulness_chain.invoke({
                "context": context_text,
                "answer": answer
            })
        except Exception as e:
            faithfulness_result = {
                "justification": f"Erreur d'évaluation: {str(e)}",
                "verdict": "ERREUR",
                "score": 0.0
            }

        try:
            # 2. Evaluate Answer Relevance
            relevance_result = self.relevance_chain.invoke({
                "question": question,
                "answer": answer
            })
        except Exception as e:
            relevance_result = {
                "justification": f"Erreur d'évaluation: {str(e)}",
                "score": 0.0
            }
            
        return {
            "faithfulness": faithfulness_result,
            "relevance": relevance_result
        }
