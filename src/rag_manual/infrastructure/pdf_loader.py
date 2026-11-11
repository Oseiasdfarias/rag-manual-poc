"""Leitura do PDF com pypdf."""

from __future__ import annotations

import logging
from pathlib import Path

from pypdf import PdfReader

from rag_manual.domain.models import Page


class PypdfLoader:
    """Devolve o texto bruto de cada página (com quebras de linha), numeradas a partir de 1."""

    def load(self, path: Path) -> list[Page]:
        logging.getLogger("pypdf").setLevel(logging.ERROR)  # avisos de fonte poluem a saída
        reader = PdfReader(path)
        return [Page(number=n, text=p.extract_text() or "") for n, p in enumerate(reader.pages, 1)]
