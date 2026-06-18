# 🪄 LO17 & RAG Intelligence Hub

Ce projet intègre de manière modulaire et interactive deux grands paradigmes de la recherche d'information :
1. **Un Moteur de Recherche Classique (Booléen & Vectoriel)** : Développé dans le cadre des travaux dirigés (TDs 1 à 6) de l'unité d'enseignement **LO17** à l'UTC (Université de Technologie de Compiègne). Ce moteur a été entièrement adapté pour indexer, analyser et interroger l'intégralité des livres de la saga *Harry Potter*.
2. **Un Assistant RAG (Retrieval-Augmented Generation) Hybride** : Un agent conversationnel intelligent qui s'appuie sur le framework **LangChain**. Contrairement aux approches cloud standard, ce projet utilise une approche **hybride locale/cloud** : 
   - **Embeddings Locaux :** Génération des vecteurs hors ligne via `sentence-transformers` et `langchain-huggingface` (modèle `paraphrase-multilingual-MiniLM-L12-v2`), garantissant rapidité, respect de la confidentialité et absence de limites de requêtes (rate limits).
   - **Génération Cloud :** Les modèles de pointe **Google Gemini** (via l'API Gemini) sont sollicités uniquement pour la génération de la réponse finale basée sur le contexte récupéré dans la base vectorielle locale **ChromaDB**.
   - **Audit Anti-Hallucination :** Un module d'évaluation automatique des réponses ("LLM-as-a-judge") valide la pertinence et la fidélité de chaque réponse au contexte.

L'ensemble du projet est piloté par une interface utilisateur unifiée, dynamique et élégante développée avec **Streamlit**, offrant des visualisations de logs en temps réel, un tableau de bord d'audit des réponses, une sélection personnalisée de livres, et un processus d'initialisation transparent et résilient.

---

## 📂 Structure du Projet

L'organisation des répertoires a été conçue pour séparer proprement le code source, les données d'entrée, les fichiers d'indexation générés et l'interface utilisateur.

```text
RAG/
├── .env.example               # Modèle de configuration des variables d'environnement (ex: GOOGLE_API_KEY)
├── environment.yml            # Fichier de configuration de l'environnement virtuel Conda (unifié)
├── requirements.txt           # Dépendances Python pour une installation via pip
├── app.py                     # Point d'entrée de l'application web Streamlit (Hub intégré)
├── data/
│   ├── input/                 # Contient les documents PDF originaux (Livres de Harry Potter)
│   └── output/                # Fichiers de sortie générés automatiquement par les pipelines
│       ├── TD1/, TD2/, TD3/   # Fichiers XML, dictionnaires et index inversés du moteur classique
│       ├── evaluation/        # Données et statistiques d'évaluation
│       ├── selected_books.json# Fichier de persistance pour les livres sélectionnés par l'utilisateur
│       └── vectorstore_local/ # Fichiers de la base de données vectorielle ChromaDB avec embeddings locaux
└── src/                       # Code source de l'application
    ├── research_engine/       # Composants du moteur de recherche classique LO17
    │   ├── pdf_corpus_parser.py  # Extraction de texte des PDF vers XML (supporte le filtrage de livres)
    │   ├── tokenizer.py          # Tokenisation et filtrage
    │   ├── stemmer.py            # Racinisation (stemming) en français (NLTK)
    │   ├── xml_builder.py        # Outils de manipulation de fichiers XML
    │   ├── inverted_index.py     # Construction de l'index inversé
    │   ├── moteur.py             # Moteur de recherche et exécution des requêtes booléennes
    │   ├── spell_checker.py      # Suggestion et correction orthographique (Levenshtein)
    │   └── ...
    ├── RAG/                   # Composants du pipeline de génération augmentée (RAG)
    │   ├── loader_pdf.py      # Chargement et découpage intelligent (chunking) des livres PDF filtrés
    │   ├── vectorstore.py     # Génération des embeddings (HuggingFace) et persistance avec ChromaDB
    │   ├── chain.py           # Orchestration de la chaîne RAG avec LangChain et l'API Gemini
    │   └── evaluation.py      # Audit de fidélité et pertinence ("LLM-as-a-judge")
    └── search_adapters/       # Adaptateurs pour la communication entre le backend classique et l'UI
```

---

## 🛠️ Installation et Configuration

### 1. Cloner le Projet
Assurez-vous de disposer de l'intégralité des fichiers du projet sur votre machine locale.

### 2. Placer les Documents de Référence
Déposez les fichiers PDF correspondant aux livres de *Harry Potter* dans le répertoire suivant :
`data/input/` (les fichiers doivent être au format PDF, par exemple `HP1.pdf`, `HP2.pdf`, etc.).

### 3. Créer l'Environnement Virtuel

#### Option A : Avec Anaconda / Miniconda (Recommandé)
Créez et configurez l'environnement à l'aide du fichier de configuration unifié `environment.yml` :
```bash
conda env create -f environment.yml
conda activate rag
```

#### Option B : Avec virtualenv et pip
Si vous préférez utiliser l'outil standard `pip`, exécutez les commandes suivantes :
```bash
# Création et activation de l'environnement virtuel
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS / Linux

# Installation des dépendances
pip install -r requirements.txt
python -m spacy download fr_core_news_sm
```

### 4. Configuration de l'API
Copiez le fichier `.env.example` vers `.env` et ajoutez votre clé API Google Gemini :
```env
GOOGLE_API_KEY="votre_clé_api_ici"
```
*(Note : La clé API est uniquement utilisée pour la génération de texte, réduisant ainsi considérablement les risques de dépassement de quota (Rate Limit) puisque la lourde tâche d'embedding vectoriel est réalisée localement).*

---

## 🚀 Lancement de l'Application

Pour lancer l'interface web interactive Streamlit :

```bash
streamlit run app.py
```

L'interface s'ouvrira automatiquement dans votre navigateur par défaut à l'adresse suivante : `http://localhost:8501`.

### Fonctionnalités de Démarrage Avancées

1. **Sélection de Livres :** Lors du tout premier lancement, ou si la base est vide, une interface de sélection s'affiche. Elle vous permet de cocher spécifiquement quels livres vous souhaitez indexer parmi les PDF disponibles. Cela réduit le temps de calcul et vous permet de vous concentrer sur un sous-ensemble d'œuvres si désiré.
2. **Processus d'Initialisation Dynamique :** Une fois les livres sélectionnés, un écran de chargement affiche les étapes d'initialisation en temps réel avec des animations :
   - **Moteur Classique :** Parsing PDF vers XML, Tokenisation, Stemming, et création des Index inversés.
   - **Assistant RAG :** Découpage du texte en chunks et génération des vecteurs 100% localement via `HuggingFace`. Les vecteurs sont ensuite stockés dans `ChromaDB`.
3. **Résilience et Tolérance aux Pannes :** Si jamais la configuration de l'IA (RAG) rencontre un problème (par exemple : clé API invalide, absence de connexion internet), l'application ne plante pas ! Un mode dégradé s'active et vous permet d'accéder au **Moteur de Recherche Classique** tout en affichant un message explicatif clair sur la raison de l'indisponibilité du RAG.

---

## 💻 Utilisation du Hub Streamlit

L'interface est structurée en deux onglets principaux :

### 1. 🧙 Onglet : Assistant RAG (Harry Potter)
Cet espace prend la forme d'un chatbot interactif intelligent.
* **Questions Naturelles :** Posez des questions en français (ex: *"Qu'est-ce que l'Armée de Dumbledore ?"*). L'agent utilisera les vecteurs locaux pour trouver les passages pertinents, puis interrogera l'API Gemini pour rédiger une réponse cohérente.
* **Transparence des Sources :** Pour chaque réponse, un panneau affiche les passages exacts récupérés dans les livres.
* **Audit Anti-Hallucination :** Un score de **Fidélité (Faithfulness)** et de **Pertinence (Answer Relevance)** est généré pour chaque réponse, afin d'assurer que l'IA ne s'est pas inventé des détails en dehors des livres.

### 2. 🔍 Onglet : Moteur de Recherche Classique (Harry Potter)
Une adaptation visuelle du moteur de recherche TD (Traitement Documentaire).
* **Requêtes Booléennes et Flexibles :** Cherchez des termes spécifiques en utilisant la syntaxe du moteur (incluant le traitement de l'orthographe via la distance de Levenshtein).
* **Analyse et Logs :** Observez dans le terminal visuel intégré comment le moteur interprète votre requête, l'équation booléenne générée, et les calculs de pondération TF-IDF pour lister les résultats les plus pertinents.

---
**Note de Développement :** Ce projet a été préparé pour être intégré à un dépôt Git professionnel (utilisation de `.gitignore` ciblant les données générées et clés sensibles) et intègre des bibliothèques robustes d'Intelligence Artificielle en Python (`langchain`, `sentence-transformers`, `chromadb`).