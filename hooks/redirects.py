"""hooks/redirects.py — Native_Redirect_Hook.

Gera páginas de redirecionamento HTML (meta refresh) para caminhos antigos
de página, sem depender do pacote `mkdocs-redirects` (nem, por
consequência, do pacote `properdocs`). Referenciado na opção `hooks` do
mkdocs.yml.

Documentação oficial da funcionalidade `hooks` do MkDocs (disponível desde a
versão 1.4, sem exigir nenhum pacote PyPI adicional):
https://www.mkdocs.org/user-guide/configuration/#hooks
"""

import os

# Mapeamento de caminho antigo (relativo a docs_dir) -> caminho atual.
REDIRECTS = {
    "preview.md": "playwright-preview.md",
}


def _write_redirect_html(target_path: str, destination_url: str) -> None:
    """Escreve um arquivo HTML de redirecionamento em `target_path`."""
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    content = (
        "<!DOCTYPE html>\n"
        "<html lang=\"pt-BR\">\n"
        "<head>\n"
        "  <meta charset=\"utf-8\">\n"
        f"  <meta http-equiv=\"refresh\" content=\"0; url={destination_url}\">\n"
        f"  <link rel=\"canonical\" href=\"{destination_url}\">\n"
        "  <title>Redirecionando...</title>\n"
        "</head>\n"
        "<body>\n"
        f"  Redirecionando para <a href=\"{destination_url}\">{destination_url}</a>...\n"
        "</body>\n"
        "</html>\n"
    )
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)


def on_post_build(config, **kwargs):
    """Evento `on_post_build` do MkDocs: gera uma página de
    redirecionamento para cada entrada de REDIRECTS, dentro de
    `config["site_dir"]`."""
    site_dir = config["site_dir"]
    for old_path, new_path in REDIRECTS.items():
        old_slug = old_path.rsplit(".", 1)[0]
        new_slug = new_path.rsplit(".", 1)[0]
        target_html = os.path.join(site_dir, old_slug, "index.html")
        destination_url = f"../{new_slug}/"
        _write_redirect_html(target_html, destination_url)
