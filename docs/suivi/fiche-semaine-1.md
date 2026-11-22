# Fiche de suivi, semaine 1 : cadrage et lancement du projet

## 1. Identification du groupe

| Élément | Votre réponse |
| --- | --- |
| Nom du groupe | Binôme G3 — Amine & Aymen |
| Titre du projet | Agent de recherche documentaire |
| Sujet : numéro du catalogue, ou « hors catalogue » | N°1 (Connaissance et RAG) |
| Adresse du dépôt GitHub | https://github.com/elkhaldymohamed16-alt/agent-recherche-documentaire |
| Enseignant ajouté au dépôt (oui ou non) | oui (`ia.dev.dep@gmail.com` / `larhlimi-ia`) |
| Date de remise de la fiche | 22/11/2026 |

Membres du groupe :

| Nom et prénom | Compte GitHub | Rôle principal dans le projet |
| --- | --- | --- |
| Mohammed Amine Elkhaldy | `@elkhaldymohamed16-alt` | Coordinateur, architecture RAG, squelette agent, API FastAPI et interface Streamlit |
| Aymen Elhaimer | `@aymen-elhaimer` | Dataset, ingestion PDF/Markdown, jeu d'évaluation, tests et conteneurisation Docker |

## 2. Sujet et besoin

| Question | Votre réponse |
| --- | --- |
| Besoin en une phrase | Interroger en langage naturel un corpus de documents techniques et réglementaires (PDF et Markdown) et obtenir une réponse synthétique accompagnée de ses citations exactes. |
| Utilisateur final : qui se sert de l'application | Les étudiants ingénieurs, développeurs et équipes techniques qui recherchent rapidement des règles d'architecture, procédures ou textes réglementaires dans une base interne. |
| Ce que fait l'application, vu par l'utilisateur (3 lignes au plus) | L'utilisateur dépose ses documents PDF/Markdown (ou utilise le corpus indexé), pose une question en français et reçoit une réponse ancrée uniquement dans les extraits récupérés, avec le nom du fichier, la section et un résumé par source ; si la question sort du corpus, l'agent s'abstient explicitement. |
| Approche retenue (règles, apprentissage, RAG, agent) et raison du choix | **Agent RAG** : (b) chaque réponse doit être vérifiable par citation exacte de la source, (a) aucune base de questions-réponses étiquetées n'existe pour entraîner un classifieur supervisé, et un LLM seul risquerait d'halluciner des références inexistantes. |
| Conséquence d'une erreur de l'application, et validation humaine prévue | Une réponse erronée ou non sourcée peut induire une mauvaise décision technique ou de conformité. L'interface affiche toujours les extraits originaux cités et les scores de similarité pour permettre une vérification immédiate par l'utilisateur, et renvoie une abstention sous le seuil de confiance. |
| Sujet hors catalogue : projet du catalogue auquel il est comparable | Non applicable (sujet N°1 issu directement du catalogue officiel). |

## 3. Périmètre

| Rubrique | Votre réponse |
| --- | --- |
| Version minimale : le parcours que vous montrerez en semaine 2 | Un utilisateur interroge les documents de `data/sample/` via l'interface Streamlit connectée à l'API FastAPI (`/ask`) et obtient une réponse sourcée avec citations et abstention sur les questions hors corpus, mesurée sur le jeu de 20 questions. |
| Fonction 1, indispensable | Ingestion et indexation de documents PDF texte et Markdown (`POST /ingest`) avec découpage en passages et conservation des métadonnées (`source`, `section`, `page`). |
| Fonction 2, indispensable | Recherche sémantique et génération de réponse RAG (`POST /ask`) avec citations vérifiées, résumé des sources et seuil d'abstention hors corpus. |
| Fonction 3, si le temps le permet | Interface Streamlit à trois onglets (ingestion, recherche avec citations, inspection des extraits) et conteneurisation Docker Compose avec CI GitHub Actions. |
| Hors périmètre : ce que vous ne ferez pas | OCR sur PDF scannés ou images, authentification SSO/RBAC multi-utilisateurs, synchronisation temps réel SharePoint/Google Drive et fine-tuning de LLM. |

## 4. Architecture et technologies

| Composant | Choix prévu | Dossier ou fichier dans le dépôt |
| --- | --- | --- |
| Cœur : modèle, agent ou chaîne RAG | Extraction `pypdf`/UTF-8, baseline TF-IDF (`scikit-learn`) en S1 puis embeddings `sentence-transformers` + ChromaDB + LLM en S2 | `src/agent.py` |
| API | FastAPI + Pydantic v2 (`/health`, `/ingest`, `/ask`) | `api/` (prévu en S2-3) |
| Interface | Streamlit + `httpx` (découplée de la logique RAG) | `ui/` (prévu en S2-4) |
| Données et stockage | Fichiers `.md` / `.pdf` dans `data/sample/`, index persistant ChromaDB (`chroma_db/` hors Git) | `data/sample/`, `src/stats_dataset.py` |
| Tests | `pytest` (tests unitaires, cas limites, jeu d'évaluation de 20 questions) et `ruff` | `tests/test_smoke.py` |
| Services externes et clés nécessaires | Optionnel : API LLM OpenAI-compatible ou Ollama local (`LLM_API_KEY` dans `.env`, jamais commité ; `.env.example` versionné) | `.env.example` |

Schéma d'architecture dans le dépôt : [`docs/architecture.png`](../architecture.png) (et diagramme Mermaid dans [`README.md`](../../README.md)).

## 5. Données

| Question | Votre réponse |
| --- | --- |
| Origine des données (source, licence) | Guides techniques et réglementaires rédigés pour le projet (CC BY 4.0) complétés par les documentations publiques FastAPI (MIT) et scikit-learn (BSD-3-Clause) |
| Volume disponible aujourd'hui | 5 documents (3 Markdown, 2 PDF natifs), 20 passages, 807 mots + 20 questions d'évaluation |
| Format | `.md` (UTF-8), `.pdf` (texte natif PDF 1.4), `.json` (jeu d'évaluation) |
| Données personnelles : non, ou oui avec la méthode d'anonymisation | Non : aucune donnée personnelle ni confidentielle (corpus 100 % public et synthétique). |
| Jeu d'essai versionné dans le dépôt : chemin du fichier ou du script | `data/sample/` (5 documents + `jeu_test_20_questions.json`) et `src/stats_dataset.py` |

### Description du jeu de données

Vue d'ensemble (chiffres calculés par `python src/stats_dataset.py`) :

| Caractéristique | Votre réponse |
| --- | --- |
| Ce que représente une ligne (ou un document) | Un document technique ou réglementaire découpé en passages (sections), et une entrée du fichier JSON représente une question d'évaluation avec sa source attendue |
| Nombre de lignes ou de documents | 5 documents (20 passages indexables) et 20 questions de test |
| Nombre de variables (colonnes) | 3 champs par passage (`source`, `section`, `texte`) ; 5 champs par question (`id`, `question`, `source_attendue`, `section`, `type`) |
| Période couverte et langue | 2025–2026, français |
| Variable cible ou réponse attendue, s'il y en a une | `source_attendue` et `section` (ou `ABSTENTION (hors corpus)` pour les questions hors périmètre) |
| Répartition de la cible : effectif par classe, ou minimum, moyenne et maximum | Répartition des 20 questions par type : factuelle: 13, hors-corpus: 1, pdf: 5, synthese: 1 |
| Pour un corpus de textes : longueur moyenne d'un document, en mots | 161.4 mots en moyenne (807 mots au total) |
| Valeurs manquantes et doublons : nombre et traitement prévu | 0 valeur manquante, 0 doublon de passage ; normalisation des sauts de ligne PDF avant découpage |
| Découpage prévu : entraînement, test, évaluation | Pas d'entraînement supervisé (RAG) : 100 % des documents sont indexés ; l'évaluation porte sur le jeu indépendant de 20 questions |
| Script qui recalcule ces chiffres : chemin dans le dépôt | `src/stats_dataset.py` |

Dictionnaire des variables (`data/sample/jeu_test_20_questions.json` et structure `Passage`) :

| Variable | Type | Signification | Exemple de valeur | Valeurs manquantes (%) |
| --- | --- | --- | --- | --- |
| `id` | nombre | Identifiant unique de la question | `1` | 0 % |
| `question` | texte | Question en langage naturel posée à l'agent | `Quelle autorité supervise la loi 09-08 au Maroc ?` | 0 % |
| `source_attendue` | catégorie | Nom du document source attendu (ou abstention) | `03-conformite-loi-09-08-rgpd.md` | 0 % |
| `section` | texte | Section précise attendue dans le document | `Section 1` | 0 % |
| `type` | catégorie | Catégorie de difficulté du cas de test | `factuelle`, `pdf`, `synthese`, `hors-corpus` | 0 % |

Trois exemples tirés du jeu de données :

| Exemple (entrée) | Réponse ou étiquette attendue | Nature de l'exemple |
| --- | --- | --- |
| `Quelle autorité supervise l'application de la loi 09-08 au Maroc ?` | `03-conformite-loi-09-08-rgpd.md` — Section 1 (CNDP) | Cas simple |
| `Comment combiner les règles d'architecture découplée et Docker Compose pour déployer l'interface et l'API ?` | `01-guide-mlops-architecture.md` + `05-guide-docker-deploiement.pdf` | Cas difficile (multi-sources) |
| `Quelle est la météo prévue demain à Casablanca ?` | `ABSTENTION (hors corpus)` | Cas limite (hors corpus) |

Limites connues du jeu de données : l'échantillon de semaine 1 reste volontairement compact (5 documents, 807 mots) pour permettre des tests rapides et déterministes ; il sera étendu en semaine 2 (25 à 40 documents) pour tester la montée en charge et la précision du retrieval sur un corpus plus large.

## 6. Critères de réussite

| Critère | Mesure | Valeur cible | Comment vous le vérifierez |
| --- | --- | --- | --- |
| Précision de récupération (`Recall@3`) | Part des questions du corpus dont la source attendue figure dans le top-3 retourné | >= 90 % (au moins 18 sur 19 questions du corpus) | Script d'évaluation automatique sur `data/sample/jeu_test_20_questions.json` |
| Fidélité des citations et abstention | 0 citation inventée et 100 % d'abstention sur les questions hors corpus | 0 hallucination de source, 100 % abstention hors corpus | Tests automatisés dans `tests/test_smoke.py` puis `tests/test_evaluation.py` |
| Latence et fiabilité de l'API | Temps de réponse moyen de `POST /ask` et taux de réussite des tests + CI | Latence < 2 s (local) / < 10 s (LLM), 100 % des tests verts et Ruff muet | `pytest -q`, `ruff check .` et GitHub Actions |

## 7. Répartition et planning sur 3 semaines

| Semaine | Livrable attendu | Pour votre projet, concrètement | Responsable | Tag |
| --- | --- | --- | --- | --- |
| 1 | Cadrage, dépôt initialisé, squelette exécutable | Pushs S1-1 à S1-6, échantillon 5 docs + 20 questions, `src/agent.py`, `src/stats_dataset.py`, `pytest` vert, fiche semaine 1 | Mohammed Amine Elkhaldy & Aymen Elhaimer | `s1` |
| 2 | Version minimale qui fonctionne de bout en bout | Pushs S2-1 à S2-6 : moteur RAG complet, script d'évaluation (`docs/evaluation.md`), API FastAPI (`/health`, `/ingest`, `/ask`), interface Streamlit, CI Ruff+pytest | Mohammed Amine Elkhaldy (API/UI) & Aymen Elhaimer (RAG/Eval/CI) | `s2` |
| 3 | Application finale, documentation, compte rendu | Pushs S3-1 à S3-6 : cas limites, évaluation finale, Docker Compose reproductible sur clone neuf, `CHANGELOG.md`, rapport LaTeX (`docs/rapport/`), release | Mohammed Amine Elkhaldy & Aymen Elhaimer | `v1.0.0` |

Répartition des responsabilités :

| Membre | Responsabilités sur les 3 semaines | Remplaçant en cas d'absence |
| --- | --- | --- |
| Mohammed Amine Elkhaldy | Coordination, architecture, moteur RAG (`src/agent.py`), API FastAPI, interface Streamlit, rapport final | Aymen Elhaimer |
| Aymen Elhaimer | Corpus et ingestion PDF/MD, statistiques, évaluation sur les 20 questions, tests limites, Docker et CI GitHub Actions | Mohammed Amine Elkhaldy |

## 8. Travail réalisé en semaine 1

| Membre | Ce que j'ai fait cette semaine | Lien vers mes commits | Temps passé (heures) |
| --- | --- | --- | --- |
| Mohammed Amine Elkhaldy | Initialisation dépôt et modèle LaTeX (S1-1), descriptif et maquettes PNG, squelette exécutable `src/agent.py` + `tests/test_smoke.py` (S1-4), fiche semaine 1 (S1-6) | https://github.com/elkhaldymohamed16-alt/agent-recherche-documentaire/commit/5455a6b | 5 h |
| Aymen Elhaimer | Fiche équipe `docs/equipe.md` (S1-2), environnement reproductible `requirements.txt` + `.env.example` (S1-3), échantillon 5 docs + 20 questions, `src/stats_dataset.py` et `docs/architecture.png` (S1-5) | https://github.com/elkhaldymohamed16-alt/agent-recherche-documentaire/commit/baf4725 | 5 h |

État du dépôt à la remise de la fiche :

- [x] Dépôt créé, enseignant et tous les membres ajoutés
- [x] README avec le titre, les membres, le sujet et les commandes d'installation (S1-1)
- [x] Au moins un commit de chaque membre, depuis son propre compte (S1-2)
- [x] `requirements.txt` installable sur un clone neuf, `.env.example` présent, aucun secret poussé (S1-3)
- [x] Squelette exécutable et au moins un test qui passe (S1-4)
- [x] Jeu d'essai et schéma d'architecture dans le dépôt (S1-5)
- [x] Cette fiche poussée dans `docs/suivi/` et tag `s1` posé (S1-6)

## 9. Risques et points de blocage

| Risque ou blocage | Probabilité | Ce que vous ferez si cela arrive | Qui surveille |
| --- | --- | --- | --- |
| Indisponibilité d'une clé API LLM externe ou dépassement de quota | Moyenne | Basculer sur le mode local (Ollama `qwen2.5` ou synthèse extractive ancrée TF-IDF/embeddings) grâce à l'abstraction du moteur | Mohammed Amine Elkhaldy |
| Lourdeur de téléchargement de PyTorch/`sentence-transformers` sur clone neuf ou CI | Forte | Garder un mode de recherche léger déterministe pour la CI rapide et séparer les dépendances lourdes optionnelles | Aymen Elhaimer |
| Qualité variable de l'extraction de texte sur certains PDF multi-colonnes | Moyenne | Normaliser les sauts de ligne avec `pypdf` et limiter le corpus aux PDF texte natifs vérifiés | Aymen Elhaimer |

Question à poser à l'enseignant : aucune à ce stade ; le périmètre et l'échantillon sont prêts pour démarrer la semaine 2.

## 10. Engagements pour la semaine 2

| Engagement | Responsable | Comment on saura que c'est fait |
| --- | --- | --- |
| Implémenter le moteur RAG complet + script d'évaluation mesurant `Recall@3` sur les 20 questions (`S2-1`, `S2-2`) | Aymen Elhaimer | `docs/evaluation.md` généré et tests du cœur verts |
| Exposer l'agent via FastAPI (`/health`, `/ingest`, `/ask`) avec validation Pydantic et tests (`S2-3`) | Mohammed Amine Elkhaldy | `pytest tests/test_api.py` 100 % vert et Swagger `/docs` fonctionnel |
| Relier l'interface Streamlit à l'API et activer la CI GitHub Actions (`ruff` + `pytest`) puis poser le tag `s2` (`S2-4` à `S2-6`) | Mohammed Amine Elkhaldy & Aymen Elhaimer | Coche verte Actions sur `main`, capture dans `docs/` et tag `s2` poussé |
