"""Caso de uso: responder uma pergunta usando só os trechos recuperados."""

from __future__ import annotations

from collections.abc import Sequence

from rag_manual.domain.models import Answer, RetrievedChunk
from rag_manual.domain.ports import LLM, Retriever

PROMPT_TEMPLATE = """Você é um assistente de manutenção. Responda usando SOMENTE os trechos do manual abaixo.
Cite a página de cada informação no formato (p. N).
Se os trechos não trazem a resposta, responda apenas: "Não encontrei isso no manual."
Não complete com conhecimento próprio.

Trechos:
{context}

Pergunta: {question}"""


def build_context(chunks: Sequence[RetrievedChunk]) -> str:
    return "\n\n".join(f"[p. {c.page}] {c.text}" for c in chunks)


def build_prompt(question: str, chunks: Sequence[RetrievedChunk]) -> str:
    return PROMPT_TEMPLATE.format(context=build_context(chunks), question=question)


class AnswerQuestion:
    def __init__(self, retriever: Retriever, llm: LLM, k: int = 5) -> None:
        self._retriever = retriever
        self._llm = llm
        self._k = k

    def run(self, question: str) -> Answer:
        sources = self._retriever.search(question, self._k)
        text = self._llm.complete(build_prompt(question, sources))
        return Answer(question=question, text=text, sources=tuple(sources))
