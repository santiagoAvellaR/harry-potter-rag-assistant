"""Adapters around production retrieval code. No app or generation-chain imports."""
from collections import Counter
import hashlib
import inspect
import json
import os
from pathlib import Path
import sys


def sha(data):
    return hashlib.sha256(data).hexdigest()


def chunk_key(doc):
    return (Path(doc.metadata['source']).name, doc.metadata['page'], sha(doc.page_content.encode()))


def prepare_vector(root, config, corpus, build=False):
    import numpy as np
    from huggingface_hub import snapshot_download
    from src.RAG.loader_pdf import PDFBookLoader
    from src.RAG.vectorstore import RAGVectorStore
    from langchain_community.vectorstores.utils import maximal_marginal_relevance
    model = config['embedding']
    snapshot = Path(snapshot_download(model['model'], revision=model['revision'], local_files_only=True))
    # Refuse a different cached revision rather than quietly loading new weights.
    current = Path(snapshot_download(model['model'], local_files_only=True))
    if snapshot.resolve() != current.resolve():
        raise ValueError('Cached default model revision differs from frozen configuration')
    model_files = {str(p.relative_to(snapshot)): sha(p.read_bytes())
                   for p in sorted(snapshot.rglob('*')) if p.is_file()}
    files = [b['source'] for b in corpus['books']]
    loader = PDFBookLoader(str(root / 'data/input'), selected_files=files)
    chunks = loader.load_and_split()
    index = root / config['chroma']['path']
    index_present = (index / 'chroma.sqlite3').exists()
    if not index_present and not build:
        raise FileNotFoundError('Index absent: explicitly use --build-index to rebuild current configuration')
    manager = RAGVectorStore(str(index), model_name=model['model'])
    if index_present:
        store = manager.load_store()
        origin = 'existing benchmark index; contents verified, prior creation process not independently known'
    else:
        index.mkdir(parents=True, exist_ok=True)
        # Chroma limits insertion batches; use production manager for first batch then append.
        store = manager.create_store(chunks[:1000])
        for i in range(1000, len(chunks), 1000):
            store.add_documents(chunks[i:i+1000])
        origin = 'fresh index built by production loader/embedding/store code; app index absent at inspection'
    data = store.get(include=['documents', 'metadatas', 'embeddings'])
    actual = Counter((Path(m['source']).name, m['page'], sha(t.encode()))
                     for m, t in zip(data['metadatas'], data['documents']))
    expected = Counter(chunk_key(d) for d in chunks)
    if actual != expected:
        raise ValueError('Index documents/page references do not exactly match re-extracted current chunks')
    metadata = store._collection.metadata
    if metadata.get('hnsw:space') != 'cosine':
        raise ValueError('Index is not cosine')
    # Check every stored vector against the current embedding weights, not just text metadata.
    emb = manager.embeddings
    max_error = 0.0
    for i in range(0, len(data['documents']), 128):
        fresh = np.asarray(emb.embed_documents(data['documents'][i:i+128]))
        saved = np.asarray(data['embeddings'][i:i+128])
        error = float(np.max(np.abs(fresh - saved)))
        max_error = max(max_error, error)
        if not np.allclose(fresh, saved, atol=1e-5, rtol=1e-5):
            raise ValueError('Index embedding mismatch')
    provenance = {'origin': origin, 'chunks': len(chunks), 'pages': len({k[:2] for k in actual}),
                  'corpus_document_hash': sha(json.dumps(sorted(actual.elements())).encode()),
                  'collection_metadata': metadata, 'embedding_revision': snapshot.name,
                  'model_file_sha256': model_files, 'all_vector_max_absolute_error': max_error,
                  'dimension': len(data['embeddings'][0]),
                  'mmr_library_lambda_default': inspect.signature(maximal_marginal_relevance).parameters['lambda_mult'].default,
                  'embedding_model_kwargs': emb.model_kwargs, 'embedding_encode_kwargs': emb.encode_kwargs,
                  'app_index_present': (root / 'data/output/vectorstore_fr/chroma.sqlite3').exists()}
    if provenance['mmr_library_lambda_default'] != config['chroma']['mmr']['lambda_mult']:
        raise ValueError('MMR library default differs from frozen config')
    # Leave lambda implicit, exactly as production chain does.
    mmr = store.as_retriever(search_type='mmr', search_kwargs={'k': 12, 'fetch_k': 50})
    cosine = store.as_retriever(search_type='similarity', search_kwargs={'k': 12})
    return {'mmr': mmr.invoke, 'cosine': cosine.invoke}, provenance


def prepare_classic(root, corpus, build=False):
    """Build missing app artifacts with the exact app sequence; return page results."""
    sys.path.insert(0, str(root / 'src/research_engine'))
    from src.research_engine.pdf_corpus_parser import PDFCorpusParser
    from src.research_engine.tokenizer import Tokenizer
    from src.research_engine.stemmer import Stemmer
    from src.research_engine.inverted_index import InvertedIndexGenerator
    from src.search_adapters.search_bridge import SearchEngineBridge
    from lxml import etree
    base = root / 'data/output'
    xml = base / 'TD1/xml.xml'
    td2, td3 = base / 'TD2', base / 'TD3'
    paths = [xml, td2/'anti_dic.txt', td3/'stem_nltk.txt', td3/'inverse_text.txt']
    existed = all(p.exists() for p in paths)
    if not existed:
        if not build:
            raise FileNotFoundError('Classical artifacts missing; use --build-index')
        if any(p.exists() for p in paths):
            raise ValueError('Refusing partial classical artifacts of unknown provenance')
        for d in [xml.parent, td2, td3]:
            d.mkdir(parents=True, exist_ok=True)
        parser = PDFCorpusParser(str(root/'data/input'), selected_files=[b['source'] for b in corpus['books']])
        parser.parse()
        parser.save(str(xml))
        tokenizer = Tokenizer(str(xml), str(td2))
        tokenizer.export_stats()
        Stemmer(str(td2/'xml_filtre.xml'), str(td3/'stem_nltk.txt')).run()
        tokenizer.export_stem_stats(str(td3/'stem_nltk.txt'), str(td2/'xml_filtre.xml'),
                                    str(td3/'finale_nltk.txt'), filter_again=True)
        generator = InvertedIndexGenerator(str(td3/'xml_filtre_2.xml'), str(td3))
        generator.generate()
        generator.export()
    # Verify original XML against a fresh production parser result, page by page.
    parser = PDFCorpusParser(str(root/'data/input'), selected_files=[b['source'] for b in corpus['books']])
    fresh = {n.findtext('id'): n.findtext('text') for n in parser.parse().findall('document')}
    saved = {n.findtext('id'): n.findtext('text') for n in etree.parse(str(xml)).getroot().findall('document')}
    if fresh != saved:
        raise ValueError('Classical corpus XML differs from supplied PDFs')
    receipt_path = base / 'eval/classic_build.json'
    if existed:
        if not receipt_path.exists():
            raise ValueError('Existing classical processed indexes have no verified build provenance')
        receipt = json.loads(receipt_path.read_text())
        if receipt['corpus'] != corpus['books']:
            raise ValueError('Classical build corpus receipt mismatch')
        for name, fingerprint in receipt['artifacts'].items():
            if sha((root/name).read_bytes()) != fingerprint:
                raise ValueError('Classical artifact fingerprint mismatch')
        for name, fingerprint in receipt['code'].items():
            if sha((root/name).read_bytes()) != fingerprint:
                raise ValueError('Classical build code mismatch')
    bridge = SearchEngineBridge()
    sources = {b['book']: b['source'] for b in corpus['books']}

    def retrieve(question):
        result = bridge.search(question)
        # Production sorts by score only over a set; explicit numeric tie ordering makes ties repeatable.
        ranked = sorted(result['results'], key=lambda r: (-r['score'], int(r['id'])))[:12]
        docs = []
        from langchain_core.documents import Document
        for row in ranked:
            code = int(row['id'])
            docs.append(Document(page_content=bridge.engine.doc_texts[row['id']],
                metadata={'source': sources[code//1000], 'page': code % 1000 - 1,
                          'classic_score': row['score']}))
        return docs
    artifact_hashes = {str(p.relative_to(root)): sha(p.read_bytes())
                       for d in [xml.parent, td2, td3] for p in sorted(d.glob('*')) if p.is_file()}
    code = {str(p.relative_to(root)): sha(p.read_bytes()) for p in sorted((root/'src/research_engine').glob('*.py'))}
    receipt_path.write_text(json.dumps({'corpus': corpus['books'], 'artifacts': artifact_hashes, 'code': code}, indent=2)+'\n')
    return retrieve, {'origin': 'fresh production TD1->TD3 build', 'pages': len(saved),
                      'artifact_sha256': artifact_hashes, 'scoring': 'BM25-inspired, k1=1.2, no length normalization; title weight=3',
                      'candidate_filter': 'production natural-language parsing, spell correction and boolean filters',
                      'tie_break': 'ascending numeric ID after descending production score'}
