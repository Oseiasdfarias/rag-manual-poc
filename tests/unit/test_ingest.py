from pathlib import Path

import pytest

from rag_manual.application.ingest import IngestManual, NoTextExtractedError
from rag_manual.domain.models import Page
from rag_manual.infrastructure.chunking import FixedSizeChunker
from tests.conftest import FakeEmbedder, FakeKeywordIndex, FakeLoader, FakeVectorStore

TEXT = "Frase de teste do manual de motores. " * 5


def _use_case(pages):
    store, index, embedder = FakeVectorStore(), FakeKeywordIndex(), FakeEmbedder()
    use_case = IngestManual(FakeLoader(pages), FixedSizeChunker(), embedder, store, index)
    return use_case, store, index, embedder


def test_ingest_grava_nos_dois_indices():
    use_case, store, index, embedder = _use_case([Page(1, TEXT), Page(2, TEXT)])
    report = use_case.run(Path("x.pdf"))
    assert (report.pages, report.chunks) == (2, 2)
    assert len(store.chunks) == 2 and len(index.built) == 2
    assert len(embedder.passages) == 2
    assert store.reset_calls == 1


def test_ingest_sem_texto_levanta_erro():
    use_case, store, _, _ = _use_case([Page(1, ""), Page(2, "oi")])
    with pytest.raises(NoTextExtractedError):
        use_case.run(Path("x.pdf"))
    assert store.reset_calls == 0  # não apaga o índice antigo se não há o que gravar
