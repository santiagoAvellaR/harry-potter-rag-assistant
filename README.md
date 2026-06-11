# LO17 & RAG Intelligence Hub

Este projeto integra o **Moteur de Recherche d'Information** clássico (desenvolvido nos TDs 1 a 6 da disciplina LO17 na UTC) e um **Assistente de Perguntas & Respostas RAG (Retrieval-Augmented Generation)** baseado no universo de Harry Potter, utilizando a API do Gemini, LangChain, banco de dados vetorial ChromaDB e interface Streamlit.

---

## Estrutura do Projeto

A nova estrutura do projeto é organizada na raiz de forma modular:

```
RAG/
├── .env.example               # Exemplo de configuração de chaves (GOOGLE_API_KEY)
├── environment.yml            # Arquivo de ambiente Conda unificado
├── requirements.txt           # Dependências de execução via pip
├── app.py                     # Dashboard integrado Streamlit (Moteur clássico + RAG Harry Potter)
├── data/
│   ├── input/                 # PDFs originais de Harry Potter para RAG (Livros 1 a 7)
│   └── output/                # Ficheiros gerados pelos pipelines (indexadores, ChromaDB, etc.)
│       ├── TD1/               # XML gerado pelo parsing do Moteur
│       ├── TD2/               # Anti-dicionário e XML filtrado
│       ├── TD3/               # Stems e índices invertidos do Moteur
│       ├── evaluation/        # Resultados de testes e precisão/recall do Moteur
│       └── vectorstore/       # Banco de dados vetorial Chroma contendo os embeddings dos livros
└── src/                       # Código-fonte principal
    ├── research-engine/       # Backend do motor de busca clássico LO17 (stems, index, SQL)
    ├── RAG/                   # Módulos do pipeline RAG
    │   ├── loader_pdf.py      # Carregamento e particionamento dos PDFs
    │   ├── vectorstore.py     # Criação de embeddings e gerência do ChromaDB
    │   ├── chain.py           # Configuração de prompt e fluxo RAG (LangChain + Gemini)
    │   └── evaluation.py      # Avaliação de fidelidade/relevância e detecção de alucinações
    └── search_adapters/       # Adaptador para execução integrada do motor clássico
```

---

## Instalação e Configuração

### 1. Criar o Ambiente Conda

Crie o ambiente virtual a partir do arquivo unificado:

```bash
conda env create -f environment.yml
conda activate lo17-rag
```

Ou, se preferir criar manualmente com virtualenv:

```bash
python -m venv .venv
source .venv/bin/activate  # no Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download fr_core_news_sm
```

### 2. Configurar a Chave da API do Gemini

Duplique o arquivo `.env.example` para `.env` na raiz do projeto e insira sua chave da API do Gemini:

```env
GOOGLE_API_KEY=sua_chave_aqui
```

*Nota: Você também pode inserir a chave de API diretamente pela interface web da barra lateral no Streamlit.*

---

## Executando o Dashboard Streamlit

Para iniciar o painel web interativo completo:

```bash
streamlit run app.py
```

O dashboard estará disponível em `http://localhost:8501` e possui duas abas:
1. **Moteur de Recherche Classique (Bulletins ADIT):** Permite interagir com o motor clássico e inspecionar os logs de execução do backend detalhadamente.
2. **Assistant RAG (Harry Potter):** Chatbot para fazer perguntas sobre os livros de Harry Potter, exibir os trechos originais recuperados como contexto e auditar as respostas contra alucinações.

---

## Executando os Testes e Avaliações de LO17

Você pode rodar os scripts individuais de validação diretamente a partir da nova estrutura de diretórios:

### Verificação de Consultas do Backend
```bash
python src/research-engine/verify_backend_queries.py
```

### Pipeline de Avaliação Experimental (TD6)
```bash
python src/research-engine/evaluation.py --runs 100 --inspect --top 50
```

### Verificação de Checklist de Entrega
```bash
python src/research-engine/check_project.py
```

---

## Como Funciona o Pipeline RAG

1. **Leitura e Chunking (`loader_pdf.py`):** Carrega os 7 livros PDF localizados em `data/input/` e os divide em pedaços (chunks) de texto de 1000 caracteres com sobreposição de 200 caracteres.
2. **Embeddings e Armazenamento (`vectorstore.py`):** Os fragmentos são convertidos em vetores de alta dimensão usando o modelo `gemini-embedding-001` da Google e gravados na pasta `data/output/vectorstore/`.
3. **Recuperação e Geração (`chain.py`):** Ao fazer uma pergunta, o ChromaDB recupera os chunks mais semelhantes. Um prompt em francês envia a pergunta e o contexto ao modelo `gemini-3.5-flash` para elaborar a resposta.
4. **Audit de Hallucinations (`evaluation.py`):** Um mecanismo de "LLM-as-a-judge" avalia as respostas produzidas, medindo a **Fidelidade (Faithfulness)** ao contexto e a **Relevância** em relação à pergunta.