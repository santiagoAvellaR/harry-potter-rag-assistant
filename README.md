# 🪄 LO17 & RAG Intelligence Hub

Ce projet intègre de manière modulaire et interactive deux grands paradigmes de la recherche d'information :
1. **Un Moteur de Recherche Classique (Booléen & Vectoriel)** : Développé dans le cadre des travaux dirigés (TDs 1 à 6) de l'unité d'enseignement **LO17** à l'UTC (Université de Technologie de Compiègne). Ce moteur a été entièrement adapté pour indexer, analyser et interroger l'intégralité des livres de la saga *Harry Potter*.
2. **Un Assistant RAG (Retrieval-Augmented Generation)** : Un agent conversationnel intelligent qui s'appuie sur le framework **LangChain**, les modèles de pointe **Google Gemini** (via l'API Gemini), la base de données vectorielle **ChromaDB** et un module d'évaluation automatique des hallucinations ("LLM-as-a-judge").

L'ensemble du projet est piloté par une interface utilisateur unifiée, dynamique et élégante développée avec **Streamlit**, offrant des visualisations de logs en temps réel, un tableau de bord d'audit des réponses et un processus d'initialisation transparent.

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
│   ├── input/                 # Contient les documents PDF originaux (Livres de Harry Potter 1 à 7)
│   └── output/                # Fichiers de sortie générés automatiquement par les pipelines
│       ├── TD1/               # Fichier XML brut issu du parsing initial des livres
│       ├── TD2/               # Anti-dictionnaire (mots vides) et fichier XML filtré
│       ├── TD3/               # Stems (racines), dictionnaires et index inversés finaux
│       ├── evaluation/        # Données et statistiques d'évaluation (Précision/Rappel) du moteur classique
│       └── vectorstore/       # Fichiers de la base de données vectorielle ChromaDB
└── src/                       # Code source de l'application
    ├── research_engine/       # Composants du moteur de recherche classique LO17
    │   ├── pdf_corpus_parser.py  # Extraction de texte des PDF et structuration au format XML
    │   ├── tokenizer.py          # Tokenisation, filtrage des stopwords et statistiques
    │   ├── stemmer.py            # Racinisation (stemming) en s'appuyant sur NLTK (règles françaises)
    │   ├── xml_builder.py        # Outils de manipulation de fichiers XML
    │   ├── inverted_index.py     # Construction de l'index inversé et calcul des poids TF-IDF
    │   ├── moteur.py             # Moteur de recherche et exécution des requêtes booléennes
    │   ├── traitement_requete.py # Analyse syntaxique, correction orthographique et extraction de métadonnées
    │   ├── spell_checker.py      # Module de suggestion et correction orthographique (distance de Levenshtein)
    │   ├── evaluation.py         # Outil d'évaluation des performances du moteur classique (TD6)
    │   ├── check_project.py      # Script de vérification de l'intégrité de la structure et des fichiers requis
    │   └── verify_backend_queries.py # Script de validation des requêtes SQL et logiques en console
    ├── RAG/                   # Composants du pipeline de génération augmentée (RAG)
    │   ├── loader_pdf.py      # Chargement et découpage intelligent (chunking) des livres PDF
    │   ├── vectorstore.py     # Génération des embeddings et persistance avec ChromaDB
    │   ├── chain.py           # Orchestration de la chaîne RAG avec LangChain et l'API Gemini
    │   └── evaluation.py      # Audit de fidélité et pertinence ("LLM-as-a-judge" anti-hallucination)
    └── search_adapters/       # Adaptateurs pour la communication entre le backend classique et l'UI
        └── search_bridge.py   # Passerelle convertissant les requêtes utilisateurs en commandes LO17
```

---

## 🛠️ Installation et Configuration

### 1. Cloner le Projet
Assurez-vous de disposer de l'intégralité des fichiers du projet sur votre machine locale.

### 2. Placer les Documents de Référence
Déposez les fichiers PDF correspondant aux 7 livres de *Harry Potter* dans le répertoire suivant :
`data/input/` (les fichiers doivent être nommés ou structurés pour être reconnus, par exemple `HP1.pdf`, `HP2.pdf`, etc.).

### 3. Créer l'Environnement Virtuel

#### Option A : Avec Anaconda / Miniconda (Recommandé)
Créez et configurez l'environnement à l'aide du fichier de configuration unifié `environment.yml` :
```bash
conda env create -f environment.yml
conda activate lo17-rag
```

#### Option B : Avec virtualenv et pip
Si vous préférez utiliser l'outil standard `pip`, exécutez les commandes suivantes :
```bash
# Création de l'environnement virtuel
python -m venv .venv

# Activation de l'environnement
# Sur Windows :
.venv\Scripts\activate
# Sur macOS / Linux :
source .venv/bin/activate

# Installation des dépendances
pip install -r requirements.txt

# Téléchargement du modèle de langue SpaCy pour le français
python -m spacy download fr_core_news_sm
```


## 🚀 Lancement de l'Application

Pour lancer l'interface web interactive Streamlit :

```bash
streamlit run app.py
```

L'interface s'ouvrira automatiquement dans votre navigateur par défaut à l'adresse suivante : `http://localhost:8501`.

### L'Écran d'Initialisation Automatique (Loading Screen)
Lors du premier lancement (ou si certains fichiers requis sont manquants dans `data/output/`), l'application bascule sur un **écran de chargement bloquant**.
Cet écran exécute pas à pas l'ensemble des tâches de traitement et affiche la progression en temps réel à l'utilisateur :
- **Moteur Classique :**
  1. *Phase 1/4 :* Parsing de tous les PDFs de Harry Potter présents dans `data/input/` pour générer un fichier XML consolidé (`data/output/TD1/xml.xml`).
  2. *Phase 2/4 :* Tokenisation (découpage en mots), suppression de la ponctuation, conversion en minuscules et application de l'anti-dictionnaire pour filtrer les mots vides.
  3. *Phase 3/4 :* Racinisation (Stemming) à l'aide de NLTK pour associer chaque terme à sa racine morphologique en français.
  4. *Phase 4/4 :* Construction des index inversés et des dictionnaires finaux avec calcul des fréquences de termes (TF-IDF).
- **RAG (Assistant IA) :**
  - Si la base vectorielle ChromaDB n'existe pas, l'application vous invite à saisir votre clé API Gemini (si non fournie dans le `.env`).
  - L'application procède alors au découpage des livres en segments de texte (chunks), calcule leurs vecteurs de caractéristiques (embeddings) via le modèle `gemini-embedding-001` et les sauvegarde dans la base vectorielle persistante (`data/output/vectorstore/`).

Une fois toutes ces étapes complétées avec succès, la page se recharge automatiquement et donne accès à l'interface de recherche.

---

## 💻 Fonctionnalités du Hub Streamlit

L'interface est structurée en deux onglets principaux :

### 1. 🧙 Onglet : Assistant RAG (Harry Potter)
Cet espace prend la forme d'un chatbot de discussion interactif.
* **Saisie de Questions :** Vous pouvez poser des questions en français sur des détails précis des livres (ex: *"Qui a donné la cape d'invisibilité à Harry ?"* ou *"Qu'est-ce que l'Armée de Dumbledore ?"*).
* **Affichage des Sources :** Pour chaque réponse fournie par l'IA, un panneau rétractable affiche les extraits originaux du livre récupérés dans la base vectorielle ChromaDB (indiquant le nom du livre et le paragraphe d'origine).
* **Audit Anti-Hallucination :** L'application intègre un évaluateur automatique de réponses :
  * **Fidélité (Faithfulness) :** Évalue (sur une échelle de 0 à 1) si l'affirmation formulée par l'IA est strictement supportée par les documents sources récupérés (évite les inventions).
  * **Pertinence (Answer Relevance) :** Mesure si la réponse répond effectivement à la question posée.
  * Les logs d'évaluation détaillés s'affichent sous chaque réponse, assurant une transparence totale.

### 2. 🔍 Onglet : Moteur de Recherche Classique (Harry Potter)
Il s'agit de l'adaptation visuelle du moteur de recherche conçu lors des TDs de LO17.
* **Requêtes en Langage Naturel ou Booléen :** Tapez une requête comme *"sortilège de protection contre les forces du mal"* ou utilisez des opérateurs.
* **Extraction automatique de Métadonnées :** Le moteur isole automatiquement les critères de filtrage (titre, auteur, date, etc.).
* **Racinisation et Correction :** La requête est normalisée (stems) et un correcteur d'orthographe dynamique basé sur la distance de Levenshtein propose des alternatives en cas de mot mal orthographié.
* **Tri des Résultats :** Les résultats peuvent être triés par pertinence (score TF-IDF), par ordre chronologique ou antichronologique.
* **Affichage des correspondances :** Les extraits de livres correspondants sont affichés avec une mise en évidence visuelle (surlignage en gras) des termes recherchés.
* **Terminal de Logs :** Un panneau dédié affiche le déroulement des opérations internes du moteur classique (requête nettoyée, équation logique générée, arbres d'évaluation, temps d'exécution SQL/Index).

---