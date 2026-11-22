# Livrable 2 : dataset

**Rédacteur :** Aymen Elhaimer (`@aymen-elhaimer`) &emsp; **Relecteur :** Mohammed Amine Elkhaldy (`@elkhaldymohamed16-alt`) &emsp; **Fichiers :** `docs/semaine1/2-dataset.md` + `data/sample/`

## 2.1 Description

| Rubrique | Réponse |
| --- | --- |
| Nom et source (lien) | Corpus documentaire technique et réglementaire (guides d'ingénierie IA/MLOps, FastAPI, Docker, RAG et conformité Loi 09-08/RGPD) complété par la documentation publique officielle FastAPI (`https://fastapi.tiangolo.com/`) et scikit-learn (`https://scikit-learn.org/stable/`) |
| Producteur ou propriétaire | Documents pédagogiques rédigés par l'équipe et documentations techniques open-source publiques |
| Volume (nombre de fichiers, lignes, pages, taille) | Échantillon livré : 5 documents (3 Markdown + 2 PDF natifs, ~120 lignes, < 20 Ko) + 1 fichier de 20 questions de test (`jeu_test_20_questions.json`). Corpus cible en semaine 2 : 25 à 40 documents (~300 pages, < 15 Mo) |
| Format et structure | Fichiers `.md` structurés par titres `## Section`, fichiers `.pdf` texte natif (non scannés), et jeu d'évaluation au format `.json` (`id`, `question`, `source_attendue`, `section`, `type`) |
| Langue et période couverte | Français (principal) et extraits techniques en anglais ; documents à jour (2025–2026) |
| Licence et droits d'usage | Licence libre CC BY 4.0 (contenus rédigés par l'équipe) et licences MIT / BSD-3-Clause (documentations FastAPI et scikit-learn), autorisant librement l'usage dans un projet académique |
| Données personnelles ou sensibles, et traitement prévu | Aucune donnée personnelle ni confidentielle : uniquement des contenus techniques publics et synthétiques |
| Emplacement des données complètes | Échantillon versionné dans `data/sample/` ; corpus complet téléchargé automatiquement dans `data/raw/` (ignoré par Git) via un script d'ingestion reproductible en semaine 2 |

## 2.2 Qualité constatée sur l'échantillon

Les cinq fichiers de `data/sample/` s'ouvrent sans erreur (encodage UTF-8 pour les Markdown, format PDF 1.4 texte natif extractible sans OCR pour les deux PDF). Aucun doublon ni caractère corrompu n'a été constaté. Les PDF génèrent de légers retours à la ligne fixes en fin de ligne qu'il faudra normaliser lors de l'étape de prétraitement avant le chunking.

## 2.3 Justification

| Fonctionnalité | Données utilisées | En quoi elles suffisent |
| --- | --- | --- |
| F1 — Ingestion et indexation | Fichiers `.md` et `.pdf` de `data/sample/` puis corpus complet `data/raw/` | Couvrent les deux formats cibles (PDF et Markdown) avec titres et pages permettant de tester l'extraction, le découpage et les métadonnées |
| F2 — Réponse RAG sourcée et résumé | Passages indexés avec métadonnées (`source`, `section`, `page`) + `jeu_test_20_questions.json` | Contiennent des faits précis et vérifiables (chiffres, seuils, règles légales) pour contrôler l'exactitude des réponses, des résumés et des citations ainsi que l'abstention hors corpus |
| F3 — Interface Streamlit | Documents téléversables depuis `data/sample/` et requêtes de démonstration | Permettent de démontrer en direct l'ajout d'un document PDF/MD, la recherche en langage naturel et l'affichage des extraits sources |

## 2.4 Alternative de repli

Si l'extension du corpus depuis les documentations web rencontrait une coupure réseau ou un changement de structure HTML, la source de repli vérifiée est le jeu public **arXiv / Wikipedia FR (CC BY-SA 4.0)** via l'API publique Wikimedia (`https://fr.wikipedia.org/api/rest_v1/page/summary/Apprentissage_automatique`) ou les articles PDF ouverts d'arXiv (`https://arxiv.org/list/cs.CL/recent`). Ce repli reste accessible sans authentification ; l'inconvénient serait un corpus plus académique (en anglais pour arXiv) et moins homogène vis-à-vis des besoins d'ingénierie logicielle en français.

## 2.5 Jeu de test

Le jeu de test initial est déjà rédigé dans `data/sample/jeu_test_20_questions.json` par le binôme et comporte **20 cas** répartis ainsi :
- **13 questions factuelles** sur les fichiers Markdown (MLOps, RAG, Loi 09-08/RGPD) ;
- **5 questions spécifiques aux fichiers PDF** (FastAPI, Docker) ;
- **1 question de synthèse multi-documents** croisant architecture et Docker Compose ;
- **1 question hors corpus** (*« Quelle est la météo prévue demain à Casablanca ? »*) vérifiant que l'agent s'abstient au lieu d'halluciner.

Les métriques suivies seront le **taux de rappel du bon document dans le top-3 (`Recall@3 >= 0,90`)**, l'**exactitude des citations** (0 citation inventée) et la **détection des questions hors corpus**.

## Critères d'acceptation (vérifiés par le relecteur : Mohammed Amine Elkhaldy)

- [x] L'échantillon est dans `data/sample/` et s'ouvre sans erreur.
- [x] La licence autorise l'usage dans un projet de cours.
- [x] Les données personnelles éventuelles sont anonymisées ou remplacées par des données fictives (aucune donnée personnelle).
- [x] Chaque fonctionnalité du MVP est couverte par la justification.
- [x] L'alternative de repli est réellement accessible (liens vérifiés).
- [x] Le jeu de test est défini et déjà rédigé (20 questions dans `data/sample/jeu_test_20_questions.json`).
