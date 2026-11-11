# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "playwright>=1.47",
# ]
# ///
"""Builda a documentação (MkDocs) e abre o resultado no navegador via Playwright.

Uso:
    uv run docs_preview.py

Este script é um "script uv" autocontido (metadados PEP 723 no topo do
arquivo): ao executá-lo com `uv run docs_preview.py`, o `uv` cria
automaticamente um ambiente efêmero só com o `playwright` instalado — não é
necessário rodar `uv add`/`pip install` manualmente antes.

Passo a passo:
    1. Executa o `mkdocs build` do `.venv` do projeto diretamente (grupo
       de dependências `docs`: mkdocs, mkdocs-material, mkdocstrings),
       gerando o site estático em `site/`. Chama o binário direto em vez
       de `uv run mkdocs build` para não depender da sincronização do
       `uv`, que trava com frequência quando o `.venv` está dentro de
       uma pasta sincronizada pelo OneDrive.
    2. Garante que o navegador Chromium do Playwright esteja instalado
       (`playwright install chromium`), baixando-o na primeira execução
       caso ainda não exista.
    3. Serve o diretório `site/` localmente via `http.server` (necessário
       para a busca do Material funcionar — abrir `index.html` direto
       como `file://` bloqueia o carregamento do índice de busca).
    4. Abre a página inicial em um navegador Chromium controlado pelo
       Playwright e mantém a janela aberta até você apertar Enter no
       terminal.
"""

from __future__ import annotations

import socket
import subprocess
import sys
import threading
from contextlib import closing
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SITE_DIR = PROJECT_ROOT / "site"


def run_mkdocs_build() -> None:
    """Executa o ``mkdocs build`` do ambiente do projeto, na raiz do projeto.

    Chama o executável ``mkdocs`` dentro de ``.venv`` diretamente, em vez
    de ``uv run mkdocs build``: o ``uv run`` faz uma sincronizacao do
    ambiente antes de rodar, e isso trava com frequencia quando o `.venv`
    fica dentro de uma pasta sincronizada pelo OneDrive (o OneDrive
    bloqueia arquivos do `.venv` durante a sincronizacao, e o `uv`
    recebe "Acesso negado" ao tentar reinstalar pacotes). Chamando o
    binario direto, pulamos essa sincronizacao.

    Raises:
        SystemExit: Se o `mkdocs` nao existir em `.venv` (rode
            `uv sync --group docs` primeiro), ou se o build falhar
            (codigo de saida diferente de 0), ou se o diretorio `site/`
            nao existir apos o build.

    Returns:
        None: Esta funcao nao retorna valor.
    """
    mkdocs_bin = (
        PROJECT_ROOT / ".venv" / "Scripts" / "mkdocs.exe"
        if sys.platform == "win32"
        else PROJECT_ROOT / ".venv" / "bin" / "mkdocs"
    )

    if not mkdocs_bin.exists():
        print(f"mkdocs nao encontrado em: {mkdocs_bin}")
        print("Rode `uv sync --group docs` na raiz do projeto primeiro.")
        raise SystemExit(1)

    print(f"==> Executando: {mkdocs_bin} build")

    result = subprocess.run([str(mkdocs_bin), "build"], cwd=str(PROJECT_ROOT))

    if result.returncode != 0:
        print("Build do MkDocs falhou. Abortando.")
        raise SystemExit(result.returncode)

    if not SITE_DIR.exists():
        print(f"Diretório do site não encontrado em: {SITE_DIR}")
        raise SystemExit(1)

    print(f"==> Build concluído em: {SITE_DIR}")


def find_free_port() -> int:
    """Encontra uma porta TCP livre na máquina local.

    Returns:
        int: Número de uma porta TCP livre em ``127.0.0.1``.
    """
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def start_local_server(directory: Path, port: int) -> ThreadingHTTPServer:
    """Inicia um servidor HTTP local servindo `directory`, em background.

    Args:
        directory (Path): Diretório a ser servido (ex.: `site/`).
        port (int): Porta TCP onde o servidor vai escutar.

    Returns:
        ThreadingHTTPServer: Instância do servidor já rodando em uma
            thread separada (`daemon=True`, não bloqueia o encerramento
            do script).
    """
    handler = partial(SimpleHTTPRequestHandler, directory=str(directory))
    server = ThreadingHTTPServer(("127.0.0.1", port), handler)

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    return server


def ensure_playwright_browser_installed() -> None:
    """Garante que o navegador Chromium do Playwright esteja instalado.

    Baixa o Chromium na primeira execução (pode levar alguns minutos);
    em execuções seguintes, o Playwright detecta que já está instalado
    e a chamada retorna quase imediatamente.

    Returns:
        None: Esta função não retorna valor.
    """
    print("==> Verificando instalação do Chromium (Playwright)...")

    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=False)


def open_in_browser(url: str) -> None:
    """Abre `url` em um navegador Chromium controlado pelo Playwright.

    Mantém o navegador aberto até o usuário apertar Enter no terminal,
    depois encerra o navegador e o contexto do Playwright de forma
    limpa.

    Args:
        url (str): URL a ser aberta (ex.: ``"http://127.0.0.1:8000/"``).

    Returns:
        None: Esta função não retorna valor.
    """
    from playwright.sync_api import sync_playwright

    print(f"==> Abrindo {url} no navegador (Playwright)...")

    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(
            headless=False,
            args=["--start-maximized"],
        )

        # `no_viewport=True` faz a pagina usar o tamanho real da janela do
        # navegador (maximizada) em vez do viewport fixo padrao do
        # Playwright (1280x720) - sem isso, a janela fica maximizada mas a
        # pagina continua renderizada como se a tela fosse pequena.
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        page.goto(url)

        input("\nNavegador aberto. Pressione Enter aqui para fechar...\n")

        browser.close()


def main() -> None:
    """Builda a documentação e abre o resultado no navegador.

    Returns:
        None: Esta função não retorna valor.
    """
    run_mkdocs_build()

    port = find_free_port()
    server = start_local_server(SITE_DIR, port)

    url = f"http://127.0.0.1:{port}/"

    print(f"==> Servindo {SITE_DIR} em {url}")

    ensure_playwright_browser_installed()

    try:
        open_in_browser(url)
    finally:
        print("==> Encerrando servidor local...")
        server.shutdown()


if __name__ == "__main__":
    main()
