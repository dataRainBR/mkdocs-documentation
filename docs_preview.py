# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "playwright>=1.47",
# ]
# ///
"""Atualiza referências, builda a documentação e abre o resultado no navegador.

Uso:
    uv run docs_preview.py
    uv run docs_preview.py --generate-references

Este script é um "script uv" autocontido (metadados PEP 723 no topo do
arquivo): ao executá-lo com `uv run docs_preview.py`, o `uv` cria
automaticamente um ambiente efêmero só com o `playwright` instalado — não é
necessário rodar `uv add`/`pip install` manualmente antes.

Passo a passo:
    1. Gera docs/referencias.md a partir das dependências declaradas no
       pyproject.toml ou requirements.txt.
    2. Executa o `mkdocs build` do `.venv` do projeto diretamente (grupo
       de dependências `docs`: mkdocs, mkdocs-material, mkdocstrings),
       gerando o site estático em `site/`. Chama o binário direto em vez
       de `uv run mkdocs build` para não depender da sincronização do
       `uv`, que trava com frequência quando o `.venv` está dentro de
       uma pasta sincronizada pelo OneDrive.
    3. Garante que o navegador Chromium do Playwright esteja instalado
       (`playwright install chromium`), baixando-o na primeira execução
       caso ainda não exista.
    4. Serve o diretório `site/` localmente via `http.server` (necessário
       para a busca do Material funcionar — abrir `index.html` direto
       como `file://` bloqueia o carregamento do índice de busca).
    5. Abre a página inicial em um navegador Chromium controlado pelo
       Playwright e mantém a janela aberta até você apertar Enter no
       terminal.
"""

from __future__ import annotations

import argparse
import re
import socket
import subprocess
import sys
import threading
import tomllib
from contextlib import closing
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SITE_DIR = PROJECT_ROOT / "site"
REQUIREMENT_PATTERN = re.compile(
    r"^\s*([A-Za-z0-9][A-Za-z0-9._-]*)(?:\[([^\]]+)\])?(.*)$"
)


def _normalize_package_name(name: str) -> str:
    """Normaliza o nome de uma distribuição conforme a convenção do PyPI."""
    return re.sub(r"[-_.]+", "-", name).lower()


def _parse_requirement(requirement: str) -> tuple[str, str, str]:
    """Extrai nome, especificação e URL de referência de uma dependência."""
    match = REQUIREMENT_PATTERN.match(requirement)
    if match is None:
        raise ValueError(f"Declaração de dependência inválida: {requirement}")

    name, extras, specifier = match.groups()
    display_name = f"{name}[{extras}]" if extras else name
    specifier = specifier.strip()

    if specifier.startswith("@"):
        reference = specifier[1:].strip()
        if not reference:
            raise ValueError(f"Referência direta vazia: {requirement}")
        return display_name, specifier, reference

    return (
        display_name,
        specifier,
        f"https://pypi.org/project/{_normalize_package_name(name)}/",
    )


def _read_requirements_file(
    requirements_path: Path, visited: set[Path] | None = None
) -> list[str]:
    """Lê requisitos diretos e arquivos incluídos com ``-r``."""
    if visited is None:
        visited = set()

    requirements_path = requirements_path.resolve()
    if requirements_path in visited:
        raise ValueError(f"Referência circular em requirements: {requirements_path}")
    if not requirements_path.is_file():
        raise FileNotFoundError(f"Arquivo de requisitos não encontrado: {requirements_path}")

    visited.add(requirements_path)
    requirements: list[str] = []
    ignored_options = (
        "--index-url",
        "--extra-index-url",
        "--find-links",
        "--trusted-host",
        "--no-index",
        "--pre",
    )

    for raw_line in requirements_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        include_match = re.match(r"^(?:-r|--requirement)\s+(.+)$", line)
        if include_match:
            included_path = requirements_path.parent / include_match.group(1).strip()
            requirements.extend(_read_requirements_file(included_path, visited))
            continue

        if line.startswith(ignored_options) or line.startswith(("-c ", "--constraint ")):
            continue

        editable_prefix = re.match(r"^(?:-e|--editable)\s+(.+)$", line)
        if editable_prefix:
            url = editable_prefix.group(1).strip()
            egg_match = re.search(r"#egg=([A-Za-z0-9][A-Za-z0-9._-]*)", url)
            if egg_match is None:
                raise ValueError(f"Requisito editável sem #egg=<pacote>: {line}")
            requirements.append(f"{egg_match.group(1)} @ {url}")
            continue

        if line.startswith("-"):
            raise ValueError(f"Opção de requirements não suportada: {line}")

        line = re.sub(r"\s+#.*$", "", line)
        line = re.sub(r"\s+--hash(?:=|\s+)\S+", "", line)
        requirements.append(line.strip())

    visited.remove(requirements_path)
    return requirements


def _dependency_references(project_root: Path) -> list[tuple[str, str, str]]:
    """Obtém dependências do pyproject.toml ou, como alternativa, requirements.txt."""
    pyproject_path = project_root / "pyproject.toml"
    sources: dict[str, object] = {}
    requirement_strings: list[str] = []

    if pyproject_path.is_file():
        project_data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
        requirement_strings = project_data.get("project", {}).get("dependencies", [])
        sources = project_data.get("tool", {}).get("uv", {}).get("sources", {})

    if not requirement_strings:
        requirement_strings = _read_requirements_file(project_root / "requirements.txt")

    if not requirement_strings:
        raise ValueError("Nenhuma dependência encontrada no pyproject.toml ou requirements.txt.")

    references: list[tuple[str, str, str]] = []
    for requirement in requirement_strings:
        name, specifier, reference = _parse_requirement(requirement)
        source = sources.get(name.split("[", 1)[0])
        if isinstance(source, dict) and isinstance(source.get("git"), str):
            git_url = source["git"].removeprefix("git+")
            revision = source.get("rev")
            if revision and git_url.startswith("https://github.com/"):
                reference = f"{git_url.removesuffix('.git')}/commit/{revision}"
            else:
                reference = git_url
        references.append((name, specifier, reference))

    return references


def generate_references_markdown(project_root: Path = PROJECT_ROOT) -> Path:
    """Gera ``docs/referencias.md`` com referências extraídas das dependências.

    Lê as dependências de ``pyproject.toml`` (incluindo origens Git definidas
    em ``tool.uv.sources``) ou, se não houver uma lista de dependências,
    usa ``requirements.txt``. Para dependências GitHub com revisão fixada, cria
    um link para o commit; para pacotes sem URL direta, cria uma referência à
    página correspondente no PyPI. A página gerada também documenta a
    instalação com ``uv sync`` e inclui esta função via ``mkdocstrings``.

    A função roda antes do build em ``run_mkdocs_build`` e no workflow de
    publicação. Também pode ser chamada isoladamente com
    ``uv run docs_preview.py --generate-references``.

    Args:
        project_root: Raiz do projeto que contém os arquivos de dependências.

    Returns:
        Path: Caminho do arquivo Markdown gerado.

    Raises:
        FileNotFoundError: Se não houver um ``requirements.txt`` de fallback.
        ValueError: Se as dependências estiverem vazias ou malformadas.
    """
    project_root = project_root.resolve()
    dependencies = _dependency_references(project_root)
    rows = [
        "| Pacote | Requisito declarado | Referência |",
        "|---|---|---|",
    ]

    for name, specifier, reference in dependencies:
        safe_name = name.replace("|", r"\|")
        safe_specifier = (specifier or "sem versão mínima").replace("|", r"\|")
        safe_reference = reference.replace("|", r"\|")
        rows.append(
            f"| `{safe_name}` | `{safe_specifier}` | [Abrir referência]({safe_reference}) |"
        )

    content = "\n".join(
        [
            "# Referências de pacotes Python",
            "",
            "Esta página é gerada automaticamente a partir das dependências do projeto.",
            "Para atualizar a lista manualmente, execute `uv run docs_preview.py --generate-references`.",
            "",
            *rows,
            "",
            "## Instalar os pacotes",
            "",
            "Na raiz do repositório, instale as dependências e as versões registradas no lockfile com:",
            "",
            "```bash",
            "uv sync",
            "```",
            "",
            "## Função de extração",
            "",
            "A função abaixo lê o `pyproject.toml` ou o `requirements.txt` e gera esta página:",
            "",
            "::: docs_preview.generate_references_markdown",
            "",
        ]
    )

    output_path = project_root / "docs" / "referencias.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    return output_path


def run_mkdocs_build() -> None:
    """Atualiza as referências e executa o ``mkdocs build`` do projeto.

    Chama o executável ``mkdocs`` dentro de ``.venv`` diretamente, em vez
    de ``uv run mkdocs build``: o ``uv run`` faz uma sincronizacao do
    ambiente antes de rodar, e isso trava com frequencia quando o `.venv`
    fica dentro de uma pasta sincronizada pelo OneDrive (o OneDrive
    bloqueia arquivos do `.venv` durante a sincronizacao, e o `uv`
    recebe "Acesso negado" ao tentar reinstalar pacotes). Antes de executar
    o binário do MkDocs, gera ``docs/referencias.md`` a partir de
    ``pyproject.toml`` ou ``requirements.txt``.

    Raises:
        SystemExit: Se o `mkdocs` nao existir em `.venv` (rode
            `uv sync --group docs` primeiro), ou se o build falhar
            (codigo de saida diferente de 0), ou se o diretorio `site/`
            nao existir apos o build.
        FileNotFoundError: Se a página de referências não puder ser gerada
            porque não há um arquivo de dependências de fallback.
        ValueError: Se as dependências estiverem ausentes ou malformadas.

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

    references_path = generate_references_markdown()
    print(f"==> Referências atualizadas em: {references_path}")
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
    """Executa o preview ou gera apenas a página de referências.

    Por padrão, atualiza as referências, executa o build do MkDocs e abre o
    site no Chromium. Com ``--generate-references``, atualiza
    ``docs/referencias.md`` e encerra sem abrir o navegador.

    Returns:
        None: Esta função não retorna valor.
    """
    parser = argparse.ArgumentParser(description="Builda ou atualiza a documentação.")
    parser.add_argument(
        "--generate-references",
        action="store_true",
        help="Gera docs/referencias.md a partir das dependências do projeto.",
    )
    args = parser.parse_args()

    if args.generate_references:
        print(f"==> Referências atualizadas em: {generate_references_markdown()}")
        return

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
