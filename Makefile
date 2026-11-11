.PHONY: install ingest eval ask answers experiments test lint format

PY ?= python
Q ?= Qual a altitude máxima de operação do motor?

install:  ## instala o pacote e as ferramentas de desenvolvimento
	uv pip install torch --index-url https://download.pytorch.org/whl/cpu
	uv pip install -e ".[dev]"

ingest:  ## lê data/manual.pdf e cria os índices
	rag-manual ingest

eval:  ## mede hit@3 e MRR da busca
	rag-manual eval

ask:  ## responde uma pergunta: make ask Q="sua pergunta"
	rag-manual ask $(Q)

answers:  ## responde as 15 perguntas do conjunto de teste
	rag-manual answers --out results/respostas.md

experiments:  ## roda todos os experimentos (precisa dos modelos baixados)
	rag-manual experiment --rerank

test:  ## testes unitários (rápidos, sem baixar modelos)
	pytest

lint:  ## confere o estilo do código
	ruff check src tests
	ruff format --check src tests

format:  ## formata o código
	ruff format src tests
