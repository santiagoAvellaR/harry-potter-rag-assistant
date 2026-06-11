"""Bridge adapter to import and expose the classical LO17 search engine components.
Ensures correct paths are added to sys.path so relative imports within the research-engine module work correctly.
"""

import os
import sys

# Resolve paths
BRIDGE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BRIDGE_DIR, "../.."))
ENGINE_SRC_DIR = os.path.join(PROJECT_ROOT, "src", "research_engine")

# Add the research-engine directory to sys.path to resolve relative imports (e.g. from traitement_requete import ...)
if ENGINE_SRC_DIR not in sys.path:
    sys.path.append(ENGINE_SRC_DIR)

# Now safely import components
import moteur
import traitement_requete
import tokenizer
import spell_checker
import stemmer
import logger

class SearchEngineBridge:
    """Helper to initialize and query the classical search engine from the root project."""
    
    def __init__(self, data_root: str = None):
        if data_root is None:
            data_root = os.path.join(PROJECT_ROOT, "data")
            
        self.xml_path = os.path.join(data_root, "output", "TD1", "xml.xml")
        self.index_dir = os.path.join(data_root, "output", "TD3")
        self.anti_dic_path = os.path.join(data_root, "output", "TD2", "anti_dic.txt")
        self.stem_path = os.path.join(data_root, "output", "TD3", "stem_nltk.txt")
        
        # Verify indexes exist
        if not os.path.exists(self.xml_path) or not os.path.exists(self.index_dir):
            raise FileNotFoundError(
                f"Classic engine indexes not found. "
                f"Please ensure they exist at:\n"
                f"- XML: {self.xml_path}\n"
                f"- Index: {self.index_dir}"
            )
            
        # Initialize subcomponents
        self.tok = tokenizer.Tokenizer(xml_filepath=self.xml_path, output_dir=os.path.dirname(self.anti_dic_path))
        self.stop_words = self.tok.load_dictionary(self.anti_dic_path)
        self.spell = spell_checker.SpellChecker(lexicon_file=self.stem_path)
        self.engine = moteur.SearchEngine(index_dir=self.index_dir, xml_path=self.xml_path)

    def search(self, query: str, sort_by: str = "relevance") -> dict:
        """Executes full parsing, spell check, boolean resolution, and scoring."""
        req_logger = logger.RequestLogger()
        req_logger.log("BRIDGE", f"Received query: '{query}' (Sort: {sort_by})")
        
        # 1. Parse natural query
        structured = traitement_requete.process_request(
            query_text=query,
            stemmer=None,
            spell_checker=self.spell,
            stop_words=self.stop_words,
            logger=req_logger
        )
        
        # 2. Search
        results = self.engine.search(structured, sort_by=sort_by, logger=req_logger)
        
        return {
            "results": results,
            "structured": structured,
            "logs": req_logger.logs
        }
