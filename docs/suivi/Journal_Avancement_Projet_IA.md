# Journal d’avancement — Projet d’application intelligente

> Journal tenu à jour avant chaque séance de suivi. Aucune clé API, mot de passe ou donnée personnelle réelle n'y figure.

## 1. Identification du projet

| Information | Valeur |
|---|---|
| Intitulé du projet | Agent de recherche documentaire (Projet N°1 du catalogue) |
| Groupe / classe | G3 — 4IAD (EMSI Casablanca) |
| Membres | Mohammed Amine Elkhaldy (`@elkhaldymohamed16-alt`), Aymen Elhaimer (`@aymen-elhaimer`) |
| Enseignant encadrant | A. Larhlimi |
| Dépôt du projet | https://github.com/elkhaldymohamed16-alt/agent-recherche-documentaire |
| Date de début / échéance | 09/11/2026 — 13/12/2026 |
| Utilisateur cible | Étudiants ingénieurs, développeurs et équipes techniques consultant une base documentaire interne (PDF et Markdown) |
| Problème à résoudre | Retrouver manuellement des règles d'architecture, procédures DevOps ou obligations légales (Loi 09-08 / RGPD) dans des documents hétérogènes prend plusieurs minutes et manque de traçabilité. L'agent fournit une réponse rapide et vérifiable avec citations exactes. |
| Fonction intelligente attendue | Recherche documentaire sémantique (RAG) avec réponse ancrée, résumé des sources, citations vérifiées et abstention contrôlée hors corpus |
| Résultat attendu | Ingestion PDF/MD (`POST /ingest`), Q&R RAG sourcée (`POST /ask`, `Recall@3 >= 90 %`, 0 citation inventée, 100 % abstention hors corpus), interface Streamlit et déploiement Docker Compose reproductible |

## 2. Entrée de suivi — 22/11/2026 (Semaine 1 / Bilan S1)

- **Période couverte :** du 16/11/2026 au 22/11/2026
- **Version ou commit présenté :** tag `s1` (commit `d34715f`) et tag `semaine1-remis`
- **État général :** Conforme au planning
- **Objectif prévu pour cette période :** Cadrer le projet (dossier de lancement + fiche de suivi S1), constituer un échantillon réel PDF/MD + jeu d'évaluation de 20 questions, livrer un squelette exécutable testé (`S1-1` à `S1-6`) et poser le tag `s1`.
- **Résultat effectivement obtenu :** Les 6 jalons `S1-1` à `S1-6` et les 4 livrables de lancement sont fusionnés sur `main` via branches et revues croisées ; `src/agent.py` répond avec citations sur les 5 documents de `data/sample/` ; `ruff check .` et `pytest -q` (`5 passed`) sont verts ; `src/stats_dataset.py` recalcule les statistiques du corpus.
- **Écart par rapport au planning :** Aucun retard. Le passage du moteur baseline TF-IDF vers ChromaDB/LLM ainsi que l'exposition FastAPI/Streamlit sont planifiés en semaine 2 (`S2-1` à `S2-6`).

### 2.1 Synthèse à présenter en deux minutes

1. **Nous avons terminé :** (1) le dossier complet de cadrage, maquettes PNG et schéma d'architecture (`docs/semaine1/`, `docs/architecture.png`, `docs/suivi/fiche-semaine-1.md`) ; (2) le corpus échantillon de 5 documents (3 Markdown + 2 PDF, 20 passages, 807 mots) et le jeu de 20 questions (`data/sample/`) ; (3) le squelette exécutable `src/agent.py` avec abstention et 5 tests `pytest` verts + `ruff` muet (tag `s1`).
2. **Nous pouvons démontrer :** L'exécution locale en ligne de commande de `python src/agent.py` sur une question du corpus (renvoie la réponse sourcée avec `03-conformite-loi-09-08-rgpd.md` et score `0.4225`), sur une question hors corpus (renvoie `abstention: true`), ainsi que `python src/stats_dataset.py` et `pytest -q`.
3. **Notre principal blocage est :** La taille et la lourdeur des dépendances d'embeddings locaux (PyTorch / `sentence-transformers`) sur un clone neuf et dans la CI GitHub Actions, nécessitant de découpler le mode léger déterministe du moteur vectoriel complet.
4. **Avant le prochain suivi, nous livrerons :** L'API FastAPI (`/health`, `/ingest`, `/ask`) avec tests (`S2-3`), le script d'évaluation complet sur les 20 questions (`docs/evaluation.md`, `S2-2`), l'interface Streamlit reliée à l'API (`S2-4`) et la CI GitHub Actions verte (tag `s2`).

## 3. Volet A — Développement de l’application intelligente

| Élément | Travail réalisé et résultat | Statut | Preuve : fichier, commit, test ou mesure | Responsable |
|---|---|---|---|---|
| Besoin et cas d’usage | Problème, utilisateurs cibles, 3 fonctionnalités MVP (F1–F3) et hors périmètre rédigés | Validé | `docs/semaine1/1-descriptif.md`, `docs/suivi/fiche-semaine-1.md` | Mohammed Amine Elkhaldy |
| Architecture | Schéma complet en 4 couches (Streamlit → FastAPI → Agent RAG → ChromaDB) + 3 maquettes PNG | Validé | `docs/architecture.png`, `docs/semaine1/3-maquette.md`, `docs/semaine1/img/` | Mohammed Amine Elkhaldy |
| Données | 5 documents (3 MD + 2 PDF natifs, 20 passages, 807 mots) + 20 questions JSON, licence libre | Validé | `data/sample/`, `docs/semaine1/2-dataset.md`, `src/stats_dataset.py` | Aymen Elhaimer |
| Préparation des données | Extraction UTF-8 / `pypdf`, découpage par section, normalisation espaces PDF, filtrage stop words FR | Validé | `src/agent.py::charger_passages`, `tests/test_smoke.py` | Aymen Elhaimer |
| Séparation des données | Non applicable à un entraînement supervisé (système RAG) ; corpus indexé et jeu d'évaluation indépendant de 20 questions | Validé | `data/sample/jeu_test_20_questions.json` (13 factuelles, 5 PDF, 1 synthèse, 1 hors-corpus) | Aymen Elhaimer |
| Modèle de référence | Baseline TF-IDF cosinus (`ngram_range=(1, 2)`, `STOP_WORDS_FR`, seuil `0.18`) : `Recall@3` = 19/19 (100.0 %), abstention hors corpus = 1/1 | Validé | `src/agent.py`, `tests/test_smoke.py` (`5 passed`) | Mohammed Amine Elkhaldy |
| Entraînement et comparaison | Comparaison EXP-01 (sans stop words) vs EXP-02 (avec `STOP_WORDS_FR`) ; comparaison avec embeddings ChromaDB prévue en S2 | En cours | Tableau section 3.1 ci-dessous | Mohammed Amine Elkhaldy |
| Évaluation et erreurs | Mesure initiale sur les 20 questions ; rapport détaillé `docs/evaluation.md` prévu en S2-2 | En cours | `data/sample/jeu_test_20_questions.json`, section 3.1 | Aymen Elhaimer |
| Sauvegarde du modèle | Index vectoriel persistant (`chroma_db/` hors Git) prévu en S2 ; baseline reconstruite à la volée en < 10 ms | En cours | `.gitignore` (`chroma_db/` exclu) | Aymen Elhaimer |
| API et validation | Schémas `/health`, `/ingest`, `/ask` spécifiés ; implémentation FastAPI + Pydantic prévue en S2-3 | Non commencé | `docs/semaine1/1-descriptif.md`, `docs/architecture.png` | Mohammed Amine Elkhaldy |
| Logique métier et interface | Maquettes des 3 onglets validées ; implémentation Streamlit + `httpx` prévue en S2-4 | Non commencé | `docs/semaine1/img/ecran1..3.png` | Mohammed Amine Elkhaldy |
| Tests et documentation | 5 tests unitaires `pytest` verts, `ruff check .` muet, `README.md`, `requirements.txt`, modèle LaTeX prêt | Validé | `tests/test_smoke.py`, `README.md`, `docs/rapport/` | Mohammed Amine Elkhaldy & Aymen Elhaimer |

### 3.1 Expériences et performance du modèle

| Expérience / date | Données et découpage | Modèle / paramètres | Métrique de validation | Temps d’exécution / matériel | Décision justifiée |
|---|---|---|---|---|---|
| EXP-01 (22/11/2026) | `data/sample/` (5 docs, 20 passages) évalués sur les 20 questions JSON | TF-IDF `ngram_range=(1, 2)`, `sublinear_tf=True`, **sans** stop words FR, seuil `0.18` | `Recall@1`: 18/19 (94.7 %) ; `Recall@3`: 18/19 (94.7 %) ; abstention hors corpus: **0/1** | 26.9 ms total (1.07 ms/req) — CPU Ubuntu 24.04 | **Rejetée** : les mots-outils (« quelle », « est », « la ») faussent la similarité cosinus et empêchent l'abstention hors corpus |
| EXP-02 (22/11/2026) | Même protocole fixe (`data/sample/`, 20 questions) | TF-IDF `ngram_range=(1, 2)`, `sublinear_tf=True`, **avec `STOP_WORDS_FR`**, seuil `0.18` | `Recall@1`: 18/19 (94.7 %) ; `Recall@3`: 19/19 (100.0 %) ; abstention hors corpus: **1/1** | 24.5 ms total (1.06 ms/req) — CPU Ubuntu 24.04 | **Retenue comme baseline S1** : détecte 100 % des questions hors corpus tout en gardant un excellent `Recall@3` |

- **Pourquoi cette métrique correspond-elle au besoin ?** `Recall@3` mesure directement la capacité du moteur à remonter le bon document dans le contexte fourni au LLM, et le taux d'abstention hors corpus garantit qu'aucune citation n'est inventée lorsque la réponse n'existe pas dans les documents.
- **Quel facteur a été modifié et quel effet a été observé ?** L'ajout d'une liste explicite de mots-outils français (`STOP_WORDS_FR`) dans `TfidfVectorizer` a éliminé les faux scores cosinus causés par les déterminants/pronoms interrogatifs et fait passer l'abstention hors corpus de `0/1` à `1/1`.
- **Comment avez-vous évité les fuites de données ?** Les 20 questions d'évaluation sont stockées séparément dans `jeu_test_20_questions.json` et ne sont jamais indexées dans le corpus (`charger_passages` ne lit que `.md` et `.pdf`).
- **Quels signes de surapprentissage ou de sous-apprentissage observez-vous ?** Un modèle purement lexical (TF-IDF) souffre de sous-apprentissage sémantique sur les synonymes ou reformulations ; l'ajout d'embeddings multilingues en semaine 2 adressera cette limite.
- **Comment reproduire l’expérience ?** `source .venv/bin/activate && python src/stats_dataset.py && pytest -q` (sur le tag `s1`, dépendances figées dans `requirements.txt`, Python 3.11.18).
- **Évaluation sur le test final :** Non réalisée (prévue en semaine 3 sur le système complet RAG + API + jeu d'évaluation gelé).
