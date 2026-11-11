from rag_manual.application.answering import AnswerQuestion, build_context, build_prompt
from tests.conftest import FakeLLM, FakeRetriever, hit


def test_contexto_traz_pagina_e_texto():
    context = build_context([hit("a", 54, "altitude 1000 m"), hit("b", 20, "graxa")])
    assert context == "[p. 54] altitude 1000 m\n\n[p. 20] graxa"


def test_prompt_tem_regras_pergunta_e_trechos():
    prompt = build_prompt("Qual a altitude?", [hit("a", 54, "1000 m")])
    assert "SOMENTE os trechos" in prompt
    assert "(p. N)" in prompt
    assert '"Não encontrei isso no manual."' in prompt
    assert "[p. 54] 1000 m" in prompt
    assert prompt.endswith("Pergunta: Qual a altitude?")


def test_answer_question_usa_k_e_devolve_fontes():
    retriever = FakeRetriever([hit(f"c{i}", i + 1) for i in range(10)])
    llm = FakeLLM("Resposta (p. 1).")
    answer = AnswerQuestion(retriever, llm, k=3).run("pergunta")
    assert retriever.requested_k == [3]
    assert answer.text == "Resposta (p. 1)."
    assert answer.pages == (1, 2, 3)
    assert len(llm.prompts) == 1 and "pergunta" in llm.prompts[0]
