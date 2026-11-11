"""Linha de comando: ingest, ask, eval, experiment, answers."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from dataclasses import replace
from pathlib import Path

from rag_manual.application.evaluation import EvaluateRetrieval
from rag_manual.application.ingest import NoTextExtractedError
from rag_manual.composition import (
    CHUNKERS,
    build_answerer,
    build_ingest,
    build_retrievers,
)
from rag_manual.config import RERANKER_MODEL, Settings
from rag_manual.experiments import EXPERIMENTS, find_experiments, run_experiment
from rag_manual.infrastructure.golden_csv import load_golden_cases
from rag_manual.reporting import format_answers_markdown, format_metrics


def _add_config_options(parser: argparse.ArgumentParser) -> None:
    group = parser.add_argument_group("configuração (sobrepõe as variáveis de ambiente)")
    group.add_argument("--index-dir", type=Path, help="pasta dos índices (padrão: db)")
    group.add_argument("--chunker", choices=sorted(CHUNKERS), help="como dividir o texto")
    group.add_argument("--chunk-size", type=int, help="tamanho do trecho, em caracteres")
    group.add_argument("--overlap", type=int, help="sobreposição entre trechos, em caracteres")
    group.add_argument("--embedding-model", help="modelo de embedding")
    group.add_argument(
        "--reranker",
        nargs="?",
        const=RERANKER_MODEL,
        metavar="MODELO",
        help="liga o reranker (sem valor: usa %(const)s). Use 'none' para desligar",
    )


def _settings_from(args: argparse.Namespace) -> Settings:
    settings = Settings.from_env()
    overrides = {
        "index_dir": args.index_dir,
        "chunker": args.chunker,
        "chunk_size": args.chunk_size,
        "chunk_overlap": args.overlap,
        "embedding_model": args.embedding_model,
    }
    if args.reranker is not None:
        overrides["reranker_model"] = "" if args.reranker == "none" else args.reranker
    return replace(settings, **{k: v for k, v in overrides.items() if v is not None})


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rag-manual", description="RAG sobre o manual de motores elétricos da WEG."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    ingest = sub.add_parser("ingest", help="lê o PDF, divide em trechos e grava os índices")
    ingest.add_argument("pdf", nargs="?", type=Path, help="padrão: data/manual.pdf")
    _add_config_options(ingest)

    ask = sub.add_parser("ask", help="responde uma pergunta citando a página")
    ask.add_argument("question", nargs="+", help="a pergunta")
    _add_config_options(ask)

    evaluate = sub.add_parser("eval", help="mede hit@3 e MRR de cada busca")
    evaluate.add_argument("--out", type=Path, help="grava a saída também neste arquivo")
    _add_config_options(evaluate)

    experiment = sub.add_parser("experiment", help="roda experimentos e grava em results/")
    experiment.add_argument("names", nargs="*", help="nomes (padrão: todos)")
    experiment.add_argument("--list", action="store_true", help="só lista os experimentos")
    experiment.add_argument("--rerank", action="store_true", help="inclui a busca com reranker")
    experiment.add_argument("--skip-ingest", action="store_true", help="reaproveita os índices")
    experiment.add_argument("--results-dir", type=Path, default=Path("results"))

    answers = sub.add_parser("answers", help="responde as perguntas do conjunto de teste")
    answers.add_argument("--out", type=Path, required=True, help="arquivo .md de saída")
    answers.add_argument("--title", help="título do arquivo")
    _add_config_options(answers)
    return parser


def _cmd_ingest(args: argparse.Namespace) -> int:
    settings = _settings_from(args)
    pdf = args.pdf or settings.pdf_path
    try:
        report = build_ingest(settings).run(pdf)
    except NoTextExtractedError as error:
        print(error, file=sys.stderr)
        return 1
    print(f"{report.pages} páginas, {report.chunks} trechos")
    print("Ingestão concluída.")
    return 0


def _cmd_ask(args: argparse.Namespace) -> int:
    answer = build_answerer(_settings_from(args)).run(" ".join(args.question))
    print(answer.text)
    print("\nPáginas usadas:", list(answer.pages))
    return 0


def _cmd_eval(args: argparse.Namespace) -> int:
    settings = _settings_from(args)
    cases = load_golden_cases(settings.golden_path)
    metrics = EvaluateRetrieval().run_all(build_retrievers(settings), cases)
    text = "\n".join(format_metrics(m) for m in metrics)
    print(text)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    return 0


def _cmd_experiment(args: argparse.Namespace) -> int:
    if args.list:
        for e in EXPERIMENTS:
            print(f"{e.name:10s} {e.description}")
        return 0
    settings = Settings.from_env()
    for experiment in find_experiments(args.names):
        print(f"== {experiment.name}: {experiment.description}", flush=True)
        print(run_experiment(experiment, settings, args.results_dir, args.rerank, args.skip_ingest))
    return 0


def _cmd_answers(args: argparse.Namespace) -> int:
    settings = _settings_from(args)
    cases = load_golden_cases(settings.golden_path)
    answerer = build_answerer(settings)
    answers = []
    for number, case in enumerate(cases, start=1):
        print(number, case.question, flush=True)
        answers.append(answerer.run(case.question))
    title = args.title or f"Respostas geradas ({settings.llm_model}, k={settings.answer_k})"
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(format_answers_markdown(title, cases, answers), encoding="utf-8")
    return 0


COMMANDS = {
    "ingest": _cmd_ingest,
    "ask": _cmd_ask,
    "eval": _cmd_eval,
    "experiment": _cmd_experiment,
    "answers": _cmd_answers,
}


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return COMMANDS[args.command](args)


if __name__ == "__main__":
    raise SystemExit(main())
