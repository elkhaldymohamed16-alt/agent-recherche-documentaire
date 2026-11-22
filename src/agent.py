#!/usr/bin/env python
"""Squelette exécutable de l'agent de recherche documentaire (Semaine 1 — S1-4).

Charge les documents Markdown et PDF de `data/sample/`, découpe en sections/passages,
indexe par TF-IDF cosinus (baseline déterministe avant l'intégration ChromaDB/LLM
de la semaine 2) et répond avec citations exactes ou abstention hors corpus.

Usage :
  python src/agent.py "Quels sont les trois artefacts à versionner dans une application IA ?"
"""
from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

RACINE = Path(__file__).resolve().parents[1]
DOSSIER_SAMPLE = RACINE / "data" / "sample"
SEUIL_ABSTENTION = float(os.environ.get("SEUIL_ABSTENTION", "0.18"))

STOP_WORDS_FR = [
    "a", "au", "aux", "avec", "ce", "ces", "dans", "de", "des", "du", "elle",
    "en", "est", "et", "etre", "il", "ils", "je", "la", "le", "les", "leur",
    "lui", "ma", "mais", "me", "meme", "mes", "moi", "mon", "ne", "nos",
    "notre", "nous", "on", "ou", "par", "pas", "pour", "qu", "que", "quel",
    "quelle", "quelles", "quels", "qui", "sa", "sans", "se", "ses", "son",
    "sont", "sur", "ta", "te", "tes", "toi", "ton", "tu", "un", "une", "vos",
    "votre", "vous", "y", "à", "être", "d", "l", "n", "s", "c", "j",
]


@dataclass
class Passage:
    """Un extrait documentaire avec ses métadonnées de provenance."""

    source: str
    section: str
    texte: str


def charger_passages(dossier: Path = DOSSIER_SAMPLE) -> list[Passage]:
    """Lit les fichiers .md et .pdf d'un dossier et les découpe par section."""
    passages: list[Passage] = []
    for fichier in sorted(dossier.iterdir()):
        if fichier.suffix.lower() == ".md":
            contenu = fichier.read_text(encoding="utf-8")
            blocs = re.split(r"(?=^## )", contenu, flags=re.M)
            for bloc in blocs:
                bloc_propre = bloc.strip()
                if not bloc_propre:
                    continue
                lignes = bloc_propre.splitlines()
                titre = lignes[0].lstrip("# ").strip()
                corps = " ".join(line.strip() for line in lignes[1:] if line.strip()) or titre
                passages.append(Passage(source=fichier.name, section=titre, texte=corps))
        elif fichier.suffix.lower() == ".pdf":
            lecteur = PdfReader(str(fichier))
            texte_pdf = "\n".join((page.extract_text() or "") for page in lecteur.pages)
            blocs = re.split(r"(?=Section \d+\s*:)", texte_pdf)
            for idx, bloc in enumerate(blocs, start=1):
                bloc_propre = " ".join(bloc.split())
                if len(bloc_propre) < 20:
                    continue
                m = re.match(r"(Section \d+\s*:[^.]+)", bloc_propre)
                titre = m.group(1).strip() if m else f"Page {idx}"
                passages.append(Passage(source=fichier.name, section=titre, texte=bloc_propre))
    return passages


def rechercher(question: str, dossier: Path = DOSSIER_SAMPLE, top_k: int = 3) -> dict:
    """Recherche les passages pertinents et retourne une réponse sourcée ou une abstention."""
    if not isinstance(question, str) or not question.strip():
        raise ValueError("La question ne doit pas être vide.")
    passages = charger_passages(dossier)
    if not passages:
        raise FileNotFoundError(f"Aucun document exploitable dans {dossier}")

    corpus = [f"{p.section} {p.texte}" for p in passages]
    vect = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, stop_words=STOP_WORDS_FR)
    matrice = vect.fit_transform(corpus)
    q_vec = vect.transform([question])
    scores = cosine_similarity(q_vec, matrice).ravel()

    ordre = scores.argsort()[::-1][:top_k]
    meilleur_score = float(scores[ordre[0]])
    sources = [
        {
            **asdict(passages[i]),
            "score": round(float(scores[i]), 4),
        }
        for i in ordre
        if scores[i] > 0
    ]

    if meilleur_score < SEUIL_ABSTENTION or not sources:
        return {
            "question": question,
            "abstention": True,
            "reponse": "Information absente du corpus fourni (similarité insuffisante).",
            "score_max": round(meilleur_score, 4),
            "citations": [],
        }

    top = sources[0]
    return {
        "question": question,
        "abstention": False,
        "reponse": f"D'après {top['source']} ({top['section']}) : {top['texte']}",
        "score_max": round(meilleur_score, 4),
        "citations": sources,
    }


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if not args:
        print('Usage : python src/agent.py "Votre question"')
        return 2
    resultat = rechercher(" ".join(args))
    print(json.dumps(resultat, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
