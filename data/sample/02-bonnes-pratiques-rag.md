# Bonnes pratiques pour les systèmes RAG (Retrieval-Augmented Generation)

## Section 1 : Découpage des documents (Chunking)
La qualité d'un système RAG dépend d'abord du découpage en passages. Des passages de 400 à 600 caractères avec un chevauchement (overlap) de 80 à 100 caractères préservent le contexte autour des transitions de paragraphes tout en gardant des vecteurs précis pour la recherche sémantique. Chaque chunk conserve obligatoirement ses métadonnées : `source`, `section` et `page`.

## Section 2 : Embeddings et recherche vectorielle
Pour un corpus majoritairement francophone, un modèle d'embeddings multilingue léger comme `paraphrase-multilingual-MiniLM-L12-v2` (384 dimensions) offre un excellent compromis vitesse/qualité sur CPU. La recherche par similarité cosinus renvoie les `k=4` passages les plus proches (top-k retrieval).

## Section 3 : Ancrage factuel, citations et abstention
Pour limiter les hallucinations du LLM, le prompt système impose trois règles strictes :
- répondre exclusivement à partir des extraits fournis dans le contexte ;
- citer systématiquement le nom du fichier et la section pour chaque affirmation ;
- répondre « Information absente du corpus fourni » lorsque le score de similarité maximal reste sous le seuil d'abstention (fixé à 0,35 par défaut).
