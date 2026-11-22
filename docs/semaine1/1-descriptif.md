# Livrable 1 : descriptif du projet mis à jour

**Rédacteur :** Mohammed Amine Elkhaldy (`@elkhaldymohamed16-alt`) &emsp; **Relecteur :** Aymen Elhaimer (`@aymen-elhaimer`) &emsp; **Fichier :** `docs/semaine1/1-descriptif.md`

## 1.1 Contexte et problème

Les étudiants ingénieurs et les développeurs en entreprise doivent régulièrement retrouver des informations précises (règles d'architecture, conformité RGPD / loi 09-08, conventions API, procédures DevOps) réparties dans des dizaines de documents PDF et Markdown hétérogènes. Aujourd'hui, cette recherche se fait manuellement par `Ctrl+F` fichier par fichier, ce qui prend plusieurs minutes par question et expose à des oublis ou à des interprétations erronées sans traçabilité de la source exacte.

## 1.2 Objectif

Permettre à un utilisateur d'interroger en langage naturel un corpus de documents PDF et Markdown et d'obtenir en moins de 10 secondes une réponse synthétique accompagnée de citations exactes (document, section/page et extrait source).

## 1.3 Utilisateurs cibles et scénario d'usage principal

Les utilisateurs cibles sont les **ingénieurs logiciels, étudiants en data/IA et équipes techniques** qui consultent une base documentaire interne.

**Scénario principal :**
1. L'utilisateur ouvre l'interface web Streamlit et importe un ou plusieurs documents (PDF ou Markdown) dans le corpus via l'onglet « Ingestion » (ou utilise le corpus déjà indexé).
2. Le système découpe automatiquement les documents en passages (chunks), calcule leurs embeddings et les stocke dans la base vectorielle avec leurs métadonnées (nom de fichier, titre de section, numéro de page).
3. L'utilisateur saisit une question en langage naturel dans l'onglet « Recherche RAG » (ex. : *« Quelles obligations impose la loi 09-08 avant de traiter des données personnelles ? »*).
4. L'API FastAPI déclenche l'agent RAG qui récupère les passages les plus pertinents, vérifie le score de similarité, génère une réponse ancrée uniquement sur ces extraits et affiche la réponse avec les sources cliquables et un résumé de chaque source.
5. Si aucun passage ne dépasse le seuil de pertinence, l'agent s'abstient explicitement au lieu d'inventer une réponse.

## 1.4 Fonctionnalités du MVP

| N° | Fonctionnalité | Ce que l'utilisateur voit ou obtient | Priorité |
| --- | --- | --- | --- |
| F1 | Ingestion et indexation documentaire (`POST /ingest`) | Téléversement de fichiers PDF/Markdown, découpage en passages avec métadonnées et confirmation du nombre de passages indexés dans la base vectorielle | Indispensable |
| F2 | Question-réponse RAG avec citations et résumé des sources (`POST /ask`) | Une réponse structurée en français, la liste des références exactes (fichier, page/section, score de similarité), les extraits utilisés et un résumé concis par source (ou un message d'abstention si hors corpus) | Indispensable |
| F3 | Interface web de recherche et inspection des sources (Streamlit) | Une application web à trois vues (ingestion du corpus, interrogation RAG avec affichage des citations, inspection/évaluation des extraits) communiquant uniquement par HTTP avec l'API | Indispensable |

## 1.5 Services et composants techniques

| Service ou composant | Rôle dans le projet | Technologie choisie | Pourquoi ce choix |
| --- | --- | --- | --- |
| Modèle (LLM et embeddings) | Calcul des vecteurs sémantiques et génération de réponses ancrées en français | `sentence-transformers` (`paraphrase-multilingual-MiniLM-L12-v2`) + LLM via API OpenAI-compatible ou Ollama local (`qwen2.5` / `llama3.2`) | Embeddings multilingues légers sur CPU sans coût par appel ; abstraction LLM permettant de basculer entre modèle local et API sans changer le code |
| Recherche et mémoire | Stockage persistant des vecteurs et récupération des `top-k` passages | ChromaDB + LangChain | Base vectorielle embarquée sans infrastructure lourde, filtrage natif par métadonnées et intégration directe avec LangChain |
| Outils appelés par l'agent | Recherche sémantique, résumé des sources et contrôle de présence des citations | Outils Python typés (`search_documents`, `summarize_source`, `verify_citations`) | Séparation claire des responsabilités et vérification systématique que chaque citation correspond à un extrait réellement récupéré |
| API | Exposition REST (`/health`, `/ingest`, `/ask`) et validation des schémas | FastAPI + Pydantic v2 | Validation stricte des requêtes/réponses, documentation OpenAPI `/docs` automatique et cohérence directe avec l'architecture du cours |
| Interface | Application utilisateur de démonstration et d'inspection des sources | Streamlit + `httpx` | Prototypage rapide, découplage total vis-à-vis du moteur RAG et testabilité via `AppTest` |
| Conteneur et intégration continue | Exécution reproductible et contrôles automatiques | Docker, Docker Compose, GitHub Actions (`ruff`, `mypy`, `pytest`) | Déploiement identique sur tous les postes et prévention des régressions à chaque push |

## 1.6 Hors périmètre

- Reconnaissance optique de caractères (OCR) sur des PDF scannés ou des images.
- Gestion des comptes utilisateurs, authentification SSO et contrôle d'accès par document (RBAC).
- Synchronisation temps réel avec des sources externes propriétaires (SharePoint, Confluence, Google Drive).
- Fine-tuning de modèles de langage (le projet repose exclusivement sur le RAG).

## 1.7 Écart avec la fiche du catalogue

Ajout d'un **seuil d'abstention** (l'agent refuse de répondre lorsque la similarité maximale est insuffisante afin d'éliminer les hallucinations) et restriction aux formats textuels natifs (PDF texte, Markdown, TXT) pour garantir un MVP complet et testé en 4 semaines pour un binôme.

## Critères d'acceptation (vérifiés par le relecteur : Aymen Elhaimer)

- [x] Le problème et l'utilisateur sont compréhensibles sans le catalogue.
- [x] Le nombre de fonctionnalités correspond à la taille de l'équipe (3 fonctionnalités pour un binôme).
- [x] Chaque fonctionnalité est démontrable (pas de formulation vague comme « améliorer »).
- [x] Chaque composant technique a une justification d'une ligne.
- [x] Le hors périmètre est rempli.
