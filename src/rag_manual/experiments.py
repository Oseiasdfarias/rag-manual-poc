"""Experimentos: cada um muda uma coisa em relação à base e grava um arquivo em results/."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any

from rag_manual.application.evaluation import EvaluateRetrieval
from rag_manual.composition import build_ingest, build_retrievers
from rag_manual.config import BASE_EMBEDDING_MODEL, E5_EMBEDDING_MODEL, RERANKER_MODEL, Settings
from rag_manual.infrastructure.golden_csv import load_golden_cases
from rag_manual.reporting import format_metrics


@dataclass(frozen=True)
class Experiment:
    name: str
    description: str
    overrides: dict[str, Any] = field(default_factory=dict)


# A base é sempre a configuração original: trechos fixos 800/150, MiniLM, sem reranker.
E5 = E5_EMBEDDING_MODEL
BASE = {
    "chunker": "fixed",
    "chunk_size": 800,
    "chunk_overlap": 150,
    "embedding_model": BASE_EMBEDDING_MODEL,
}

EXPERIMENTS: tuple[Experiment, ...] = (
    Experiment("base", "trechos fixos 800/150, MiniLM", dict(BASE)),
    Experiment("chunk400", "trechos de 400", {**BASE, "chunk_size": 400}),
    Experiment("chunk1500", "trechos de 1500", {**BASE, "chunk_size": 1500}),
    Experiment("overlap0", "sem sobreposição", {**BASE, "chunk_overlap": 0}),
    Experiment("e5", "base com multilingual-e5-small", {**BASE, "embedding_model": E5}),
    Experiment("secao", "trechos por seção", {**BASE, "chunker": "section"}),
    Experiment(
        "secao_e5",
        "trechos por seção + multilingual-e5-small",
        {**BASE, "chunker": "section", "embedding_model": E5},
    ),
)


def find_experiments(names: Sequence[str]) -> list[Experiment]:
    by_name = {e.name: e for e in EXPERIMENTS}
    unknown = [n for n in names if n not in by_name]
    if unknown:
        raise ValueError(f"Experimento desconhecido: {unknown}. Disponíveis: {sorted(by_name)}")
    return [by_name[n] for n in names] if names else list(EXPERIMENTS)


def run_experiment(
    experiment: Experiment,
    settings: Settings,
    results_dir: Path,
    use_reranker: bool,
    skip_ingest: bool = False,
) -> str:
    """Ingere (a menos que `skip_ingest`), avalia e grava `results/eval_<nome>.txt`."""
    config = replace(
        settings,
        **experiment.overrides,
        index_dir=settings.index_dir / "experimentos" / experiment.name,
        reranker_model=RERANKER_MODEL if use_reranker else "",
    )
    header = [f"# experimento: {experiment.name} ({experiment.description})"]
    if not skip_ingest:
        report = build_ingest(config).run(config.pdf_path)
        header.append(f"# {report.pages} páginas, {report.chunks} trechos")
    cases = load_golden_cases(config.golden_path)
    metrics = EvaluateRetrieval().run_all(build_retrievers(config), cases)
    text = "\n".join(header) + "\n" + "\n".join(format_metrics(m) for m in metrics)
    results_dir.mkdir(parents=True, exist_ok=True)
    (results_dir / f"eval_{experiment.name}.txt").write_text(text, encoding="utf-8")
    return text
