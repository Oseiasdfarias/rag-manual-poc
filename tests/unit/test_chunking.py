from rag_manual.domain.models import Page
from rag_manual.infrastructure.chunking import (
    FixedSizeChunker,
    SectionAwareChunker,
    clean_text,
    split_text,
    strip_page_header,
)

FILLER = "Frase de teste do manual. " * 12  # cerca de 300 caracteres


def test_clean_text_junta_hifenizacao_e_espacos():
    assert clean_text("manu-\ntenção  do\nmotor ") == "manutenção do motor"


def test_split_text_respeita_tamanho_e_termina_em_ponto():
    text = FILLER * 6
    pieces = split_text(text, size=400, overlap=50)
    assert len(pieces) > 1
    assert all(len(p) <= 400 for p in pieces)
    assert pieces[0].endswith(".")


def test_split_text_descarta_resto_curto():
    assert split_text("curto", size=800, overlap=150) == []


def test_split_text_tem_sobreposicao():
    text = "a" * 1000
    first, second = split_text(text, size=500, overlap=100)[:2]
    assert len(first) == 500
    assert second.startswith("a" * 100)


def test_fixed_chunker_ids_e_paginas():
    pages = [Page(1, FILLER), Page(2, FILLER * 4)]
    chunks = FixedSizeChunker(size=800, overlap=150).chunk(pages)
    assert chunks[0].id == "p1-c0"
    assert {c.page for c in chunks} == {1, 2}
    assert [c.id for c in chunks if c.page == 2][:2] == ["p2-c0", "p2-c1"]
    assert all(c.section == "" for c in chunks)


def test_fixed_chunker_nao_atravessa_paginas():
    chunks = FixedSizeChunker().chunk([Page(1, FILLER), Page(2, FILLER)])
    assert len(chunks) == 2
    assert chunks[0].text == clean_text(FILLER)


def test_strip_page_header_pagina_impar_e_par():
    odd = "Motores Elétricos | 232 \nPROBLEMAS X SOLUÇÕES\n10 PROBLEMAS X SOLUÇÕES\nTexto"
    even = "162 | Motores Elétricos\nINSTALAÇÃO\nTexto"
    assert strip_page_header(odd) == ("10 PROBLEMAS X SOLUÇÕES\nTexto", "PROBLEMAS X SOLUÇÕES")
    assert strip_page_header(even) == ("Texto", "INSTALAÇÃO")


def test_strip_page_header_sem_cabecalho_nao_mexe():
    text = "SUMÁRIO\n1 DEFINIÇÕES"
    assert strip_page_header(text) == (text, "")


def test_strip_page_header_nao_corta_se_linha_seguinte_nao_e_titulo():
    text = "Motores Elétricos | 10 \nTexto normal do corpo"
    assert strip_page_header(text) == ("Texto normal do corpo", "")


def _page(number: int, body: str) -> Page:
    return Page(number, f"Motores Elétricos | {number} \nMANUTENÇÃO\n{body}")


def test_section_chunker_poe_titulo_em_todos_os_trechos():
    body = "8 MANUTENÇÃO\n8.2 LUBRIFICAÇÃO\n" + FILLER * 5
    chunks = SectionAwareChunker(size=400, overlap=50).chunk([_page(60, body)])
    assert len(chunks) > 1
    assert all(c.text.startswith("[8 MANUTENÇÃO > 8.2 LUBRIFICAÇÃO] ") for c in chunks)
    assert all(c.section == "8 MANUTENÇÃO > 8.2 LUBRIFICAÇÃO" for c in chunks)
    assert all(c.page == 60 for c in chunks)


def test_section_chunker_nao_mistura_secoes():
    body = f"8.1 INSPEÇÃO GERAL\n{FILLER}\n8.2 LUBRIFICAÇÃO\n{FILLER}"
    chunks = SectionAwareChunker().chunk([_page(59, body)])
    assert len(chunks) == 2
    assert "INSPEÇÃO" in chunks[0].section and "INSPEÇÃO" not in chunks[1].section
    assert "LUBRIFICAÇÃO" in chunks[1].section
    assert chunks[0].id == "p59-c0" and chunks[1].id == "p59-c1"


def test_section_chunker_secao_continua_na_pagina_seguinte():
    chunks = SectionAwareChunker().chunk(
        [_page(59, f"8.2 LUBRIFICAÇÃO\n{FILLER}"), _page(60, FILLER)]
    )
    assert chunks[1].page == 60
    assert chunks[1].section.endswith("8.2 LUBRIFICAÇÃO")


def test_section_chunker_titulo_longo_em_duas_linhas():
    title = "4.2 PROCEDIMENTO PARA TOMBAMENTO DE MOTORES W22/WEG GENERAL"
    chunks = SectionAwareChunker().chunk([_page(18, f"{title}\nPURPOSE/WIN VERTICAIS\n{FILLER}")])
    assert chunks[0].section.endswith(f"{title} PURPOSE/WIN VERTICAIS")


def test_section_chunker_ignora_linhas_que_nao_sao_titulo():
    body = f"440 V\n1 RT1 1 RT2 1 RT2\n{FILLER}"
    chunks = SectionAwareChunker().chunk([_page(45, body)])
    assert chunks[0].section == "MANUTENÇÃO"
    assert "440 V" in chunks[0].text


def test_section_chunker_tira_cabecalho_do_texto():
    chunks = SectionAwareChunker().chunk([_page(61, FILLER)])
    assert "Motores Elétricos |" not in chunks[0].text


def test_section_chunker_capitulo_sem_subsecao_usa_o_capitulo():
    chunks = SectionAwareChunker().chunk([_page(76, f"10 PROBLEMAS X SOLUÇÕES\n{FILLER}")])
    assert chunks[0].section == "10 PROBLEMAS X SOLUÇÕES"
    assert chunks[0].text.startswith("[10 PROBLEMAS X SOLUÇÕES] ")
