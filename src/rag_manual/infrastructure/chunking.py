"""Divisão do texto em trechos: tamanho fixo (base) e por seção (melhoria)."""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass

from rag_manual.domain.models import Chunk, Page

MIN_CHUNK_CHARS = 50  # trechos menores que isso são restos e são descartados


def clean_text(text: str) -> str:
    text = re.sub(r"-\n(\w)", r"\1", text)  # junta palavra hifenizada no fim da linha
    text = re.sub(r"\s+", " ", text)  # quebras e espaços repetidos viram um espaço
    return text.strip()


def split_text(text: str, size: int, overlap: int) -> list[str]:
    """Corta em trechos de até `size` caracteres, preferindo terminar num ponto final."""
    pieces: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        if end < len(text):
            cut = text.rfind(". ", start + size // 2, end)
            if cut != -1:
                end = cut + 1
        pieces.append(text[start:end].strip())
        if end >= len(text):
            break
        start = end - overlap
    return [p for p in pieces if len(p) > MIN_CHUNK_CHARS]


class FixedSizeChunker:
    """Trechos de tamanho fixo por página, sem olhar para a estrutura do manual."""

    def __init__(self, size: int = 800, overlap: int = 150) -> None:
        self._size = size
        self._overlap = overlap

    def chunk(self, pages: Sequence[Page]) -> list[Chunk]:
        chunks: list[Chunk] = []
        for page in pages:
            pieces = split_text(clean_text(page.text), self._size, self._overlap)
            chunks.extend(
                Chunk(id=f"p{page.number}-c{i}", page=page.number, text=piece)
                for i, piece in enumerate(pieces)
            )
        return chunks


# Cabeçalho repetido no topo das páginas do manual:
# "Motores Elétricos | 232" (páginas ímpares) ou "162 | Motores Elétricos" (pares),
# seguido do nome do capítulo em maiúsculas.
PAGE_HEADER = re.compile(r"\A\s*(?:Motores Elétricos \| \d+|\d+ \| Motores Elétricos)[ \t]*\n")
HEADING = re.compile(r"^(\d{1,2}(?:\.\d+){0,3})\s+([A-ZÀ-Ý][A-ZÀ-Ý0-9 /\-()]*)$")
HEADING_WORD = re.compile(r"[A-ZÀ-Ý]{4}")  # descarta "440 V", "1 RT1 ..." e similares
WRAPPED_HEADING_MIN_CHARS = 55  # títulos longos quebram em duas linhas no PDF


def _is_upper(line: str) -> bool:
    return line == line.upper() and any(ch.isalpha() for ch in line)


def strip_page_header(text: str) -> tuple[str, str]:
    """Tira o cabeçalho repetido. Devolve (texto sem cabeçalho, nome do capítulo).

    Se a página não tiver o cabeçalho esperado, devolve o texto como está.
    """
    match = PAGE_HEADER.match(text)
    if not match:
        return text, ""
    rest = text[match.end() :]
    first, _, remaining = rest.partition("\n")
    if _is_upper(first.strip()):
        return remaining, first.strip()
    return rest, ""


@dataclass(frozen=True)
class _Segment:
    section: str
    text: str


def _parse_heading(lines: Sequence[str], index: int) -> tuple[str, str, int] | None:
    """Se a linha `index` é título numerado, devolve (número, título completo, linhas usadas)."""
    line = lines[index].strip()
    match = HEADING.match(line)
    if not match or not HEADING_WORD.search(line):
        return None
    title, used = line, 1
    following = lines[index + 1].strip() if index + 1 < len(lines) else ""
    if (
        len(line) >= WRAPPED_HEADING_MIN_CHARS
        and _is_upper(following)
        and not following.endswith("!")
        and not HEADING.match(following)
    ):
        title, used = f"{line} {following}", 2
    return match.group(1), title, used


class SectionAwareChunker:
    """Divide por seção e põe o título da seção no começo de cada trecho.

    - Tira o cabeçalho repetido de cada página.
    - Detecta títulos numerados em maiúsculas ("5.3 MANCAIS").
    - Nunca junta texto de duas seções no mesmo trecho.
    - Mantém a página. A seção continua valendo na página seguinte, até aparecer outro título.
    - O prefixo é "capítulo > seção", por exemplo "8 MANUTENÇÃO > 8.2 LUBRIFICAÇÃO".
    """

    def __init__(self, size: int = 800, overlap: int = 150) -> None:
        self._size = size
        self._overlap = overlap

    def chunk(self, pages: Sequence[Page]) -> list[Chunk]:
        chunks: list[Chunk] = []
        chapter, section = "", ""
        for page in pages:
            body, caption = strip_page_header(page.text)
            if caption and not chapter:
                chapter = caption
            segments, chapter, section = self._segments(body, chapter, section)
            index = 0
            for segment in segments:
                for piece in split_text(clean_text(segment.text), self._size, self._overlap):
                    text = f"[{segment.section}] {piece}" if segment.section else piece
                    chunks.append(
                        Chunk(
                            id=f"p{page.number}-c{index}",
                            page=page.number,
                            text=text,
                            section=segment.section,
                        )
                    )
                    index += 1
        return chunks

    @staticmethod
    def _label(chapter: str, section: str) -> str:
        if chapter and section and section != chapter:
            return f"{chapter} > {section}"
        return section or chapter

    def _segments(self, body: str, chapter: str, section: str) -> tuple[list[_Segment], str, str]:
        lines = body.split("\n")
        segments: list[_Segment] = []
        buffer: list[str] = []
        index = 0
        while index < len(lines):
            heading = _parse_heading(lines, index)
            if heading is None:
                buffer.append(lines[index])
                index += 1
                continue
            number, title, used = heading
            segments.append(_Segment(self._label(chapter, section), "\n".join(buffer)))
            buffer = []
            if "." not in number:
                chapter, section = title, ""
            else:
                section = title
            index += used
        segments.append(_Segment(self._label(chapter, section), "\n".join(buffer)))
        return segments, chapter, section
