# Guide d'architecture MLOps et cycle de vie d'une application IA

## Section 1 : Les trois artefacts à versionner
Contrairement au développement logiciel classique qui ne versionne que le code source, une application intelligente doit assurer la traçabilité de trois artefacts : le code source (Git), les jeux de données (DVC ou manifestes datés) et les modèles entraînés (MLflow ou registre dédié). Les fichiers binaires volumineux comme `.joblib` ou `.venv/` ne doivent jamais entrer dans Git ; seules les métriques légères (`metrics.json`) y sont versionnées.

## Section 2 : Architecture en couches découplées
Une architecture maintenable sépare strictement quatre couches :
1. Couche données (`data/`) : jeux bruts, échantillons et jeu d'or d'évaluation.
2. Couche modèle (`src/` ou paquet installable) : ingestion, entraînement, prédiction et explicabilité.
3. Couche service (`api/`) : API REST FastAPI exposant `/health` et `/predict` ou `/ask`, validation Pydantic et gestion des codes HTTP (200, 422, 500, 503).
4. Couche présentation (`ui/`) : interface Streamlit communiquant uniquement par HTTP avec l'API, sans jamais importer directement le modèle.

## Section 3 : Prévention de la dérive et réentraînement
En production, la distribution des données d'entrée évolue dans le temps : c'est la dérive des données (data drift). Une surveillance continue de la latence, du taux d'abstention et des métriques métier déclenche un réentraînement contrôlé (Continuous Training) suivi d'une porte de validation automatisée en CI.
