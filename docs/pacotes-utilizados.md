# Pacotes utilizados

Esta página reúne as dependências Python declaradas diretamente pelo projeto em `pyproject.toml`, explica o papel de cada uma e aponta para suas referências. São os pacotes escolhidos para montar e publicar este site; as dependências indiretas instaladas por eles ficam registradas no `uv.lock`.

As referências são geradas automaticamente em [Referências de pacotes](referencias.md) a cada execução do preview local e antes do build no workflow de publicação do GitHub Actions.

## Dependências do projeto

| Pacote | Uso neste projeto | Referência |
|---|---|---|
| `mkdocs` | Gera o site estático a partir dos arquivos Markdown e do `mkdocs.yml`. | [Documentação do MkDocs](https://www.mkdocs.org/) · [PyPI](https://pypi.org/project/mkdocs/) |
| `mkdocs-material` | Tema Material: layout, navegação, busca, paletas e componentes do site. | [Documentação do Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) · [PyPI](https://pypi.org/project/mkdocs-material/) |
| `mkdocs-awesome-pages-plugin` | Oferece organização automática de páginas e navegação por arquivos `.pages`. | [PyPI](https://pypi.org/project/mkdocs-awesome-pages-plugin/) |
| `mkdocs-exporter` | Exporta páginas do site, inclusive para PDF; usa o navegador via Playwright. | [PyPI](https://pypi.org/project/mkdocs-exporter/) |
| `mkdocs-git-revision-date-localized-plugin` | Exibe datas de criação e de atualização baseadas no histórico Git. | [PyPI](https://pypi.org/project/mkdocs-git-revision-date-localized-plugin/) |
| `mkdocs-glightbox` | Adiciona ampliação de imagens ao clicar nelas. | [PyPI](https://pypi.org/project/mkdocs-glightbox/) |
| `mkdocs-macros-plugin` | Permite usar variáveis, macros e filtros nos arquivos Markdown. | [PyPI](https://pypi.org/project/mkdocs-macros-plugin/) |
| `mkdocs-minify-plugin` | Minifica os arquivos HTML gerados para publicação. | [PyPI](https://pypi.org/project/mkdocs-minify-plugin/) |
| `mkdocstrings[python]` | Gera documentação a partir do código e das docstrings Python; o extra `python` instala o handler Python. | [Documentação do mkdocstrings](https://mkdocstrings.github.io/) · [PyPI](https://pypi.org/project/mkdocstrings/) |
| `mkdocstrings-typescript` | Integra o handler TypeScript com o mkdocstrings. | [PyPI](https://pypi.org/project/mkdocstrings-typescript/) |
| `griffe-typedoc` | Lê a saída JSON do TypeDoc para documentar APIs TypeScript. O projeto fixa uma revisão Git que contém a correção de compatibilidade com `schema_version`. | [Repositório e revisão fixada](https://github.com/mkdocstrings/griffe-typedoc/commit/d0afb31733b2954daed464b5015db6f0e832a21e) |
| `playwright` | Automatiza o navegador Chromium no preview e na exportação de páginas. | [Documentação do Playwright para Python](https://playwright.dev/python/) · [PyPI](https://pypi.org/project/playwright/) |
| `pymdown-extensions` | Fornece extensões Markdown usadas no projeto, como `superfences`, admonitions e blocos de legenda. | [Documentação do PyMdown Extensions](https://facelessuser.github.io/pymdown-extensions/) · [PyPI](https://pypi.org/project/pymdown-extensions/) |

As versões mínimas e a origem Git de `griffe-typedoc` estão especificadas em `pyproject.toml`. O `uv.lock` registra as versões resolvidas para que a instalação do projeto seja reproduzível.

## Instalar as dependências deste projeto

Na raiz do repositório, execute:

```bash
uv sync
```

`uv sync` lê todas as dependências de `pyproject.toml` e usa `uv.lock` para instalar as versões resolvidas, incluindo a revisão Git específica de `griffe-typedoc`. **Não é necessário adicionar os pacotes novamente** quando você está trabalhando neste repositório.

O `uv sync` instala apenas dependências Python. A geração da API TypeScript também precisa do Node.js e do TypeDoc, instalados separadamente pelo workflow do GitHub Actions; o TypeDoc é um pacote JavaScript, não uma biblioteca Python. Consulte a [documentação do TypeDoc](https://typedoc.org/) e o [pacote no npm](https://www.npmjs.com/package/typedoc).

Para criar outro projeto e adicionar o mesmo conjunto de dependências, use `uv add` com as especificações abaixo:

```bash
uv add "mkdocs>=1.6.1" "mkdocs-awesome-pages-plugin>=2.10.1" "mkdocs-exporter>=6.2.0" "mkdocs-git-revision-date-localized-plugin>=1.7.0" "mkdocs-glightbox>=0.5.3" "mkdocs-macros-plugin>=1.5.0" "mkdocs-material>=9.8.1" "mkdocs-minify-plugin>=0.8.0" "mkdocstrings-typescript>=0.1.1" "mkdocstrings[python]>=1.0.8" "playwright>=1.65.0" "pymdown-extensions>=13.0" "griffe-typedoc @ git+https://github.com/mkdocstrings/griffe-typedoc.git@d0afb31733b2954daed464b5015db6f0e832a21e"
```

`uv add` registra os pacotes no projeto atual e atualiza o lockfile. No comando de exemplo, `griffe-typedoc` usa a mesma revisão Git fixada neste repositório, em vez de uma versão diferente do índice de pacotes.

### Instalar o Chromium para Playwright

O pacote Python `playwright` instala a biblioteca de automação, mas o navegador Chromium é um recurso separado. Para gerar previews e PDFs localmente, instale-o uma vez com:

```bash
uv run playwright install chromium
```

No workflow do GitHub Actions, a instalação do navegador e das dependências de sistema é feita pelo próprio workflow.
