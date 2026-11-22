"""Premiers tests du squelette exécutable (Semaine 1 — S1-4)."""
import json
from pathlib import Path

import pytest

from src.agent import charger_passages, rechercher

RACINE = Path(__file__).resolve().parents[1]
SAMPLE = RACINE / "data" / "sample"


def test_chargement_echantillon_md_et_pdf():
    passages = charger_passages(SAMPLE)
    sources = {p.source for p in passages}
    assert len(passages) >= 10
    assert "01-guide-mlops-architecture.md" in sources
    assert "04-guide-fastapi-tests.pdf" in sources
    assert "05-guide-docker-deploiement.pdf" in sources


def test_recherche_factuelle_cite_la_bonne_source():
    res = rechercher("Quelle autorité supervise la loi 09-08 au Maroc ?")
    assert res["abstention"] is False
    assert res["citations"][0]["source"] == "03-conformite-loi-09-08-rgpd.md"


def test_recherche_question_hors_corpus_s_abstient():
    res = rechercher("Quelle est la météo prévue demain à Casablanca ?")
    assert res["abstention"] is True
    assert res["citations"] == []


def test_question_vide_est_refusee():
    with pytest.raises(ValueError):
        rechercher("   ")


def test_jeu_test_contient_20_questions():
    data = json.loads((SAMPLE / "jeu_test_20_questions.json").read_text(encoding="utf-8"))
    assert len(data) == 20
