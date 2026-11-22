#!/usr/bin/env python
"""Recalcule automatiquement les statistiques du corpus et du jeu d'évaluation (S1-5)."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.agent import DOSSIER_SAMPLE, charger_passages  # noqa: E402


def calculer_stats(dossier: Path = DOSSIER_SAMPLE) -> dict:
    passages = charger_passages(dossier)
    docs_mots: dict[str, int] = {}
    for p in passages:
        docs_mots[p.source] = docs_mots.get(p.source, 0) + len(p.texte.split())

    questions_path = dossier / "jeu_test_20_questions.json"
    questions = json.loads(questions_path.read_text(encoding="utf-8"))
    types_q = dict(sorted(Counter(q["type"] for q in questions).items()))

    total_mots = sum(docs_mots.values())
    nb_docs = len(docs_mots)
    longueur_moyenne = round(total_mots / nb_docs, 1) if nb_docs else 0.0
    doublons = len(passages) - len({p.texte for p in passages})

    return {
        "nb_documents": nb_docs,
        "nb_md": sum(1 for k in docs_mots if k.endswith(".md")),
        "nb_pdf": sum(1 for k in docs_mots if k.endswith(".pdf")),
        "nb_passages": len(passages),
        "total_mots": total_mots,
        "longueur_moyenne_mots": longueur_moyenne,
        "doublons_passages": doublons,
        "valeurs_manquantes": 0,
        "nb_questions_test": len(questions),
        "repartition_questions": types_q,
        "mots_par_document": docs_mots,
    }


def main() -> int:
    stats = calculer_stats()
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
