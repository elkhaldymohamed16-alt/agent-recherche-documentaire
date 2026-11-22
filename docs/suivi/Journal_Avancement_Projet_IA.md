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

## 4. Volet B — Déploiement et exploitation

| Élément | Configuration ou action réalisée | Statut | Preuve vérifiable | Responsable |
|---|---|---|---|---|
| Cible de déploiement | Poste local Linux (Ubuntu 24.04) en S1 ; cible finale conteneurisée Docker Compose (`api` + `ui`) en S3 | En cours | `README.md`, `docs/semaine1/4-pipeline.md` | Aymen Elhaimer |
| Environnement | Python 3.11.18, `.venv` isolé, `requirements.txt` aux versions figées | Validé | `requirements.txt`, `.gitignore` | Aymen Elhaimer |
| Construction | Dockerfiles (`api` et `ui`) et `docker-compose.yml` planifiés en S3 (`T9`) | Non commencé | `docs/semaine1/4-pipeline.md` | Aymen Elhaimer |
| Configuration et secrets | Modèle `.env.example` versionné (aucun secret dans Git ; `.env` ignoré) | Validé | `.env.example`, `.gitignore` | Aymen Elhaimer |
| Démarrage du service | Exécution CLI fonctionnelle (`python src/agent.py "..."`) ; serveur Uvicorn (`:8000`) et Streamlit (`:8501`) en S2 | En cours | `src/agent.py`, `README.md` | Mohammed Amine Elkhaldy |
| Réseau et accès | Non encore exposé en HTTP ; prévu en S2-3 (`127.0.0.1:8000` et CORS contrôlé) | Non commencé | `docs/architecture.png` | Mohammed Amine Elkhaldy |
| Test de bout en bout | Parcours CLI (`question → recherche → réponse sourcée / abstention`) vérifié ; parcours UI → API en S2-4 | En cours | `tests/test_smoke.py` (`5 passed`) | Mohammed Amine Elkhaldy |
| Performance en service | Latence moyenne locale mesurée en CLI : 1.06 ms/requête sur les 20 cas (CPU, concurrence 1) | À vérifier | Mesure EXP-02 section 3.1 | Aymen Elhaimer |
| Surveillance | Journalisation structurée des requêtes/abstentions prévue dans l'API FastAPI en S2-3 | Non commencé | `docs/semaine1/1-descriptif.md` | Mohammed Amine Elkhaldy |
| Mise à jour et retour arrière | Versionnement par tags Git (`semaine1-remis`, `s1`, puis `s2`, `v1.0.0`) permettant un retour immédiat | Validé | `git tag -l` sur GitHub | Mohammed Amine Elkhaldy |

### 4.1 Démonstration de la version disponible

- **Lieu d’exécution :** Local (Ubuntu 24.04, Python 3.11.18 dans `.venv` — pas encore déployé sur serveur/conteneur)
- **Adresse ou procédure d’accès :** `git clone https://github.com/elkhaldymohamed16-alt/agent-recherche-documentaire.git && python3.11 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
- **Scénario de démonstration :**
  1. Lancer `python src/stats_dataset.py` pour afficher les statistiques du corpus.
  2. Lancer `python src/agent.py "Quelle autorité supervise l'application de la loi 09-08 au Maroc ?"`.
  3. Lancer `python src/agent.py "Quelle est la météo prévue demain à Casablanca ?"`.
  4. Lancer `pytest -q` et `ruff check .`.
- **Résultat attendu :** Réponse sourcée pointant sur `03-conformite-loi-09-08-rgpd.md` (CNDP) à l'étape 2 ; `abstention: true` et `citations: []` à l'étape 3 ; `5 passed` et `All checks passed!` à l'étape 4.
- **Résultat observé :** Conforme à l'attendu (`score_max: 0.4225` sur la question Loi 09-08 ; `abstention: true` sur la question météo ; `5 passed` en 1,68 s ; `ruff` muet).
- **Limites connues :** Pas encore d'API HTTP ni d'interface Streamlit actives ; recherche encore lexicale (TF-IDF) sans synthèse par LLM.
- **Preuve datée :** Tag Git `s1` (`22/11/2026`) et suite `tests/test_smoke.py`.

## 5. Sécurité et protection des données

| Point de contrôle | Développement : mesure intégrée au code | Déploiement : configuration ou contrôle | Statut / preuve |
|---|---|---|---|
| Validation des entrées | Refus des questions vides ou composées d'espaces (`ValueError` dans `src/agent.py`) ; validation Pydantic prévue en S2-3 | Limitation de taille (`max_length`) et types MIME PDF/MD lors de `/ingest` en S2 | En cours (`tests/test_smoke.py::test_question_vide_est_refusee`) |
| Authentification et droits | Hors périmètre SSO/RBAC ; protection optionnelle par clé `X-API-Key` prévue sur `/ingest` en S2 | Clé injectée par variable d'environnement uniquement | Non commencé (prévu S2) |
| Secrets | Aucun secret dans le code ; `.env.example` ne contient que des valeurs fictives (`changez-moi`) | `.env` listé dans `.gitignore` ; vérifié avant chaque commit | Validé (`.gitignore`, `.env.example`) |
| Données personnelles | Corpus 100 % public/synthétique ; aucune donnée personnelle (CIN, noms clients, emails) | Aucun stockage de requêtes personnelles côté serveur | Validé (`data/sample/`, `03-conformite-loi-09-08-rgpd.md`) |
| Modèles et dépendances | Versions figées dans `requirements.txt` (`scikit-learn==1.5.*`, `fastapi==0.115.*`, `pypdf==5.1.*`) | Installation reproductible vérifiée dans `.venv` neuf | Validé (`requirements.txt`) |
| Journaux | Aucune clé ni donnée sensible journalisée | Règle appliquée dès la mise en place de l'API FastAPI en S2 | En cours |

- **Risque principal restant :** Risque d'injection de prompt (prompt injection) si un document externe contient des instructions malveillantes lors du branchement du LLM en semaine 2.
- **Action corrective, responsable et échéance :** Isoler strictement les extraits récupérés entre balises de contexte dans le prompt système et vérifier les citations retournées (`verify_citations`) — Responsable : Mohammed Amine Elkhaldy, échéance : S2 (`29/11/2026`).

## 6. Contributions individuelles

| Étudiant | Contribution de développement | Contribution de déploiement | Preuve personnelle | Ce qu’il/elle expliquera à l’oral |
|---|---|---|---|---|
| Mohammed Amine Elkhaldy | Descriptif (`1-descriptif.md`), maquettes PNG (`3-maquette.md`), squelette exécutable `src/agent.py` + `tests/test_smoke.py` (`S1-4`), fiche suivi S1 (`S1-6`) | Initialisation dépôt, `.gitignore`, `README.md` (`S1-1`), gestion des tags Git (`semaine1-remis`, `s1`) | Commit `0dbbeea` (https://github.com/elkhaldymohamed16-alt/agent-recherche-documentaire/commit/0dbbeea), `src/agent.py`, `docs/semaine1/img/` | L'architecture RAG en couches, le fonctionnement de la recherche + seuil d'abstention et les choix de découplage |
| Aymen Elhaimer | Constitution du corpus échantillon 3 MD + 2 PDF et des 20 questions (`2-dataset.md`), pipeline des tâches (`4-pipeline.md`), script `src/stats_dataset.py` et `docs/architecture.png` (`S1-5`) | Configuration reproductible `requirements.txt`, `.env.example`, `pytest.ini` (`S1-3`) et revue croisée des PRs | Commit `d34715f` (https://github.com/elkhaldymohamed16-alt/agent-recherche-documentaire/commit/d34715f), `data/sample/`, `src/stats_dataset.py` | La conception du corpus/jeu de test (20 cas), les statistiques de qualité des données et la reproductibilité de l'environnement |

## 7. Blocages, décisions et demandes d’aide

| Blocage / question | Impact | Tentatives déjà réalisées et résultats | Aide ou décision attendue | Responsable / échéance |
|---|---|---|---|---|
| Faux positif sur question hors corpus (`EXP-01`) | La question météo dépassait le seuil `0.18` à cause des mots-outils français | Ajout de `STOP_WORDS_FR` dans `TfidfVectorizer` (`EXP-02`) : résolu (`abstention: 1/1`, `5 passed`) | Aucune aide requise (résolu) | Mohammed Amine Elkhaldy (résolu le 22/11/2026) |
| Poids élevé de PyTorch / `sentence-transformers` en CI | Risque de timeouts ou lenteur sur clone neuf en CI GitHub Actions | Séparation envisagée entre baseline légère pour la CI rapide et backend embeddings/ChromaDB optionnel | Validation de cette stratégie lors du point S2 | Aymen Elhaimer (26/11/2026) |

| Décision prise | Alternatives examinées | Justification | Conséquence sur le projet |
|---|---|---|---|
| Démarrer S1 avec une baseline TF-IDF déterministe avant ChromaDB + LLM en S2 | Installer directement LangChain + PyTorch + Ollama dès S1 | Garantit un squelette rapide, testable sans GPU ni clé API dès la semaine 1 et fournit une référence chiffrée pour mesurer le gain du RAG sémantique | Permet une comparaison rigoureuse EXP-02 (TF-IDF) vs EXP-03 (ChromaDB/embeddings) en semaine 2 |
| Utiliser un seuil d'abstention explicite (`SEUIL_ABSTENTION`) | Laisser le modèle toujours renvoyer le passage le plus proche | Empêche l'agent d'inventer des réponses ou citations sur des questions hors périmètre | Oblige à calibrer le seuil à chaque changement de représentation vectorielle |

## 8. Plan jusqu’au prochain suivi (Semaine 2 — tag `s2`)

| Priorité | Tâche | Volet : développement / déploiement | Responsable | Échéance | Critère de réussite et preuve prévue |
|---|---|---|---|---|---|
| 1 | Implémenter le moteur RAG enrichi (`S2-1`) et le script d'évaluation complet sur les 20 questions (`S2-2`) | Développement | Aymen Elhaimer | 25/11/2026 | `docs/evaluation.md` généré avec `Recall@3 >= 90 %` et 100 % d'abstention hors corpus |
| 2 | Développer l'API FastAPI (`/health`, `/ingest`, `/ask`) avec schémas Pydantic v2 et tests (`S2-3`) | Développement | Mohammed Amine Elkhaldy | 27/11/2026 | `pytest tests/test_api.py` 100 % vert (200/422/503/500) et page `/docs` fonctionnelle |
| 3 | Relier l'interface Streamlit à l'API (`S2-4`), activer la CI GitHub Actions `ruff` + `pytest` (`S2-5`) et livrer la fiche S2 + tag `s2` (`S2-6`) | Déploiement | Mohammed Amine Elkhaldy & Aymen Elhaimer | 29/11/2026 | Coche verte Actions sur `main`, capture d'écran dans `docs/` et tag `s2` poussé |

## 9. Retour de l’enseignant et prise en compte

- **Observations de l’enseignant :** *[À compléter après la séance de suivi S1]*
- **Corrections demandées :** *[À compléter après la séance de suivi S1]*
- **Actions retenues par le groupe :** *[À compléter après la séance de suivi S1]*
- **Vérification au suivi suivant :** *[À compléter en semaine 2]*

## 10. Vérification avant remise

- [x] La date, les membres et la version présentée sont renseignés.
- [x] Le développement et le déploiement sont distingués.
- [x] Chaque résultat annoncé possède une preuve accessible à l’enseignant.
- [x] Les mesures indiquent leur protocole et leurs conditions.
- [x] Les blocages décrivent les tentatives déjà effectuées.
- [x] Chaque membre a une contribution identifiable.
- [x] Les prochaines tâches ont un responsable, une échéance et un critère de réussite.
- [x] Les secrets et les données personnelles ont été retirés des preuves.
