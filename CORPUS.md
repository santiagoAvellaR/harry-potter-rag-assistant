# Corpus and Data Policy

This project was tested on seven French Harry Potter novels as an academic RAG / Information Retrieval prototype.

The source novels are not distributed with the public repository. Users must provide their own legally obtained PDFs in `data/input/` before running the application.

Expected local structure:

```text
data/
├── input/
│   ├── .gitkeep
│   └── your-legally-obtained-documents.pdf
└── output/
    └── .gitkeep
```

The code scans `data/input/` for files ending in `.pdf`. For the Harry Potter corpus-specific metadata, `src/research_engine/pdf_corpus_parser.py` detects book numbers from filenames containing a digit from `1` to `7`, including names like `harry-potter-1-...pdf`. Files whose book number cannot be detected are skipped by the classical XML parser.

Generated XML, token files, inverted indexes, and vector stores are rebuilt locally from the PDFs when the application initializes. No copyrighted download links are provided by this repository.

Generated files under `data/output/` may contain extracted text, inverted indexes, or vector database artifacts derived from the source documents. These files should normally stay local and should not be published unless redistribution rights and privacy constraints are explicitly verified.

Before publishing this repository, check that Git is not tracking:

- Source PDFs or other copyrighted corpus files.
- Extracted XML/text files containing novel content.
- Generated token, stem, TF/IDF, or inverted-index files derived from the novels.
- Persisted ChromaDB/vectorstore files.
- `.env` files or API credentials.
