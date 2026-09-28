import json
import os
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

try:
    from .config import CONFIG, LIMITE_HISTORICO
    from .core import gerar_resposta
    from .memory import (
        carregar_historico,
        carregar_memoria,
        corrigir_memoria_mojibake,
        criar_contexto_memoria,
        organizar_memoria,
        salvar_historico,
        salvar_memoria,
        atualizar_memoria,
        limitar_historico,
    )
    from .personality import criar_instrucoes
except ImportError:
    from config import CONFIG, LIMITE_HISTORICO
    from core import gerar_resposta
    from memory import (
        carregar_historico,
        carregar_memoria,
        corrigir_memoria_mojibake,
        criar_contexto_memoria,
        organizar_memoria,
        salvar_historico,
        salvar_memoria,
        atualizar_memoria,
        limitar_historico,
    )
    from personality import criar_instrucoes

BASE_DIR = Path(__file__).resolve().parents[1]
WEB_DIR = BASE_DIR / "web"
HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 8080))
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.guigamusic.com.br")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")


def _is_memory_message(texto):
    if not isinstance(texto, str):
        return False
    padrao = re.compile(
        r"\b(meu nome é|pode me chamar de|quero que me chame de|eu gosto de|gosto muito de|eu curto|curto muito|adoro|odeio|meu projeto|estou construindo|moro em|sou de)\b",
        re.IGNORECASE,
    )
    return bool(padrao.search(texto))


def _process_chat(message, companheira_nome="sol"):
    mensagem = (message or "").strip()
    if not mensagem:
        return {"resposta": "Você pode me mandar uma mensagem para continuar a conversa."}

    memoria = carregar_memoria()
    memoria = corrigir_memoria_mojibake(memoria)
    memoria = organizar_memoria(memoria)

    if _is_memory_message(mensagem):
        memoria = atualizar_memoria(mensagem, memoria)
        salvar_memoria(memoria)

    historico = carregar_historico() or []
    historico.append({"role": "user", "content": mensagem})
    historico = limitar_historico(historico)
    salvar_historico(historico)

    contexto = criar_contexto_memoria(memoria)
    instrucoes = criar_instrucoes(memoria, contexto, companheira_nome=companheira_nome)
    resposta = gerar_resposta(instrucoes, historico)

    historico.append({"role": "assistant", "content": resposta})
    historico = limitar_historico(historico)
    salvar_historico(historico)

    return {"resposta": resposta}


class SolHandler(BaseHTTPRequestHandler):
    def _send_json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "https://sol.guigamusic.com.br")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "https://sol.guigamusic.com.br")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            target = WEB_DIR / "index.html"
            if target.exists():
                content = target.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(content)
                return

        if self.path.startswith("/web/"):
            rel = self.path[len("/web/") :]
            target = (WEB_DIR / rel).resolve()
            if WEB_DIR in target.parents or target == WEB_DIR:
                if target.exists() and target.is_file():
                    content = target.read_bytes()
                    mime, _ = mimetypes.guess_type(str(target))
                    if mime is None:
                        mime = "application/octet-stream"
                    self.send_response(200)
                    self.send_header("Content-Type", mime)
                    self.send_header("Content-Length", str(len(content)))
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(content)
                    return

        if self.path == "/health":
            self._send_json({"status": "ok", "project": "Sol AI", "base_url": OPENAI_BASE_URL})
            return

        self._send_json({"error": "recurso não encontrado"}, status=404)

    def do_POST(self):
        if self.path != "/api/chat":
            self._send_json({"error": "endpoint não encontrado"}, status=404)
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length)

        try:
            payload = json.loads(raw_body.decode("utf-8"))
        except Exception:
            self._send_json({"error": "JSON inválido"}, status=400)
            return

        mensagem = payload.get("message") if isinstance(payload, dict) else None
        companheira = payload.get("companion") if isinstance(payload, dict) else "sol"
        resposta = _process_chat(mensagem, companheira_nome=companheira)
        self._send_json(resposta)


def run():
    os.makedirs(WEB_DIR, exist_ok=True)
    server = HTTPServer((HOST, PORT), SolHandler)
    print(f"Servidor Sol AI em {HOST}:{PORT}")
    print(f"Frontend: http://localhost:{PORT}/")
    print(f"API: http://localhost:{PORT}/api/chat")
    server.serve_forever()


if __name__ == "__main__":
    import mimetypes
    mimetypes.init()
    run()
