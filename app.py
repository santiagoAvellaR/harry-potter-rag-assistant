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
from src.research_engine.pdf_corpus_parser import PDFCorpusParser
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
    
    /* Header Gradient styling */
    .header-container {
        background: linear-gradient(135deg, #2b1854 0%, #0d0628 100%);
        padding: 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        border: 1px solid #4a2d82;
        box-shadow: 0 8px 32px 0 rgba(13, 6, 40, 0.37);
        text-align: center;
    }
    
    .header-title {
        color: #fdfdfd;
        background: linear-gradient(90deg, #b8860b, #e6b800, #ffeb99);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        margin: 0;
        letter-spacing: 1px;
    }
    
    .header-subtitle {
        color: #b0a5cf;
        font-size: 1.1rem;
        margin-top: 0.5rem;
        font-weight: 300;
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

# ----------------- SESSION STATE & INITIALIZATION -----------------

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

# ----------------- GLOBAL INDEXING CHECK -----------------
classic_td3_dir = os.path.join(PROJECT_ROOT, "data", "output", "TD3")
rag_persist_dir = os.path.join(PROJECT_ROOT, "data", "output", "vectorstore")
pdf_dir = os.path.join(PROJECT_ROOT, "data", "input")

classic_ready = os.path.exists(os.path.join(classic_td3_dir, "finale_nltk.txt"))

# Check if vectorstore exists without initializing RAGVectorStore (which requires API Key)
sqlite_file = os.path.join(rag_persist_dir, "chroma.sqlite3")
rag_ready = os.path.exists(sqlite_file) or (os.path.exists(rag_persist_dir) and len(os.listdir(rag_persist_dir)) > 0)

# Only block the UI if classic or rag is not ready.
if not classic_ready or not rag_ready:
    st.markdown("""
    <div style='text-align: center; margin-top: 50px; margin-bottom: 30px;'>
        <h1 style='font-size: 3rem; margin-bottom: 10px;'>🪄 Configuration Initiale</h1>
        <p style='font-size: 1.2rem; color: #94a3b8;'>Bienvenue ! Avant de pouvoir utiliser le Hub LO17 & RAG, nous devons générer les index et les bases de données.</p>
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
            
            log_container.info("Phase 1/4 : Parsing des livres PDF vers XML...")
            parser = PDFCorpusParser(os.path.join(base_dir, "data/input"))
            parser.parse()
            parser.save(xml_raw_path)
            
            progress_bar.progress(15)
            log_container.info("Phase 2/4 : Tokenisation et filtrage des mots vides...")
            tokenizer = Tokenizer(xml_filepath=xml_raw_path, output_dir=td2_dir)
            tokenizer.export_stats()
            
            progress_bar.progress(30)
            log_container.info("Phase 3/4 : Racinisation (Stemming) avec NLTK...")
            stemmer_engine = Stemmer(xml_filtered_path, stem_mapping_path)
            stemmer_engine.run()
            tokenizer.export_stem_stats(stem_dict_file=stem_mapping_path, target_xml=xml_filtered_path, out_file=tfidf_path, filter_again=True)
            
            progress_bar.progress(45)
            log_container.info("Phase 4/4 : Génération de l'index inversé et des poids TF-IDF...")
            index_gen = InvertedIndexGenerator(xml_filepath=xml_final_path, output_dir=td3_dir)
            index_gen.generate()
            index_gen.export()
        except Exception as e:
            st.error(f"Erreur d'indexation classique : {e}")
            st.stop()
            
    progress_bar.progress(50)
    
    if not rag_ready:
        if not st.session_state.get("google_api_key"):
            log_container.warning("⚠️ La génération de la base vectorielle ChromaDB nécessite une clé API Gemini.")
            key_input = st.text_input("Veuillez saisir votre GOOGLE_API_KEY :", type="password", help="Cette clé est requise pour créer les embeddings.")
            if key_input:
                st.session_state["google_api_key"] = key_input
                os.environ["GOOGLE_API_KEY"] = key_input
                st.rerun()
            else:
                st.stop()
                
        log_container.info("Phase RAG : Génération de la base de données vectorielle ChromaDB (cela peut prendre quelques minutes)...")
        try:
            vstore_mgr = RAGVectorStore(persist_dir=rag_persist_dir)
            loader = PDFBookLoader(directory_path=pdf_dir)
            chunks = loader.load_and_split(st_logger=log_container.info)
            vstore_mgr.create_store(chunks, st_logger=log_container.info)
        except Exception as e:
            st.error(f"Erreur d'indexation RAG : {e}")
            st.stop()
            
    progress_bar.progress(100)
    log_container.success("Initialisation terminée ! Démarrage de l'interface...")
    import time
    time.sleep(1)
    st.rerun()

# ----------------- SIDEBAR CONFIGURATIONS -----------------

with st.sidebar:
    st.image("https://img.icons8.com/color/96/harry-potter.png", width=64)
    st.title("Hub Configuration")
    
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
        options=["gemini-3.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"],
        index=0,
        help="Sélectionnez le modèle LLM à utiliser pour la génération."
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
    st.markdown("""
    **Projet UTC LO17 / AI31**  
    *Printemps 2026*  
    Moteur classique de recherche & Système RAG sur les livres de Harry Potter.
    """)

# ----------------- MAIN TITLE HEADER -----------------

st.markdown("""
<div class="header-container">
    <h1 class="header-title">🪄 LO17 & RAG Intelligence Hub</h1>
    <p class="header-subtitle">Plateforme intégrée d'Indexation, de Recherche Booléenne et de Génération Augmentée par Récupération</p>
</div>
""", unsafe_allow_html=True)

# Define main navigation tabs
tab_rag, tab_classic = st.tabs(["🧙 Assistant RAG (Harry Potter)", "🔍 Moteur de Recherche Classique (Harry Potter)"])


# =====================================================================
# TAB 1: ASSISTANT RAG (HARRY POTTER)
# =====================================================================

with tab_rag:
    st.subheader("Système RAG sur le corpus de Harry Potter")
    st.write("Posez des questions sur le monde de Harry Potter en français. Le système ira chercher les sections pertinentes dans les livres originaux PDF et utilisera l'API Gemini pour générer des réponses fidèles, tout en vérifiant l'absence d'hallucinations.")
    
    if not st.session_state["google_api_key"]:
        st.warning("⚠️ Clé API Gemini manquante. Veuillez saisir votre GOOGLE_API_KEY dans la barre latérale pour activer le RAG.")
    else:
        # Vectorstore is already guaranteed to exist by global check
        with st.spinner("Chargement de la base vectorielle..."):
            vstore_mgr = RAGVectorStore(persist_dir=rag_persist_dir)
            vstore = vstore_mgr.load_store()
            rag_chain = HarryPotterRAGChain(vectorstore=vstore, model_name=rag_model, temperature=temperature)
            evaluator = RAGEvaluator(model_name=rag_model)
            
        # Chat history interface
        if "messages" not in st.session_state:
            st.session_state.messages = []
            
        # Render chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "sources" in message:
                    with st.expander("📖 Sources de contexte récupérées"):
                        for idx, doc in enumerate(message["sources"], 1):
                            src_name = os.path.basename(doc.metadata.get('source', 'Inconnu'))
                            page = doc.metadata.get('page', 'Inconnue')
                            st.markdown(f"**Source {idx}** | Livre: `{src_name}`, Page: `{page}`")
                            st.code(doc.page_content, language="text")
                if "evaluation" in message:
                    eval_data = message["evaluation"]
                    with st.expander("🛡️ Audit de Génération (Anti-Hallucination & Pertinence)"):
                        col_e1, col_e2 = st.columns(2)
                        with col_e1:
                            st.write("**Fidélité au Contexte (Faithfulness)**")
                            f_score = eval_data["faithfulness"].get("score", 0.0)
                            if f_score >= 0.8:
                                st.success(f"Score: {f_score:.2f} ({eval_data['faithfulness'].get('verdict', 'FIDELE')})")
                            else:
                                st.warning(f"Score: {f_score:.2f} ({eval_data['faithfulness'].get('verdict', 'HALLUCINATION')})")
                            st.write(f"*Justification:* {eval_data['faithfulness'].get('justification', '')}")
                        with col_e2:
                            st.write("**Pertinence de la Réponse**")
                            r_score = eval_data["relevance"].get("score", 0.0)
                            if r_score >= 0.8:
                                st.success(f"Score: {r_score:.2f}")
                            else:
                                st.warning(f"Score: {r_score:.2f}")
                            st.write(f"*Justification:* {eval_data['relevance'].get('justification', '')}")
                            
        # Prompt Input
        if prompt := st.chat_input("Posez votre question (ex: 'Qui est Rogue ?' ou 'Quel est le premier sortilège appris par Harry ?')"):
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Recherche et génération de la réponse..."):
                    response_data = rag_chain.query(prompt)
                    answer = response_data["answer"]
                    sources = response_data["source_documents"]
                    
                    st.markdown(answer)
                    
                    with st.expander("📖 Sources de contexte récupérées"):
                        for idx, doc in enumerate(sources, 1):
                            src_name = os.path.basename(doc.metadata.get('source', 'Inconnu'))
                            page = doc.metadata.get('page', 'Inconnue')
                            st.markdown(f"**Source {idx}** | Livre: `{src_name}`, Page: `{page}`")
                            st.code(doc.page_content, language="text")
                            
                    # Run evaluation
                    with st.spinner("Audit anti-hallucination en cours..."):
                        eval_res = evaluator.evaluate(prompt, answer, sources)
                        
                    with st.expander("🛡️ Audit de Génération (Anti-Hallucination & Pertinence)"):
                        col_e1, col_e2 = st.columns(2)
                        with col_e1:
                            st.write("**Fidélité au Contexte (Faithfulness)**")
                            f_score = eval_res["faithfulness"].get("score", 0.0)
                            if f_score >= 0.8:
                                st.success(f"Score: {f_score:.2f} ({eval_res['faithfulness'].get('verdict', 'FIDELE')})")
                            else:
                                st.warning(f"Score: {f_score:.2f} ({eval_res['faithfulness'].get('verdict', 'HALLUCINATION')})")
                            st.write(f"*Justification:* {eval_res['faithfulness'].get('justification', '')}")
                        with col_e2:
                            st.write("**Pertinence de la Réponse**")
                            r_score = eval_res["relevance"].get("score", 0.0)
                            if r_score >= 0.8:
                                st.success(f"Score: {r_score:.2f}")
                            else:
                                st.warning(f"Score: {r_score:.2f}")
                            st.write(f"*Justification:* {eval_res['relevance'].get('justification', '')}")
            
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

with tab_classic:
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


