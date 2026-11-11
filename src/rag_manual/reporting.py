"""Texto de saída (em português) para métricas e respostas."""

from __future__ import annotations

from collections.abc import Sequence

from rag_manual.domain.models import Answer, GoldenCase, RetrievalMetrics


def format_metrics(metrics: RetrievalMetrics) -> str:
    lines = [
        f"  [{metrics.strategy}] errou: {f.question}  "
        f"esperado {list(f.expected)}, veio {list(f.got)}"
        for f in metrics.failures
    ]
    lines.append(
        f"{metrics.strategy:9s} hit@{metrics.k} = {metrics.hits}/{metrics.total} "
        f"({metrics.hit_rate:.0%})   MRR@{metrics.depth} = {metrics.mrr:.2f}\n"
    )
    return "\n".join(lines)


def format_answers_markdown(
    title: str, cases: Sequence[GoldenCase], answers: Sequence[Answer]
) -> str:
    parts = [f"# {title}\n"]
    for number, (case, answer) in enumerate(zip(cases, answers, strict=True), start=1):
        expected = "|".join(str(p) for p in sorted(case.pages)) or "0"
        parts.append(
            f"## {number}. {case.question}\n\n"
            f"**Páginas esperadas:** {expected}  \n"
            f"**Páginas recuperadas:** {list(answer.pages)}\n\n"
            f"{answer.text}\n"
        )
    return "\n".join(parts)
