"""Streamlit application for the unmapped LO17 Search Engine and Harry Potter RAG Hub.
Provides a premium, custom-styled interface with HSL gradients, glassmorphism and real-time execution logs.
"""

import os
import sys
import streamlit as st

# Configure page metadata and styling first
st.set_page_config(
    page_title="LO17 & RAG Intelligence Hub",
    page_icon="🪄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Resolve paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
src_path = os.path.join(PROJECT_ROOT, "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Import adapters and modules
import html
import re
import json
from src.search_adapters.search_bridge import SearchEngineBridge
from src.RAG.loader_pdf import PDFBookLoader
from src.RAG.vectorstore import RAGVectorStore
from src.RAG.chain import HarryPotterRAGChain
from src.RAG.evaluation import RAGEvaluator
from src.research_engine.pdf_corpus_parser import PDFCorpusParser, detect_book_num, HP_METADATA
from src.research_engine.tokenizer import Tokenizer
from src.research_engine.inverted_index import InvertedIndexGenerator
from src.research_engine.stemmer import Stemmer

def highlight_text(raw_text: str, keywords: list) -> str:
    """Highlights keywords in the given text by wrapping them in <strong> tags, escaping HTML first."""
    if not raw_text:
        return ""
    safe_text = html.escape(raw_text)
    if not keywords:
        return safe_text
    
    literal_keywords = []
    for k in keywords:
        if k and isinstance(k, str):
            kw_cleaned = k.strip()
            if len(kw_cleaned) >= 2:
                literal_keywords.append(re.escape(kw_cleaned))
                
    if not literal_keywords:
        return safe_text
    
    pattern = re.compile(r'(' + '|'.join(literal_keywords) + r')', re.IGNORECASE)
    return pattern.sub(r'<strong>\1</strong>', safe_text)

# Premium Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    
    /* Global Typography & Font override */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    h1, h2, h3 {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
    }
    
    /* Minimalist Header Styling */
    .header-container {
        padding: 1rem 0 1.5rem 0;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .header-title {
        color: #f8fafc;
        font-size: 1.8rem;
        margin: 0;
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    
    .header-subtitle {
        color: #64748b;
        font-size: 0.95rem;
        margin: 0;
    }

    /* Modern Chat UI */
    .stChatMessage {
        padding: 1rem 0;
    }
    .stChatMessage[data-testid="chat-message-user"] {
        background-color: transparent;
    }
    .stChatMessage[data-testid="chat-message-assistant"] {
        background-color: transparent;
    }
    .stChatMessage .stMarkdown p {
        font-size: 1.05rem;
        line-height: 1.6;
        color: #e2e8f0;
    }
    
    /* LO17 Search Classic UI layout */
    .result-card {
        background: rgba(30, 41, 59, 0.7);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 15px;
        transition: transform 0.2s, border-color 0.2s;
        text-decoration: none;
        color: inherit;
        display: block;
    }
    .result-card:hover {
        transform: translateY(-2px);
        border-color: rgba(99, 102, 241, 0.6);
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.15);
    }
    .result-id {
        color: #10b981;
        font-weight: 700;
        font-size: 0.8rem;
        margin-bottom: 6px;
        display: block;
    }
    .result-title {
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 8px;
        color: #f8fafc;
    }
    .result-title strong {
        color: #10b981;
    }
    .result-snippet {
        font-size: 0.9rem;
        color: #94a3b8;
        margin-bottom: 12px;
        line-height: 1.5;
        font-style: italic;
    }
    .result-snippet strong {
        color: #10b981;
    }
    .result-meta {
        display: flex;
        align-items: center;
        gap: 10px;
        color: #94a3b8;
        font-size: 0.8rem;
    }
    .tag {
        background: rgba(255, 255, 255, 0.05);
        padding: 3px 8px;
        border-radius: 4px;
        border: 1px solid rgba(255, 255, 255, 0.03);
    }
    .structured-view {
        background: rgba(15, 23, 42, 0.4);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 15px;
    }
    .structured-view h3 {
        font-size: 0.9rem;
        color: #10b981;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0;
        margin-bottom: 0px;
    }
    .results-info {
        margin-bottom: 15px;
        color: #94a3b8;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Helper to read/write indexed books list
metadata_path = os.path.join(PROJECT_ROOT, "data", "output", "selected_books.json")

def get_indexed_books() -> list:
    if os.path.exists(metadata_path):
        try:
            with open(metadata_path, "r", encoding="utf-8") as f:
                import json
                return json.load(f)
        except Exception:
            return []
    return []

def save_indexed_books(books: list):
    os.makedirs(os.path.dirname(metadata_path), exist_ok=True)
    try:
        with open(metadata_path, "w", encoding="utf-8") as f:
            import json
            json.dump(books, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

if "google_api_key" not in st.session_state:
    # Try reading from .env file if present
    env_path = os.path.join(PROJECT_ROOT, ".env")
    api_key_env = ""
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if line.startswith("GOOGLE_API_KEY="):
                    api_key_env = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    st.session_state["google_api_key"] = api_key_env

if "rag_error" not in st.session_state:
    st.session_state["rag_error"] = None
if "rag_failed_bypass" not in st.session_state:
    st.session_state["rag_failed_bypass"] = False

if "selected_books" not in st.session_state:
    st.session_state["selected_books"] = get_indexed_books()
if "selection_confirmed" not in st.session_state:
    st.session_state["selection_confirmed"] = len(st.session_state["selected_books"]) > 0

# ----------------- GLOBAL INDEXING CHECK -----------------
classic_td3_dir = os.path.join(PROJECT_ROOT, "data", "output", "TD3")
rag_persist_dir = os.path.join(PROJECT_ROOT, "data", "output", "vectorstore_fr")
pdf_dir = os.path.join(PROJECT_ROOT, "data", "input")

classic_ready = os.path.exists(os.path.join(classic_td3_dir, "finale_nltk.txt"))

# Check if vectorstore exists and is non-empty without initializing RAGVectorStore (which requires API Key)
def is_rag_ready(persist_dir: str) -> bool:
    sqlite_file = os.path.join(persist_dir, "chroma.sqlite3")
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

rag_ready = is_rag_ready(rag_persist_dir)

# Check selection screen
available_books = []
if os.path.exists(pdf_dir):
    available_books = sorted([f for f in os.listdir(pdf_dir) if f.endswith('.pdf')])

if not st.session_state["selection_confirmed"]:
    if len(available_books) == 0:
        st.error("❌ Aucun livre PDF trouvé dans le dossier `data/input/`. Veuillez placer les fichiers PDF de Harry Potter dans ce dossier avant de continuer.")
        st.stop()
        
    st.markdown("""
    <div style='text-align: center; margin-top: 30px; margin-bottom: 20px;'>
        <h1 style='font-size: 2.8rem; margin-bottom: 10px;'>📚 Sélection des Livres</h1>
        <p style='font-size: 1.1rem; color: #94a3b8;'>Sélectionnez les livres de Harry Potter à inclure dans la base de données. Plus vous en choisissez, plus l'indexation RAG prendra du temps et consommera de requêtes d'API Gemini.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Checkbox selection
    chosen_books = []
    st.write("### Livres disponibles dans `data/input` :")
    for book in available_books:
        book_num = detect_book_num(book)
        clean_name = book
        if book_num and book_num in HP_METADATA:
            clean_name = f"Harry Potter {book_num} : {HP_METADATA[book_num]['rubric'].title()}"
        
        default_val = True
        if st.session_state["selected_books"]:
            default_val = book in st.session_state["selected_books"]
            
        if st.checkbox(clean_name, value=default_val, key=f"select_{book}"):
            chosen_books.append(book)
            
    st.markdown("---")
    if not chosen_books:
        st.warning("⚠️ Veuillez sélectionner au moins un livre.")
    else:
        if st.button("🪄 Confirmer la Sélection et Indexer", use_container_width=True):
            st.session_state["selected_books"] = chosen_books
            st.session_state["selection_confirmed"] = True
            
            # Check if selection changed
            currently_indexed = get_indexed_books()
            if set(chosen_books) != set(currently_indexed):
                # Force re-indexing
                try:
                    import shutil
                    for d in [os.path.join(PROJECT_ROOT, "data", "output", "TD1"), 
                              os.path.join(PROJECT_ROOT, "data", "output", "TD2"), 
                              classic_td3_dir]:
                        if os.path.exists(d):
                            shutil.rmtree(d)
                except Exception:
                    pass
                try:
                    import shutil
                    if os.path.exists(rag_persist_dir):
                        shutil.rmtree(rag_persist_dir)
                        os.makedirs(rag_persist_dir, exist_ok=True)
                except Exception:
                    pass
            st.rerun()
    st.stop()

# Only block the UI if classic or rag is not ready, and RAG bypass is not active.
if not classic_ready or (not rag_ready and not st.session_state.get("rag_failed_bypass")):
    st.markdown("""
    <div style='text-align: center; margin-top: 30px; margin-bottom: 20px;'>
        <h1 style='font-size: 3rem; margin-bottom: 10px;'>🪄 Configuration Initiale</h1>
        <p style='font-size: 1.2rem; color: #94a3b8;'>Bienvenue ! Avant de pouvoir utiliser le Hub LO17 & RAG, nous devons générer les index et les bases de données.</p>
    </div>
    
    <style>
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.02); opacity: 1; }
    }
    .loading-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(13, 6, 40, 0.6) 100%);
        padding: 25px;
        border-radius: 16px;
        border: 1px solid rgba(138, 43, 226, 0.2);
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
        margin-bottom: 25px;
        animation: pulse 2s infinite ease-in-out;
    }
    .magic-spinner {
        border: 4px solid rgba(255, 255, 255, 0.05);
        width: 65px;
        height: 65px;
        border-radius: 50%;
        border-left-color: #ffeb99; /* Gold */
        border-top-color: #8a2be2; /* Purple */
        animation: spin 1s linear infinite;
        margin: 15px auto;
        box-shadow: 0 0 15px rgba(138, 43, 226, 0.5);
    }
    </style>
    <div class="loading-card">
        <div class="magic-spinner"></div>
        <p style='font-size: 1.05rem; color: #b0a5cf; margin-top: 8px;'>
            ✨ Les forces magiques de l'indexation s'activent en arrière-plan...
        </p>
    </div>
    """, unsafe_allow_html=True)
            
    st.info("Initialisation en cours. Veuillez patienter pendant la génération automatique des index...")
    progress_bar = st.progress(0)
    log_container = st.empty()
    
    if not classic_ready:
        try:
            base_dir = PROJECT_ROOT
            td1_dir = os.path.join(base_dir, "data/output/TD1")
            td2_dir = os.path.join(base_dir, "data/output/TD2")
            td3_dir = os.path.join(base_dir, "data/output/TD3")
            
            xml_raw_path = os.path.join(td1_dir, "xml.xml")
            xml_filtered_path = os.path.join(td2_dir, "xml_filtre.xml")
            stem_mapping_path = os.path.join(td3_dir, "stem_nltk.txt")
            tfidf_path = os.path.join(td3_dir, "finale_nltk.txt")
            xml_final_path = os.path.join(td3_dir, "xml_filtre_2.xml")
            
            os.makedirs(td1_dir, exist_ok=True)
            os.makedirs(td2_dir, exist_ok=True)
            os.makedirs(td3_dir, exist_ok=True)
            
            if not os.path.exists(xml_raw_path):
                log_container.info("Phase 1/4 : Parsing des livres PDF vers XML...")
                parser = PDFCorpusParser(os.path.join(base_dir, "data/input"), selected_files=st.session_state["selected_books"])
                parser.parse()
                parser.save(xml_raw_path)
            else:
                log_container.info("Phase 1/4 : Fichier XML brut trouvé, parsing ignoré.")
            
            progress_bar.progress(15)
            
            if not os.path.exists(xml_filtered_path):
                log_container.info("Phase 2/4 : Tokenisation et filtrage des mots vides...")
                tokenizer = Tokenizer(xml_filepath=xml_raw_path, output_dir=td2_dir)
                tokenizer.export_stats()
            else:
                log_container.info("Phase 2/4 : Fichier XML filtré trouvé, tokenisation ignorée.")
            
            progress_bar.progress(30)
            
            if not os.path.exists(stem_mapping_path) or not os.path.exists(tfidf_path):
                log_container.info("Phase 3/4 : Racinisation (Stemming) avec NLTK...")
                stemmer_engine = Stemmer(xml_filtered_path, stem_mapping_path)
                stemmer_engine.run()
                tokenizer = Tokenizer(xml_filepath=xml_raw_path, output_dir=td2_dir)
                tokenizer.export_stem_stats(stem_dict_file=stem_mapping_path, target_xml=xml_filtered_path, out_file=tfidf_path, filter_again=True)
            else:
                log_container.info("Phase 3/4 : Fichiers Stem et TF-IDF trouvés, stemming ignoré.")
            
            progress_bar.progress(45)
            
            if not os.path.exists(os.path.join(td3_dir, "inverse_text.txt")):
                log_container.info("Phase 4/4 : Génération de l'index inversé et des poids TF-IDF...")
                index_gen = InvertedIndexGenerator(xml_filepath=xml_final_path, output_dir=td3_dir)
                index_gen.generate()
                index_gen.export()
            else:
                log_container.info("Phase 4/4 : Index inversé trouvé, génération finale ignorée.")
        except Exception as e:
            st.error(f"Erreur d'indexation classique : {e}")
            st.stop()
            
    progress_bar.progress(50)
    
    if not rag_ready:
        if not st.session_state.get("google_api_key"):
            log_container.warning("⚠️ L'assistant IA RAG nécessite une clé API Google Gemini pour pouvoir formuler des réponses.")
            col_key, col_bypass = st.columns([3, 2])
            with col_key:
                key_input = st.text_input("Veuillez saisir votre GOOGLE_API_KEY :", type="password", help="Cette clé est requise pour la génération de texte par l'IA.", key="init_api_key")
                if key_input:
                    st.session_state["google_api_key"] = key_input
                    os.environ["GOOGLE_API_KEY"] = key_input
                    st.rerun()
            with col_bypass:
                st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                if st.button("👉 Accéder uniquement au Moteur Classique (sans RAG)", use_container_width=True):
                    st.session_state["rag_error"] = "Aucune clé API fournie. L'initialisation du RAG a été ignorée par l'utilisateur."
                    st.session_state["rag_failed_bypass"] = True
                    st.rerun()
            st.stop()
                
        log_container.info("Phase RAG : Génération de la base de données vectorielle locale via HuggingFace (cela peut prendre quelques minutes)...")
        try:
            vstore_mgr = RAGVectorStore(persist_dir=rag_persist_dir)
            loader = PDFBookLoader(directory_path=pdf_dir, selected_files=st.session_state["selected_books"])
            chunks = loader.load_and_split(st_logger=log_container.info)
            vstore_mgr.create_store(chunks, st_logger=log_container.info)
        except Exception as e:
            st.session_state["rag_error"] = str(e)
            st.session_state["rag_failed_bypass"] = True
            log_container.error(f"Erreur d'indexation RAG : {e}")
            st.warning("⚠️ L'initialisation du RAG a échoué. Redirection vers l'interface en mode limité dans 5 secondes...")
            import time
            time.sleep(5)
            st.rerun()
            
    save_indexed_books(st.session_state["selected_books"])
    progress_bar.progress(100)
    log_container.success("Initialisation terminée ! Démarrage de l'interface...")
    import time
    time.sleep(1)
    st.rerun()

# ----------------- SIDEBAR CONFIGURATIONS -----------------

with st.sidebar:
    st.image("https://img.icons8.com/color/96/harry-potter.png", width=64)
    st.title("Hub Configuration")
    
    # Navigation
    app_mode = st.radio("Navigation", options=["🧙 Assistant RAG", "🔍 Recherche Classique"])
    st.markdown("---")
    
    # API Key Input
    api_key = st.text_input(
        "Gemini API Key",
        value=st.session_state["google_api_key"],
        type="password",
        help="Saisissez votre clé API Gemini pour activer les fonctionnalités de RAG."
    )
    if api_key != st.session_state["google_api_key"]:
        st.session_state["google_api_key"] = api_key
        os.environ["GOOGLE_API_KEY"] = api_key
        st.rerun()
    elif api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
        
    st.markdown("---")
    
    st.subheader("RAG Parameters")
    rag_model = st.selectbox(
        "Gemini Model",
        options=[
            "gemini-3.1-flash-lite",
            "gemini-3.5-flash",
            "gemini-3-flash",
            "gemini-2.5-flash",
            "gemini-2.5-flash-lite"
        ],
        index=0,
        help="Sélectionnez le modèle LLM. Note : 'gemini-3.1-flash-lite' offre la limite gratuite la plus élevée (15 RPM / 500 RPD)."
    )
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.2,
        step=0.05,
        help="Une température basse favorise des réponses factuelles et fidèles au contexte."
    )
    
    st.markdown("---")
    st.subheader("Database Scope")
    num_selected = len(st.session_state.get("selected_books", []))
    st.markdown(f"📚 **{num_selected}** livre{'s' if num_selected != 1 else ''} sélectionné{'s' if num_selected != 1 else ''}")
    if st.button("⚙️ Modifier la sélection", key="sidebar_change_selection", use_container_width=True):
        st.session_state["selection_confirmed"] = False
        st.rerun()
    
    if st.session_state.get("rag_error"):
        st.markdown("---")
        st.error("⚠️ Assistant RAG désactivé")
        st.caption(f"**Erreur :** {st.session_state['rag_error']}")
        if st.button("🔄 Réessayer l'initialisation", key="sidebar_retry_rag", use_container_width=True):
            st.session_state["rag_error"] = None
            st.session_state["rag_failed_bypass"] = False
            st.rerun()

    st.markdown("---")
    st.markdown("""
    **Projet UTC LO17 / AI31**  
    *Printemps 2026*  
    Moteur classique de recherche & Système RAG sur les livres de Harry Potter.
    """)

# =====================================================================
# TAB 1: ASSISTANT RAG (HARRY POTTER)
# =====================================================================

if app_mode == "🧙 Assistant RAG":
    if st.session_state.get("rag_error"):
        st.error(f"""
        ⚠️ **L'Assistant RAG est actuellement indisponible.**
        
        **Détail de l'erreur rencontré :**
        `{st.session_state['rag_error']}`
        
        L'initialisation de la base vectorielle ChromaDB a échoué (limite de quota d'API Gemini dépassée 429, clé invalide ou erreur réseau).
        """)
        
        st.info("💡 Vous pouvez continuer à utiliser l'onglet **Moteur de Recherche Classique** pour interroger les livres de Harry Potter sans clé API.")
        
        if st.button("🔄 Réinitialiser et réessayer l'indexation RAG", key="tab_retry_rag"):
            st.session_state["rag_error"] = None
            st.session_state["rag_failed_bypass"] = False
            st.rerun()
    elif not st.session_state["google_api_key"]:
        st.warning("⚠️ Clé API Gemini manquante. Veuillez saisir votre GOOGLE_API_KEY dans la barre latérale pour activer le RAG.")
    else:
        # Vectorstore is already guaranteed to exist by global check
        @st.cache_resource(show_spinner="Chargement de la base vectorielle...")
        def get_rag_components(persist_dir, model_name, temp):
            vstore_mgr = RAGVectorStore(persist_dir=persist_dir)
            vstore = vstore_mgr.load_store()
            chain = HarryPotterRAGChain(vectorstore=vstore, model_name=model_name, temperature=temp)
            _evaluator = RAGEvaluator(model_name=model_name)
            return chain, _evaluator

        rag_chain, evaluator = get_rag_components(rag_persist_dir, rag_model, temperature)
            
        # Chat history interface
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Bonjour ! Je suis votre assistant expert sur l'univers de Harry Potter. Que souhaitez-vous savoir ?"}]
            
        # Render chat history
        for message in st.session_state.messages:
            avatar = "🧑‍💻" if message["role"] == "user" else "✨"
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])
                
                # Small columns for metadata if they exist
                if "sources" in message or "evaluation" in message:
                    col1, col2 = st.columns(2)
                    if "sources" in message:
                        with col1:
                            with st.expander("📚 Sources récupérées"):
                                for idx, doc in enumerate(message["sources"], 1):
                                    src_name = os.path.basename(doc.metadata.get('source', 'Inconnu'))
                                    page = doc.metadata.get('page', 'Inconnue')
                                    st.markdown(f"**Source {idx}** | `{src_name}` (p. {page})")
                                    st.caption(doc.page_content[:200] + "...")
                                    
                    if "evaluation" in message:
                        eval_data = message["evaluation"]
                        f_score = eval_data["faithfulness"].get("score", 0.0)
                        r_score = eval_data["relevance"].get("score", 0.0)
                        icon = "🟢" if f_score >= 0.8 and r_score >= 0.8 else ("🟡" if f_score >= 0.5 and r_score >= 0.5 else "🔴")
                        with col2:
                            with st.expander(f"{icon} Audit IA (Fidélité: {f_score:.2f})"):
                                st.write("**Fidélité au Contexte**")
                                st.caption(eval_data['faithfulness'].get('justification', ''))
                                st.write("**Pertinence**")
                                st.caption(eval_data['relevance'].get('justification', ''))
                            
        # Prompt Input
        if prompt := st.chat_input("Posez votre question (ex: 'Quelle est la maison de Draco Malfoy ?' ou 'Comment s'appelle le chat de Hermione ?')"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user", avatar="🧑‍💻"):
                st.markdown(prompt)
            
            with st.chat_message("assistant", avatar="✨"):
                with st.spinner("Analyse des grimoires en cours..."):
                    response_data = rag_chain.query(prompt)
                    answer = response_data["answer"]
                    sources = response_data["source_documents"]
                    
                    st.markdown(answer)
                    
                    # Run evaluation
                    with st.spinner("Vérification anti-hallucination..."):
                        eval_res = evaluator.evaluate(prompt, answer, sources)
                        
                    col1, col2 = st.columns(2)
                    with col1:
                        with st.expander("📚 Sources récupérées"):
                            for idx, doc in enumerate(sources, 1):
                                src_name = os.path.basename(doc.metadata.get('source', 'Inconnu'))
                                page = doc.metadata.get('page', 'Inconnue')
                                st.markdown(f"**Source {idx}** | `{src_name}` (p. {page})")
                                st.caption(doc.page_content[:200] + "...")
                                
                    with col2:
                        f_score = eval_res["faithfulness"].get("score", 0.0)
                        r_score = eval_res["relevance"].get("score", 0.0)
                        icon = "🟢" if f_score >= 0.8 and r_score >= 0.8 else ("🟡" if f_score >= 0.5 and r_score >= 0.5 else "🔴")
                        with st.expander(f"{icon} Audit IA (Fidélité: {f_score:.2f})"):
                            st.write("**Fidélité au Contexte**")
                            st.caption(eval_res['faithfulness'].get('justification', ''))
                            st.write("**Pertinence**")
                            st.caption(eval_res['relevance'].get('justification', ''))
            
            # Save to history
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources,
                "evaluation": eval_res
            })

# =====================================================================
# TAB 2: MOTEUR DE RECHERCHE CLASSIQUE (HARRY POTTER)
# =====================================================================

elif app_mode == "🔍 Recherche Classique":
    st.subheader("Recherche Classique LO17 sur Harry Potter")
    st.write("Interrogez le moteur de recherche classique LO17 adapté aux livres de Harry Potter (indexation inversée, équations booléennes, correction orthographique et scoring de pertinence).")
    
    # Initialize classic engine
    try:
        bridge = SearchEngineBridge()
        engine_ready = True
    except FileNotFoundError as e:
        engine_ready = False
        
    if engine_ready:
        col_main_left, col_main_right = st.columns([3, 2])
        
        with col_main_left:
            st.markdown("### 🔍 Moteur de Recherche")
            col_q, col_s, col_b = st.columns([4, 2, 1])
            with col_q:
                query_str = st.text_input("Recherche", placeholder="Saisissez votre requête en langage naturel...", label_visibility="collapsed", key="classic_query")
            with col_s:
                sort_by = st.selectbox("Trier par", options=["relevance", "newest", "oldest"], format_func=lambda x: {"relevance": "Pertinence", "newest": "Plus récent", "oldest": "Plus ancien"}[x], label_visibility="collapsed")
            with col_b:
                search_btn = st.button("Search", use_container_width=True)
                
        if query_str or search_btn:
            import time
            start_time = time.time()
            with col_main_left:
                with st.spinner("Analyse et recherche..."):
                    search_res = bridge.search(query_str, sort_by=sort_by)
            time_ms = (time.time() - start_time) * 1000
            
            results = search_res["results"]
            structured = search_res["structured"]
            logs = search_res["logs"]
            
            with col_main_left:
                st.markdown(f'<div class="results-info"><span>{len(results)} résultat{"s" if len(results) != 1 else ""} trouvé{"s" if len(results) != 1 else ""}</span> <span style="font-size: 0.8rem; opacity: 0.6; margin-left: 10px;">({time_ms:.2f} ms)</span></div>', unsafe_allow_html=True)
                
                if not results:
                    st.markdown('<div class="result-card" style="text-align:center">Aucun document ne correspond à votre requête.</div>', unsafe_allow_html=True)
                else:
                    hl_keywords = structured.get("highlight_keywords", [])
                    for res in results:
                        title_hl = highlight_text(res['title'], hl_keywords)
                        snippet_hl = highlight_text(res['snippet'], hl_keywords)
                        
                        st.markdown(f"""
                        <div class="result-card">
                            <span class="result-id">ID: {res['id']}</span>
                            <div class="result-title">📖 {title_hl}</div>
                            <div class="result-snippet">{snippet_hl}</div>
                            <div class="result-meta">
                                <span class="tag">📅 {res['date']}</span>
                                <span class="tag">📂 {res['rubric']}</span>
                                <span class="tag">🔍 Pertinence: {round(res['score'], 2)}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
            with col_main_right:
                st.markdown("""
                <div class="structured-view" style="display: block;">
                    <h3>Représentation Structurée</h3>
                </div>
                """, unsafe_allow_html=True)
                
                date_filter = "ALL"
                if structured.get('date_min') or structured.get('date_max'):
                    date_filter = f"{structured.get('date_min', '*')} to {structured.get('date_max', '*')}"
                    
                xml_aligned_structured = {
                    "id": "ALL",
                    "livre": "ALL",
                    "date": date_filter,
                    "rubric": structured.get("rubric", "ALL"),
                    "author": "ALL",
                    "text": structured.get("equation", " ".join(structured.get("keywords", [])))
                }
                st.code(json.dumps(xml_aligned_structured, indent=4, ensure_ascii=False), language="json")
                
                st.markdown("<br>", unsafe_allow_html=True)
                with st.expander("Voir les logs d'exécution", expanded=False):
                    log_text = "\n".join([f"[{l[0]}][{l[1]}] {l[2]}" for l in logs])
                    st.code(log_text, language="log")
        else:
            with col_main_right:
                st.info("Les résultats structurés et les logs apparaîtront ici après une recherche.")


