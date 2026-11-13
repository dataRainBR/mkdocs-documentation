---
pdf: false
---

# Referências de pacotes Python

Esta página é gerada automaticamente a partir das dependências do projeto.
Para atualizar a lista manualmente, execute `uv run docs_preview.py --generate-references`.

| Pacote | Requisito declarado | Referência |
|---|---|---|
| `griffe-typedoc` | `sem versão mínima` | [Abrir referência](https://github.com/mkdocstrings/griffe-typedoc/commit/d0afb31733b2954daed464b5015db6f0e832a21e) |
| `mkdocs` | `>=1.6.1` | [Abrir referência](https://pypi.org/project/mkdocs/) |
| `mkdocs-awesome-pages-plugin` | `>=2.10.1` | [Abrir referência](https://pypi.org/project/mkdocs-awesome-pages-plugin/) |
| `mkdocs-exporter` | `>=6.2.0` | [Abrir referência](https://pypi.org/project/mkdocs-exporter/) |
| `mkdocs-git-revision-date-localized-plugin` | `>=1.7.0` | [Abrir referência](https://pypi.org/project/mkdocs-git-revision-date-localized-plugin/) |
| `mkdocs-glightbox` | `>=0.5.3` | [Abrir referência](https://pypi.org/project/mkdocs-glightbox/) |
| `mkdocs-macros-plugin` | `>=1.5.0` | [Abrir referência](https://pypi.org/project/mkdocs-macros-plugin/) |
| `mkdocs-material` | `>=9.8.1` | [Abrir referência](https://pypi.org/project/mkdocs-material/) |
| `mkdocs-minify-plugin` | `>=0.8.0` | [Abrir referência](https://pypi.org/project/mkdocs-minify-plugin/) |
| `mkdocstrings-typescript` | `>=0.1.1` | [Abrir referência](https://pypi.org/project/mkdocstrings-typescript/) |
| `mkdocstrings[python]` | `>=1.0.8` | [Abrir referência](https://pypi.org/project/mkdocstrings/) |
| `playwright` | `>=1.65.0` | [Abrir referência](https://pypi.org/project/playwright/) |
| `pymdown-extensions` | `>=13.0` | [Abrir referência](https://pypi.org/project/pymdown-extensions/) |
| `pypdf` | `>=7.0.1` | [Abrir referência](https://pypi.org/project/pypdf/) |
| `pyyaml` | `>=6.0.3` | [Abrir referência](https://pypi.org/project/pyyaml/) |

## Instalar os pacotes

Na raiz do repositório, instale as dependências e as versões registradas no lockfile com:

```bash
uv sync
```

## Função de extração

A função abaixo lê o `pyproject.toml` ou o `requirements.txt` e gera esta página:

::: docs_preview.generate_references_markdown
