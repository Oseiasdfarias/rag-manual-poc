"""Responde usando os trechos recuperados, citando a página."""
import os
import sys

from openai import OpenAI

from search import busca_hibrida

PROMPT = """Você é um assistente de manutenção. Responda usando SOMENTE os trechos do manual abaixo.
Cite a página de cada informação no formato (p. N).
Se os trechos não trazem a resposta, responda apenas: "Não encontrei isso no manual."
Não complete com conhecimento próprio.

Trechos:
{contexto}

Pergunta: {pergunta}"""


def responder(pergunta: str, k: int = 5) -> tuple[str, list[dict]]:
    trechos = busca_hibrida(pergunta, k)
    contexto = "\n\n".join(f"[p. {t['pagina']}] {t['texto']}" for t in trechos)
    cliente = OpenAI(
        base_url=os.getenv("LLM_BASE_URL"),  # vazio = OpenAI; Ollama: http://localhost:11434/v1
        api_key=os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY"),
    )
    r = cliente.chat.completions.create(
        model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
        temperature=0,
        messages=[{"role": "user", "content": PROMPT.format(contexto=contexto, pergunta=pergunta)}],
    )
    return r.choices[0].message.content, trechos


if __name__ == "__main__":
    resposta, trechos = responder(" ".join(sys.argv[1:]))
    print(resposta)
    print("\nPáginas usadas:", [t["pagina"] for t in trechos])
