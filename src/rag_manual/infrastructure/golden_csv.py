"""Leitura do conjunto de teste (golden.csv, separado por ponto e vírgula)."""

from __future__ import annotations

import csv
from pathlib import Path

from rag_manual.domain.models import GoldenCase


def load_golden_cases(path: Path) -> list[GoldenCase]:
    """Colunas: `pergunta` e `paginas` (separadas por `|`; `0` = o manual não responde)."""
    with open(path, encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file, delimiter=";"))
    cases = []
    for row in rows:
        pages = frozenset(int(p) for p in row["paginas"].split("|"))
        cases.append(GoldenCase(question=row["pergunta"], pages=pages - {0}))
    return cases
