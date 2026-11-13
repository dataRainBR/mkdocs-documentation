from __future__ import annotations

import argparse
import base64
import mimetypes
import re
import tempfile
import threading
import warnings
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path, PurePosixPath
from typing import Any, Iterator
from urllib.parse import urlparse

import yaml
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter
from yaml.nodes import MappingNode, ScalarNode, SequenceNode


PRINT_STYLES = """
@page {
  size: A4;
  margin: 26mm 15mm 25mm;
}

@media print {
  html, body, .md-main, .md-content {
    color: #132B40 !important;
    background: #FFFFFF !important;
    color-scheme: light;
  }
  a {
    color: #3791A6 !important;
  }
  pre, code {
    color: #132B40 !important;
  }
  .md-header, .md-tabs, .md-sidebar, .md-footer, .md-top {
    display: none !important;
  }
  .md-main__inner {
    display: block;
    max-width: none;
    margin: 0;
  }
  .md-content {
    max-width: none;
  }
  h1, h2, h3 {
    break-after: avoid;
  }
  img, svg {
    max-width: 100%;
    height: auto;
  }
  pre {
    white-space: pre-wrap;
    overflow-wrap: anywhere;
  }
}
"""


class _MkDocsConfigLoader(yaml.SafeLoader):
    pass


def _construct_ignored_tag(loader: _MkDocsConfigLoader, suffix: str, node: Any) -> Any:
    if isinstance(node, ScalarNode):
        return loader.construct_scalar(node)
    if isinstance(node, SequenceNode):
        return loader.construct_sequence(node)
    if isinstance(node, MappingNode):
        return loader.construct_mapping(node)
    raise TypeError(f"Tipo de nó YAML não suportado: {type(node).__name__}")


_MkDocsConfigLoader.add_multi_constructor("", _construct_ignored_tag)


def _source_title(source_path: Path) -> str:
    if source_path.suffix.lower() in {".md", ".markdown"}:
        for line in source_path.read_text(encoding="utf-8").splitlines():
            match = re.match(r"^\s*#\s+(.+?)\s*#*\s*$", line)
            if match:
                return match.group(1).strip()
    return source_path.stem.replace("-", " ").replace("_", " ").title()


def _image_data_uri(image_path: Path) -> str:
    if not image_path.is_file():
        raise FileNotFoundError(f"Imagem de identidade visual não encontrada: {image_path}")
    mime_type = mimetypes.guess_type(image_path.name)[0]
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError(f"Formato de imagem não suportado: {image_path.suffix}")
    encoded_image = base64.b64encode(image_path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded_image}"


def _logo_data_uri(site_path: Path, config: dict[str, Any]) -> str:
    theme = config.get("theme") or {}
    configured_logo = theme.get("logo") if isinstance(theme, dict) else None
    logo_relative = PurePosixPath(configured_logo or "assets/logo.png")
    logo_path = (site_path / Path(*logo_relative.parts)).resolve()
    if not logo_path.is_relative_to(site_path) or not logo_path.is_file():
        raise FileNotFoundError(
            f"Logo configurado não foi encontrado no site gerado: {logo_path}"
        )
    return _image_data_uri(logo_path)


def _header_footer_templates(
    logo_data_uri: str,
    footer_data_uri: str,
) -> tuple[str, str]:
    header = f"""
    <div style="width:100%; box-sizing:border-box; padding:0 2mm 2mm;
                display:flex; align-items:center; justify-content:space-between;
                border-bottom:1px solid #3791A6; color:#132B40;
                font:9px Arial,sans-serif;">
      <img src="{logo_data_uri}" style="width:32mm; max-height:11mm; object-fit:contain;">
      <span>DATA RAIN DOCUMENTATION</span>
    </div>
    """
    footer = f"""
    <div style="width:100%; box-sizing:border-box; padding:1mm 0 0;
                border-top:1px solid #F27507; text-align:center;">
      <img src="{footer_data_uri}"
           style="width:100%; max-height:16mm; object-fit:contain; object-position:center;">
    </div>
    """
    return header, footer


def _iter_nav(
    nav: Any,
    sections: tuple[str, ...] = (),
) -> Iterator[tuple[str, str, tuple[str, ...]]]:
    if isinstance(nav, list):
        for item in nav:
            yield from _iter_nav(item, sections)
    elif isinstance(nav, str):
        yield PurePosixPath(nav).stem, nav, sections
    elif isinstance(nav, dict):
        for title, item in nav.items():
            if isinstance(item, str):
                yield str(title), item, sections
            else:
                yield from _iter_nav(item, sections + (str(title),))


def _html_path(document: str, use_directory_urls: bool) -> PurePosixPath | None:
    if "://" in document:
        return None

    relative_path = PurePosixPath(
        document.replace("\\", "/").split("#", 1)[0].split("?", 1)[0]
    )
    if relative_path.suffix.lower() in {".md", ".markdown"}:
        if relative_path.name.lower() == "index.md":
            return relative_path.with_suffix(".html")
        if use_directory_urls:
            return relative_path.parent / relative_path.stem / "index.html"
        return relative_path.with_suffix(".html")
    if relative_path.suffix.lower() == ".html":
        return relative_path
    return None


def _rewrite_internal_links(page: Any, base_url: str | None) -> None:
    if base_url is None:
        return
    page.evaluate(
        """(baseUrl) => {
          for (const link of document.querySelectorAll("a[href]")) {
            const href = link.getAttribute("href");
            if (!href || href.startsWith("#")) continue;
            const target = new URL(href, window.location.href);
            if (target.origin !== window.location.origin) continue;
            const path = target.pathname.replace(/^\\/+/, "");
            const destination = new URL(path, baseUrl);
            destination.search = target.search;
            destination.hash = target.hash;
            link.href = destination.href;
          }
        }""",
        base_url,
    )


def export_to_pdf(
    site_dir: str | Path = "site",
    output_pdf: str | Path | None = None,
    mkdocs_config: str | Path = "mkdocs.yml",
    base_url: str | None = None,
) -> Path:
    """Render the MkDocs pages in navigation order and merge them into one PDF."""
    site_path = Path(site_dir).resolve()
    config_path = Path(mkdocs_config).resolve()
    if not site_path.is_dir():
        raise FileNotFoundError(
            f"Diretório HTML não encontrado: {site_path}. Execute `uv run mkdocs build` primeiro."
        )
    if not config_path.is_file():
        raise FileNotFoundError(f"Configuração MkDocs não encontrada: {config_path}")

    config = (
        yaml.load(
            config_path.read_text(encoding="utf-8"),
            Loader=_MkDocsConfigLoader,
        )
        or {}
    )
    nav = config.get("nav")
    if not nav:
        raise ValueError(
            "A configuração mkdocs.yml precisa definir `nav` para preservar a ordem das páginas."
        )

    use_directory_urls = config.get("use_directory_urls", True)
    docs_directory = Path(config.get("docs_dir", "docs"))
    docs_path = (config_path.parent / docs_directory).resolve()
    if not docs_path.is_dir():
        raise FileNotFoundError(f"Diretório de origem MkDocs não encontrado: {docs_path}")

    pages: list[tuple[str, tuple[str, ...], Path]] = []
    seen_paths: set[Path] = set()
    for title, document, sections in _iter_nav(nav):
        relative_html = _html_path(document, use_directory_urls)
        if relative_html is None:
            continue
        html_path = (site_path / Path(*relative_html.parts)).resolve()
        if not html_path.is_relative_to(site_path):
            raise ValueError(f"Caminho de página fora do site gerado: {document}")
        if not html_path.is_file():
            raise FileNotFoundError(
                f"HTML da página '{document}' não encontrado em {html_path}. "
                "Confirme se o build do MkDocs terminou com sucesso."
            )
        if html_path not in seen_paths:
            pages.append((title, sections, html_path))
            seen_paths.add(html_path)

    for source_path in sorted(docs_path.rglob("*")):
        if source_path.suffix.lower() not in {".md", ".markdown", ".html"}:
            continue
        relative_document = source_path.relative_to(docs_path).as_posix()
        relative_html = _html_path(relative_document, use_directory_urls)
        if relative_html is None:
            continue
        html_path = (site_path / Path(*relative_html.parts)).resolve()
        if html_path in seen_paths:
            continue
        if not html_path.is_relative_to(site_path):
            raise ValueError(f"Caminho de página fora do site gerado: {relative_document}")
        if not html_path.is_file():
            warnings.warn(
                f"Página de origem não foi incluída no site gerado e será ignorada: "
                f"{relative_document}",
                RuntimeWarning,
                stacklevel=2,
            )
            continue
        sections = tuple(
            part.replace("-", " ").replace("_", " ").title()
            for part in PurePosixPath(relative_document).parts[:-1]
        )
        pages.append((_source_title(source_path), sections, html_path))
        seen_paths.add(html_path)

    if not pages:
        raise ValueError("Nenhuma página Markdown ou HTML foi encontrada em `docs_dir`.")

    canonical_url = base_url or config.get("site_url")
    if canonical_url:
        parsed_url = urlparse(canonical_url)
        if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
            raise ValueError("`base_url` ou `site_url` deve ser uma URL HTTP ou HTTPS completa.")
        canonical_url = canonical_url.rstrip("/") + "/"
    else:
        warnings.warn(
            "Defina `site_url` em mkdocs.yml ou informe `base_url` para que links internos "
            "no PDF apontem ao site publicado.",
            RuntimeWarning,
            stacklevel=2,
        )

    header_template, footer_template = _header_footer_templates(
        _logo_data_uri(site_path, config),
        _image_data_uri(site_path / "assets" / "footer.png"),
    )
    destination = (
        Path(output_pdf).resolve()
        if output_pdf is not None
        else site_path / "assets" / "documentacao-local.pdf"
    )
    destination.parent.mkdir(parents=True, exist_ok=True)

    handler = partial(SimpleHTTPRequestHandler, directory=str(site_path))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    try:
        with tempfile.TemporaryDirectory(prefix="mkdocs-pdf-") as temporary_directory:
            temporary_path = Path(temporary_directory)
            temporary_pdfs: list[Path] = []
            with sync_playwright() as playwright:
                try:
                    browser = playwright.chromium.launch()
                except PlaywrightError as error:
                    raise RuntimeError(
                        "Chromium do Playwright não está instalado. "
                        "Execute `uv run playwright install chromium`."
                    ) from error

                try:
                    page = browser.new_page()
                    origin = f"http://127.0.0.1:{server.server_port}"
                    for index, (_, _, html_path) in enumerate(pages, start=1):
                        relative_html = html_path.relative_to(site_path).as_posix()
                        response = page.goto(
                            f"{origin}/{relative_html}",
                            wait_until="networkidle",
                        )
                        if response is None or response.status >= 400:
                            raise RuntimeError(
                                f"Não foi possível carregar a página HTML: {relative_html}"
                            )
                        page.emulate_media(media="print")
                        page.evaluate(
                            """() => {
                              document.documentElement.setAttribute(
                                "data-md-color-scheme", "default"
                              );
                              if (document.body) {
                                document.body.setAttribute(
                                  "data-md-color-scheme", "default"
                                );
                              }
                            }"""
                        )
                        page.add_style_tag(content=PRINT_STYLES)
                        page.evaluate("() => document.fonts.ready.then(() => true)")
                        _rewrite_internal_links(page, canonical_url)

                        page_pdf = temporary_path / f"pagina-{index:04}.pdf"
                        page.pdf(
                            path=str(page_pdf),
                            print_background=True,
                            prefer_css_page_size=True,
                            display_header_footer=True,
                            header_template=header_template,
                            footer_template=footer_template,
                        )
                        temporary_pdfs.append(page_pdf)
                finally:
                    browser.close()

            writer = PdfWriter()
            section_bookmarks: dict[tuple[str, ...], Any] = {}
            for (title, sections, _), page_pdf in zip(pages, temporary_pdfs):
                first_page = len(writer.pages)
                for pdf_page in PdfReader(page_pdf).pages:
                    writer.add_page(pdf_page)

                parent = None
                for depth in range(1, len(sections) + 1):
                    section_path = sections[:depth]
                    if section_path not in section_bookmarks:
                        section_bookmarks[section_path] = writer.add_outline_item(
                            section_path[-1],
                            first_page,
                            parent=parent,
                        )
                    parent = section_bookmarks[section_path]
                writer.add_outline_item(title, first_page, parent=parent)

            writer.add_metadata({"/Title": "Documentação MkDocs"})
            with destination.open("wb") as pdf_file:
                writer.write(pdf_file)
    finally:
        server.shutdown()
        server.server_close()
        server_thread.join()

    return destination


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Converte as páginas HTML do site MkDocs em um único PDF."
    )
    parser.add_argument("--site-dir", type=Path, default=Path("site"))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--config", type=Path, default=Path("mkdocs.yml"))
    parser.add_argument("--base-url")
    arguments = parser.parse_args()

    output = export_to_pdf(
        site_dir=arguments.site_dir,
        output_pdf=arguments.output,
        mkdocs_config=arguments.config,
        base_url=arguments.base_url,
    )
    print(f"PDF criado: {output}")


if __name__ == "__main__":
    main()
