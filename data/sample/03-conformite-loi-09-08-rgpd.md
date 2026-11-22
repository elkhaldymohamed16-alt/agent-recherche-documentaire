# Conformité, éthique et protection des données personnelles

## Section 1 : Cadre légal au Maroc (Loi 09-08) et en Europe (RGPD)
Au Maroc, la loi n° 09-08 relative à la protection des personnes physiques à l'égard du traitement des données à caractère personnel, supervisée par la CNDP, impose le consentement préalable, la finalité déterminée et la proportionnalité des données collectées. En Europe, le RGPD applique des principes équivalents de minimisation, de transparence et de droit à l'effacement.

## Section 2 : Règles applicables aux systèmes IA et RAG
Aucune donnée personnelle réelle (noms de clients, numéros de téléphone, CIN, adresses postales ou dossiers médicaux) ne doit être indexée dans une base vectorielle de développement ou envoyée à un LLM tiers sans anonymisation préalable. En contexte académique, seuls des documents publics, sous licence libre ou synthétiques sont autorisés.

## Section 3 : Supervision humaine et sécurité des prompts
Les agents documentaires doivent se prémunir contre les attaques par injection de prompt (prompt injection) contenues dans des documents non fiables en isolant strictement les instructions système des passages récupérés. Toute décision à fort impact juridique, médical ou financier requiert une validation humaine finale.
