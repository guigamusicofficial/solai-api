import os
import httpx
from openai import OpenAI


# ============================================================
# CONFIGURAÇÃO DO MOTOR
# ============================================================

API_KEY = os.environ.get("OPENAI_API_KEY", "").strip()
BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").strip()
PROXY_URL = os.environ.get("PROXY_URL", "").strip()
MODEL_NAME = os.environ.get("OPENAI_MODEL", "gpt-4o-mini").strip() or "gpt-4o-mini"

http_client = None
if PROXY_URL:
    http_client = httpx.Client(proxy=PROXY_URL)

client = None
if API_KEY:
    try:
        client = OpenAI(
            api_key=API_KEY,
            base_url=BASE_URL,
            http_client=http_client
        )
    except Exception as erro:
        print(f"[Aviso] Cliente OpenAI não inicializado: {erro}")


# ============================================================
# GERAR RESPOSTA USANDO A FUSÃO DE MODELOS
# ============================================================

def gerar_resposta(instrucoes, historico):
    if not client or not API_KEY:
        return (
            "A API da IA ainda não está configurada neste ambiente. "
            "Configure OPENAI_API_KEY e OPENAI_BASE_URL para ativar as respostas reais."
        )

    try:
        mensagens = [
            {
                "role": "system",
                "content": instrucoes
            },
            *historico
        ]

        resposta = client.chat.completions.create(
            model=MODEL_NAME,
            messages=mensagens,
            temperature=0.7,
            max_tokens=1024
        )

        texto = resposta.choices[0].message.content
        if texto:
            print(f"[Motor: {MODEL_NAME}]")
            return texto.strip()

    except Exception as erro:
        print(f"\n[Erro ao gerar resposta com o modelo {MODEL_NAME}]: {erro}\n")
        return "Tive um problema técnico para processar a resposta agora."

    return "Não consegui gerar uma resposta válida no momento."
