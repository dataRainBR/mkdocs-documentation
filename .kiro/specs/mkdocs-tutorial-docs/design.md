# Design Document

## Overview

Este documento descreve o design da documentação MkDocs do projeto `teste-mkdocks`: um `mkdocs.yml` real na raiz do projeto, uma pasta `docs/` com cinco páginas de tutorial em pt-BR mais uma página inicial, e a integração do `mkdocstrings` para documentar automaticamente a função `calcular_media` de `teste.py`. O site é gerado pelos comandos padrão do MkDocs (`mkdocs build` / `mkdocs serve`), executados via `uv run` a partir da raiz do projeto, conforme o roteiro já esboçado em `mkdocks.ipynb`.

O projeto é um ambiente Python gerenciado por `uv` (ver `pyproject.toml`), portanto os exemplos de código/configuração neste design usam Python e YAML.

## Architecture

```
teste_mkdocks/                       (raiz do projeto)
├── mkdocs.yml                       # Mkdocs_Config_File
├── pyproject.toml                   # já existente — dependências mkdocs*
├── teste.py                         # já existente — calcular_media()
├── mkdocks.ipynb                    # já existente — roteiro de referência
├── Dockerfile                        # Dockerfile_Example (multi-estágio, comentado)
├── examples/                         # Multi_Language_Examples
│   ├── exemplo.js                    # JavaScript
│   ├── exemplo.yaml                  # YAML
│   ├── exemplo.tf                    # Terraform (HCL)
│   ├── exemplo.sh                    # Shell
│   └── exemplo.sql                   # SQL
└── docs/                            # Docs_Directory
    ├── index.md                     # página inicial (visão geral + links)
    ├── instalacao.md                # Installation_Page
    ├── configuracao-yaml.md         # Configuration_Page
    ├── personalizacao.md            # Customization_Page
    ├── exemplos-codigo.md           # Code_Examples_Page
    ├── exemplos-notebook.md         # Notebook_Examples_Page
    ├── playwright-preview.md        # Preview_Page
    ├── dockerfile-outras-linguagens.md  # Snippets_Page
    ├── imagens-recursos-visuais.md  # Images_Page
    ├── diagramas-arquitetura.md     # Diagrams_Page
    ├── integracao-github.md         # GitHub_Integration_Page
    ├── extensoes-pymdownx.md        # Pymdown_Extensions_Page
    ├── outros-plugins.md            # Other_Plugins_Page
    ├── assets/                      # logo, favicon, imagens (quando existirem)
    └── javascripts/
        └── mathjax.js                # configuração do MathJax para pymdownx.arithmatex (Mathjax_Frontend_Scripts)
```

**`docs/javascripts/mathjax.js`** — Mathjax_Frontend_Scripts (parte local, Requirement 19.4), configura os delimitadores reconhecidos pelo MathJax para coincidir exatamente com os gerados pela Arithmatex_Extension no modo `generic: true`:

```javascript
window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  }
};
```

Estrutura de arquivos do exemplo TypeScript (Requirement 10), também na raiz do projeto:

```
teste_mkdocks/
├── typedoc.base.json                # Typedoc_Root_Config
├── typedoc.json                     # Typedoc_Root_Config (entryPointStrategy: packages, entryPoints: ["./src/*"])
└── src/
    └── calcular-media/               # TypeScript_Example_Package
        ├── package.json              # name: "calcular-media"
        ├── tsconfig.json              # declaration: true, para gerar src/index.d.ts
        ├── typedoc.json               # entryPointStrategy: expand, entryPoints: ["src/index.d.ts"]
        └── src/
            └── index.ts               # função calcularMedia com JSDoc
```

O `typedoc.json` da raiz do projeto, no modo `entryPointStrategy: "packages"`, descobre cada subpasta listada em `entryPoints: ["./src/*"]` (neste caso, `src/calcular-media/`) e delega a cada uma delas seu próprio `typedoc.json` local (modo `entryPointStrategy: "expand"`, apontando para o `.d.ts` gerado pelo `tsc`). Esse é o mesmo mecanismo de descoberta em dois níveis (raiz → pacote) usado pelo handler `typescript` do mkdocstrings quando ele invoca o TypeDoc_Toolchain internamente.

Fluxo de geração do site:

```
mkdocs.yml (nav + theme + plugins + markdown_extensions)
        │
        ├─ lê cada página listada em `nav` a partir de docs/*.md
        │
        ├─ plugin mkdocstrings (handler python) importa `teste`
        │     a partir da raiz do projeto e resolve `teste.calcular_media`
        │
        └─ mkdocs build  ──►  site/ (HTML estático, tema Material)
                mkdocs serve ──► http://127.0.0.1:8000 (live reload)
```

A raiz do projeto (onde está `teste.py`) **não** é, por padrão, um diretório que o MkDocs/mkdocstrings sabe importar — por padrão o handler Python do mkdocstrings resolve módulos a partir do `cwd` em que `mkdocs` é executado. Como `mkdocs build`/`mkdocs serve` já são executados a partir da raiz do projeto (onde fica `teste.py`), isso normalmente já é suficiente; mesmo assim, o design torna essa resolução **explícita e robusta** adicionando `paths: [.]` em `plugins.mkdocstrings.handlers.python`, conforme Requirement 8.3 (evita falhas caso o comando seja disparado de outro diretório ou via ferramentas que alterem o `cwd`).

## Components and Interfaces

### 1. `mkdocs.yml` (Mkdocs_Config_File)

Componente central de configuração. Estrutura completa:

```yaml
site_name: "Teste MkDocs"
site_description: "Tutorial de MkDocs: instalação, configuração e personalização"
docs_dir: docs

hooks:
  - hooks/redirects.py

repo_url: https://github.com/dataRainBR/mkdocs-documentation   # Real_Repository_URL — substitui o Repository_Placeholder_URL a partir do Requirement 20
repo_name: dataRainBR/mkdocs-documentation
edit_uri: edit/main/docs/

nav:
  - Início: index.md
  - Instalação: instalacao.md
  - "Configuração do mkdocs.yml": configuracao-yaml.md
  - Personalização: personalizacao.md
  - "Exemplos de código": exemplos-codigo.md
  - "Exemplos do notebook": exemplos-notebook.md
  - "Preview com Playwright": playwright-preview.md
  - "Dockerfile e outras linguagens": dockerfile-outras-linguagens.md
  - "Imagens e recursos visuais": imagens-recursos-visuais.md
  - "Diagramas e arquitetura": diagramas-arquitetura.md
  - "Integração com GitHub": integracao-github.md
  - "Extensões pymdownx": extensoes-pymdownx.md
  - "Outros plugins": outros-plugins.md

theme:
  name: material
  logo: assets/logo.png
  favicon: assets/favicon.png
  font:
    text: Roboto
    code: Roboto Mono
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: "Mudar para modo escuro"
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: "Mudar para modo claro"
  features:
    - content.action.edit
    - content.action.view

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          paths: [.]              # resolve `teste` a partir da raiz do projeto
          options:
            show_source: true
            show_root_heading: true
            docstring_style: google
        typescript: {}
  - glightbox
  - git-revision-date-localized:
      fallback_to_build_date: true
      enable_creation_date: true
      type: timeago
  - macros
  - minify:
      minify_html: true
  - awesome-pages
  - exporter:
      formats:
        pdf:
          enabled: true

markdown_extensions:
  - admonition
  - attr_list
  - md_in_html
  - pymdownx.snippets:
      base_path: .
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.inlinehilite
  - pymdownx.blocks.caption
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.tasklist:
      custom_checkbox: true
  - pymdownx.details
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg
  - toc:
      permalink: true
  - abbr
  - def_list
  - footnotes
  - tables
  - pymdownx.mark
  - pymdownx.caret
  - pymdownx.tilde
  - pymdownx.keys
  - pymdownx.critic
  - pymdownx.magiclink
  - pymdownx.smartsymbols
  - pymdownx.arithmatex:
      generic: true

extra_javascript:
  - javascripts/mathjax.js
  - https://unpkg.com/mathjax@3/es5/tex-mml-chtml.js
```

> Nota sobre o Requirement 19 (Reference_Extensions, Text_Formatting_Extensions e Arithmatex_Extension): as extensões nativas do Python-Markdown `abbr`, `def_list`, `footnotes` e `tables` (Reference_Extensions) e as extensões `pymdownx.mark`, `pymdownx.caret`, `pymdownx.tilde`, `pymdownx.keys`, `pymdownx.critic`, `pymdownx.magiclink` e `pymdownx.smartsymbols` (Text_Formatting_Extensions) não exigem nenhuma configuração adicional — todas são habilitadas apenas citando seu nome na lista `markdown_extensions`. Já `pymdownx.arithmatex`, com a opção `generic: true`, apenas prepara o HTML das fórmulas LaTeX (envolvendo-as em `<span>`/`<div>` com a classe `arithmatex`) para que um motor de exibição matemática no navegador as renderize visualmente — sem esse motor, o HTML fica pronto, mas nenhuma fórmula aparece de fato na página. Por isso a opção `extra_javascript`, no nível raiz do `mkdocs.yml` (fora de `markdown_extensions`), referencia os dois Mathjax_Frontend_Scripts: `javascripts/mathjax.js` é um pequeno arquivo JavaScript local (Componente "Arquivos auxiliares de frontend" na seção Architecture, a ser criado em `docs/javascripts/mathjax.js`) que configura o MathJax para reconhecer exatamente a sintaxe gerada pelo `pymdownx.arithmatex` no modo `generic` — delimitadores `\(...\)` para fórmulas em linha e `\[...\]` para fórmulas em bloco — e o segundo item (`https://unpkg.com/mathjax@3/es5/tex-mml-chtml.js`) carrega a própria biblioteca MathJax 3 via CDN, responsável por ler esse HTML preparado e renderizar as fórmulas no navegador do leitor.

> Nota sobre os Requirements 12–16 e 18 (Ecosystem_Pages e Exporter_Plugin): os blocos `repo_url`/`repo_name`/`edit_uri`, `theme.features`, a opção `hooks` (Native_Redirect_Hook), e os novos plugins (`glightbox`, `git-revision-date-localized`, `macros`, `minify`, `awesome-pages`, `exporter`) e extensões (`attr_list`, `md_in_html`, `pymdownx.blocks.caption`, `pymdownx.tabbed`, `pymdownx.tasklist`, `pymdownx.details`, `pymdownx.emoji`, e o `custom_fences` do `pymdownx.superfences`) acima são explicados em detalhe, um a um, nos Componentes 11 a 15 abaixo — cada um na página do tutorial correspondente. Todos os pacotes Python desses plugins (`mkdocs-glightbox`, `mkdocs-git-revision-date-localized-plugin`, `mkdocs-macros-plugin`, `mkdocs-minify-plugin`, `mkdocs-awesome-pages-plugin`, `mkdocs-exporter`) devem ser declarados no Project_Manifest (`pyproject.toml`) via `uv add`, conforme Requirement 17.3 (e Requirement 18.1 para o Exporter_Plugin especificamente). Já o Native_Redirect_Hook **não** é um pacote do PyPI: é um script Python local (`hooks/redirects.py`), referenciado apenas pela opção `hooks` do Mkdocs_Config_File, sem nenhuma entrada correspondente no Project_Manifest.

> Nota sobre `pymdownx.snippets` (Requirement 11.9–11.13): a extensão `pymdownx.snippets` é fornecida pelo pacote Python `pymdown-extensions` (Pymdown_Extensions_Package), adicionado ao Project_Manifest (`pyproject.toml`) através de `uv add pymdown-extensions`. A opção `base_path: .` faz com que todo caminho usado na sintaxe `--8<-- "caminho/arquivo"` (ver Componente 10 abaixo) seja resolvido a partir da raiz do projeto — o mesmo diretório em que `mkdocs build`/`mkdocs serve` são executados — sem exigir configuração adicional por página. As extensões `admonition`, `pymdownx.superfences`, `pymdownx.inlinehilite` e `toc` (com `permalink: true`) já presentes anteriormente são mantidas sem alteração de comportamento; apenas `pymdownx.highlight` passa a ser configurada explicitamente com `anchor_linenums: true`, `line_spans: __span` e `pygments_lang_class: true`, opções recomendadas pela documentação do tema Material para compatibilidade com `pymdownx.superfences` e `pymdownx.snippets`.

> Nota sobre `handlers.typescript` (Requirement 10.5): a opção `paths`, usada pelo handler `python`, não é uma opção documentada do handler `typescript` do mkdocstrings — esse handler descobre seus pacotes a partir dos arquivos `typedoc.json`/`typedoc.base.json` na raiz do projeto (ver seção "Architecture" e o Componente 9 abaixo), não a partir de uma lista de `paths` do MkDocs. A configuração correta do handler é `typescript: {}` (sem opções obrigatórias para este exemplo), substituindo a configuração anterior `typescript: paths: [.]`, que era inválida.

> Nota sobre `repo_url`/`repo_name`/`edit_uri` (Requirement 20.2–20.3): a partir do Requirement 20, esses três campos passam a conter o Real_Repository_URL (`https://github.com/dataRainBR/mkdocs-documentation`, branch `main`, confirmada pelo usuário), substituindo o Repository_Placeholder_URL (`https://github.com/seu-usuario/teste-mkdocks`) usado até o Requirement 14. `edit_uri` permanece `edit/main/docs/`, agora apontando de fato para a branch `main` do repositório real em vez de uma branch hipotética de um repositório de exemplo. As duas variantes de `theme.palette` (`media: "(prefers-color-scheme: light)"` e `media: "(prefers-color-scheme: dark)"`) já definidas acima permanecem inalteradas (Requirement 20.2) — ver Componente 5 para a explicação detalhada dos modos claro/escuro.

Mapeamento requisito → chave de configuração:

| Requisito | Chave em `mkdocs.yml` |
|---|---|
| 2.2 tema material | `theme.name: material` |
| 2.3 nav na ordem correta | `nav` (6 entradas, ordem fixa) |
| 2.4 / 2.5 mkdocstrings python + typescript | `plugins.mkdocstrings.handlers.python` / `.typescript` |
| 2.6 highlight de código | `markdown_extensions: [pymdownx.highlight, pymdownx.superfences, ...]` |
| 2.7 docs_dir | `docs_dir: docs` (explícito, embora seja o padrão do MkDocs) |
| 2.8 paleta de cores | `theme.palette` (variantes light/dark) |
| 2.9 logo em `docs/assets/` | `theme.logo: assets/logo.png` |
| 8.3 resolução do módulo `teste` | `plugins.mkdocstrings.handlers.python.paths: [.]` |
| 9.4 mkdocstrings para o módulo `docs_preview` | `plugins.mkdocstrings.handlers.python.paths: [.]` (mesma chave do Requirement 8.3 — já suficiente, ver nota abaixo) |
| 9.7 Preview_Page acessível via nav | `nav` (7ª entrada: `"Preview com Playwright": playwright-preview.md`) |
| 10.5 handler `typescript` sem `paths` | `plugins.mkdocstrings.handlers.typescript: {}` |
| 10.4 descoberta do TypeScript_Example_Package | `typedoc.json` / `typedoc.base.json` na raiz do projeto (fora do `mkdocs.yml`, mas consumidos indiretamente pelo handler `typescript`) |
| 11.9 Pymdown_Extensions_Package como dependência | `pyproject.toml` → `uv add pymdown-extensions` (fora do `mkdocs.yml`, mas pré-requisito para `pymdownx.snippets`) |
| 11.10 `pymdownx.snippets` com `base_path: .` | `markdown_extensions: pymdownx.snippets.base_path: .` |
| 11.11 `pymdownx.superfences` (blocos de incorporação) | `markdown_extensions: [pymdownx.superfences]` (já existente, reafirmado pelo Requirement 11) |
| 11.12 `pymdownx.highlight` com `anchor_linenums`/`line_spans`/`pygments_lang_class` | `markdown_extensions: pymdownx.highlight: {anchor_linenums: true, line_spans: __span, pygments_lang_class: true}` |
| 11.13 manter `admonition`, `pymdownx.inlinehilite`, `toc.permalink` | `markdown_extensions: [admonition, pymdownx.inlinehilite, toc: {permalink: true}]` (inalterados) |
| 11.14 Snippets_Page acessível via nav | `nav` (8ª entrada: `"Dockerfile e outras linguagens": dockerfile-outras-linguagens.md`) |
| 12.1 / 12.2 Glightbox_Plugin | `plugins: [glightbox]` (pacote `mkdocs-glightbox` declarado no Project_Manifest) |
| 12.5 / 12.6 `attr_list`, `md_in_html`, `pymdownx.blocks.caption` | `markdown_extensions: [attr_list, md_in_html, pymdownx.blocks.caption]` |
| 13.1 `custom_fences` do mermaid | `markdown_extensions: pymdownx.superfences.custom_fences` (`name: mermaid`, `class: mermaid`, `format: !!python/name:pymdownx.superfences.fence_code_format`) |
| 14.1 `repo_url` / `repo_name` / `edit_uri` (Repository_Placeholder_URL, substituído pelo Requirement 20.3) | `repo_url`, `repo_name`, `edit_uri` (nível raiz do `mkdocs.yml`) |
| 14.2 ações de edição/visualização de página | `theme.features: [content.action.edit, content.action.view]` |
| 14.4 Git_Revision_Date_Plugin | `plugins: git-revision-date-localized: {fallback_to_build_date: true, enable_creation_date: true, type: timeago}` (pacote `mkdocs-git-revision-date-localized-plugin`) |
| 15.2 `pymdownx.tabbed` | `markdown_extensions: pymdownx.tabbed: {alternate_style: true}` |
| 15.3 `pymdownx.tasklist` / `pymdownx.details` / `pymdownx.emoji` | `markdown_extensions: [pymdownx.tasklist: {custom_checkbox: true}, pymdownx.details, pymdownx.emoji]` |
| 16.2 Macros_Plugin | `plugins: [macros]` (pacote `mkdocs-macros-plugin`) |
| 16.4 opção `hooks` (Native_Redirect_Hook) | `hooks: [hooks/redirects.py]` (script local, sem pacote PyPI) |
| 16.7 Minify_Plugin | `plugins: minify: {minify_html: true}` (pacote `mkdocs-minify-plugin`) |
| 16.9 Awesome_Pages_Plugin | `plugins: [awesome-pages]` (pacote `mkdocs-awesome-pages-plugin`) |
| 17.2 nav com as Ecosystem_Pages | `nav` (5 novas entradas, após `"Dockerfile e outras linguagens"`) |
| 18.2 Exporter_Plugin | `plugins.exporter.formats.pdf.enabled: true` (pacote `mkdocs-exporter`) |
| 19.1 Reference_Extensions | `markdown_extensions: [abbr, def_list, footnotes, tables]` |
| 19.2 Text_Formatting_Extensions | `markdown_extensions: [pymdownx.mark, pymdownx.caret, pymdownx.tilde, pymdownx.keys, pymdownx.critic, pymdownx.magiclink, pymdownx.smartsymbols]` |
| 19.3 Arithmatex_Extension | `markdown_extensions: pymdownx.arithmatex: {generic: true}` |
| 19.4 Mathjax_Frontend_Scripts | `extra_javascript: [javascripts/mathjax.js, https://unpkg.com/mathjax@3/es5/tex-mml-chtml.js]` (nível raiz do `mkdocs.yml`) |
| 20.1 seção "Modos claro e escuro" na Customization_Page | nenhuma chave nova — reafirma `theme.palette` (ver Componente 5) |
| 20.3 `repo_url` / `repo_name` / `edit_uri` com valores reais | `repo_url`, `repo_name`, `edit_uri` (nível raiz do `mkdocs.yml`, com o Real_Repository_URL) |
| 20.4 / 20.5 / 20.6 / 20.7 / 20.8 / 20.9 GitHub_Actions_Workflow | `.github/workflows/docs.yml` (fora do `mkdocs.yml`, ver Componente 16) |

> Nota sobre o Requirement 9.4: o módulo `docs_preview` (arquivo `docs_preview.py`) está na raiz do projeto, no mesmo diretório que `teste.py`. Como `plugins.mkdocstrings.handlers.python.paths: [.]` já configurado para resolver `teste` (Requirement 8.3) aponta para a raiz do projeto, essa mesma configuração já é suficiente para resolver `docs_preview` também. Nenhuma chave adicional precisa ser criada no `mkdocs.yml` para a Preview_Page — apenas a nova entrada em `nav` listada acima.

> Nota sobre `favicon`: o requisito 5.6 permite que, não havendo um arquivo de imagem binário real no projeto, a ausência seja apenas documentada textualmente em `personalizacao.md` (em vez de a tarefa de implementação ser bloqueada pela criação de um PNG). O campo `theme.favicon`/`theme.logo` no YAML referencia o caminho esperado (`assets/logo.png`, `assets/favicon.png`); se os arquivos não existirem fisicamente, o build do MkDocs ainda funciona (ele apenas usa os ícones padrão do Material quando o arquivo referenciado não é encontrado) — esse comportamento é exatamente o que a Customization_Page explica.

### 2. `docs/index.md` — página inicial

Seções:
- Título e parágrafo de abertura explicando o propósito do tutorial.
- Lista de links (Markdown) para as 5 Tutorial_Pages, na mesma ordem do `nav`.

### 3. `docs/instalacao.md` — Installation_Page

Seções:
1. Introdução (o que será instalado e por quê).
2. Instalação dos pacotes com `uv` (comando real do projeto):
   ```bash
   uv add mkdocs mkdocs-material "mkdocstrings[python]" mkdocstrings-typescript
   ```
3. Explicação individual de cada pacote: `mkdocs`, `mkdocs-material`, `mkdocstrings[python]`, `mkdocstrings-typescript`.
4. Alternativa com `pip` (nota informativa, não obrigatória pelos requisitos).

### 4. `docs/configuracao-yaml.md` — Configuration_Page

Seções, uma por chave de configuração (Requirements 4.1–4.4):
1. `nav` — define a estrutura de navegação/menu do site.
2. `theme` — define o tema visual (Material), fontes e paleta.
3. `plugins` — habilita funcionalidades como busca (`search`) e geração de documentação a partir de código (`mkdocstrings`, com os handlers `python` e `typescript`).
4. `markdown_extensions` — habilita recursos de renderização Markdown (admonitions, blocos de código com destaque de sintaxe, sumário/`toc`).

Cada seção mostra o trecho de YAML correspondente (reaproveitado do `mkdocs.yml` real do projeto) e uma explicação em prosa.

### 5. `docs/personalizacao.md` — Customization_Page

Seções (Requirements 5.1–5.6):
1. Fontes (`theme.font.text` / `theme.font.code`).
2. Paleta de cores (`theme.palette`, variantes claro/escuro, `primary`/`accent`).
3. **Modos claro e escuro** (Requirement 20.1–20.2) — seção dedicada que detalha o mesmo bloco `theme.palette` já apresentado no item anterior e no Componente 1:
   ```yaml
   theme:
     palette:
       - media: "(prefers-color-scheme: light)"
         scheme: default
         primary: indigo
         accent: indigo
         toggle:
           icon: material/brightness-7
           name: "Mudar para modo escuro"
       - media: "(prefers-color-scheme: dark)"
         scheme: slate
         primary: indigo
         accent: indigo
         toggle:
           icon: material/brightness-4
           name: "Mudar para modo claro"
   ```
   A seção explica, em prosa, os três aspectos exigidos pelo Requirement 20.1:
   - **Detecção automática (`media: "(prefers-color-scheme: light|dark)"`)**: cada entrada da lista `theme.palette` é associada a uma media query CSS padrão do navegador, que reflete a preferência de tema configurada no sistema operacional do visitante (claro ou escuro). Na primeira visita — antes de qualquer interação —, o tema Material já consulta essa preferência do sistema operacional e renderiza o site automaticamente no modo correspondente, sem exigir nenhum clique do visitante.
   - **Botão de alternância manual (`toggle.icon` / `toggle.name`)**: cada variante de `palette` define um `toggle` (um ícone e um texto exibidos como tooltip) que aparece como um botão no cabeçalho do site. Clicar nesse botão alterna manualmente para a outra variante de `palette` — permitindo ao visitante trocar de modo mesmo que o sistema operacional já tenha indicado uma preferência diferente da desejada naquele momento.
   - **Persistência da escolha entre visitas**: quando o visitante usa o botão de alternância manual, o tema Material grava essa escolha no `localStorage` do navegador. Em visitas futuras, o site passa a ler esse valor salvo e abrir diretamente no modo escolhido anteriormente, em vez de voltar a detectar a preferência via `prefers-color-scheme` a cada carregamento de página — até que o `localStorage` seja limpo (ex.: pelo visitante, ou ao trocar de navegador/dispositivo), momento em que a detecção automática por `prefers-color-scheme` volta a valer como ponto de partida.
4. Logo (`theme.logo`) — convenção de armazenar em `docs/assets/`.
5. Favicon (`theme.favicon`) — mesma convenção.
6. Observação explícita: como o projeto não possui, hoje, um arquivo de imagem binário real, a página indica essa ausência em texto (ex.: "este projeto ainda não possui um arquivo de logo/favicon; ao adicionar um, salve-o em `docs/assets/` e aponte `theme.logo`/`theme.favicon` para ele"), sem exigir a criação de um PNG/ICO como parte desta funcionalidade.

### 6. `docs/exemplos-codigo.md` — Code_Examples_Page

Seções (Requirements 6.1–6.4):
1. **Bloco de código estático** — mostra o código-fonte de `calcular_media` dentro de um bloco ```` ```python ```` copiado de `teste.py`:
   ```python
   def calcular_media(valores: list[float]) -> float:
       """
       Calcula a média de uma lista de valores.

       Args:
           valores: Lista de valores numéricos.

       Returns:
           Média aritmética dos valores.

       Raises:
           ValueError: Se a lista estiver vazia.
       """
       if not valores:
           raise ValueError("A lista não pode estar vazia.")

       return sum(valores) / len(valores)
   ```
2. **Documentação via mkdocstrings** — usa a diretiva do plugin para renderizar a docstring diretamente a partir do código-fonte:
   ```markdown
   ::: teste.calcular_media
   ```
3. **Bloco estático vs. mkdocstrings** — explica que o bloco de código é texto fixo (precisa ser atualizado manualmente se `teste.py` mudar), enquanto a diretiva `::: teste.calcular_media` é gerada dinamicamente a cada build a partir do código real, garantindo que a documentação nunca fique desatualizada.
4. **Exemplo em TypeScript** (Requirements 10.6–10.10) — na mesma página, após o exemplo em Python:
   - **Bloco de código estático**, idêntico ao `src/calcular-media/src/index.ts` real (Componente 9):
     ```typescript
     /**
      * Calcula a média de uma lista de valores.
      *
      * @param valores - Lista de valores numéricos.
      * @returns Média aritmética dos valores.
      * @throws {Error} Se a lista estiver vazia.
      */
     export function calcularMedia(valores: number[]): number {
       if (valores.length === 0) {
         throw new Error("A lista não pode estar vazia.");
       }

       return valores.reduce((soma, valor) => soma + valor, 0) / valores.length;
     }
     ```
   - **Documentação via mkdocstrings com o handler `typescript`** — a página explica a sintaxe da diretiva (o identificador referencia o pacote TypeScript_Example_Package, e o handler é selecionado explicitamente por não ser o handler padrão do Mkdocstrings_Plugin) e também a insere de fato na página:
     ```markdown
     ::: calcular-media
         handler: typescript
     ```
   - **Bloco estático vs. mkdocstrings (TypeScript)** — explicação análoga à do Python (item 3 acima): o bloco de código acima é texto fixo, enquanto a diretiva `::: calcular-media` com `handler: typescript` é gerada a cada build a partir do `.d.ts` real produzido pelo `tsc`, através do TypeDoc_Toolchain.
   - **Passos de instalação e build do TypeDoc_Toolchain** (Requirement 10.9) — a página descreve, em prosa, os mesmos três passos documentados no Componente 9 (`npm install`/instalação do TypeDoc, geração do `.d.ts` via `tsc`, e build do site), como pré-requisito para que a diretiva `::: calcular-media` funcione.
   - **Observação sobre ausência do Node.js no ambiente original** (Requirement 10.10) — a página registra explicitamente que, no ambiente em que esta spec foi originalmente construída, Node.js/npm não estavam instalados; portanto a diretiva `::: calcular-media` com `handler: typescript` especificamente não pôde ser validada por um `uv run mkdocs build` real nesta máquina (diferentemente da diretiva `::: teste.calcular_media`, que usa o handler `python` e foi validada normalmente). O leitor deve instalar Node.js, executar os passos de toolchain acima e validar essa diretiva em seu próprio ambiente.

### 7. `docs/exemplos-notebook.md` — Notebook_Examples_Page

Reflete, em texto explicativo próprio (não é uma cópia do notebook), o roteiro de `mkdocks.ipynb`. Cada etapa do notebook se torna uma seção com o comando real equivalente (Requirements 7.1–7.2):

| Seção do notebook | Etapa na página | Comando |
|---|---|---|
| "Instalando Mkdocks" | 1. Instalação dos pacotes | `uv add mkdocs mkdocs-material "mkdocstrings[python]" mkdocstrings-typescript` |
| "Inicializando um novo projeto" | 2. Inicialização do projeto | `uv run mkdocs new .` |
| "fazendo o build" | 3. Build do site | `uv run mkdocs build` |
| "executando o mkdocs para visualizar a documentação html" | 4. Visualização local | `uv run mkdocs serve` (abre em `http://127.0.0.1:8000`) |
| "Configurando o Yaml" | 5. Configuração do `mkdocs.yml` | edição manual de `nav`, `theme`, `plugins`, `markdown_extensions` |
| "Personalizações" | 6. Personalização visual | edição de `theme.font`, `theme.palette`, `theme.logo`, `theme.favicon` |

A página apresenta essas 6 etapas em ordem sequencial (instalação → init → build → visualização → configuração → personalização), cada uma com uma breve explicação em prosa e o comando de terminal correspondente, quando aplicável.

### 8. `docs/playwright-preview.md` — Preview_Page

Seções (Requirements 9.1–9.6):

1. **Instalação do Playwright**:
   ```bash
   uv add playwright
   uv run playwright install chromium
   ```
   A página explica que os dois comandos são necessários em sequência: `uv add playwright` adiciona o pacote Python `playwright` às dependências do projeto (biblioteca cliente), mas o pacote Python por si só **não** inclui os binários dos navegadores. `uv run playwright install chromium` baixa separadamente o executável do Chromium para o cache local do Playwright — sem esse segundo passo, qualquer chamada que tente abrir um navegador (ex.: `playwright.chromium.launch(...)`) falha por não encontrar o binário instalado.

2. **O que é o Playwright e por que é usado aqui**: explica que o Playwright é uma biblioteca de automação de navegador (permite abrir, controlar e inspecionar páginas web via código, originalmente criada para testes end-to-end). Nesta funcionalidade ele não é usado para testes automatizados, e sim pelo Preview_Script (`docs_preview.py`) como forma prática de abrir o Documentation_Site já buildado (`site/index.html`, servido localmente via `http.server`) em uma janela de Chromium controlada por código, em vez de depender do navegador padrão do sistema operacional — o que dá ao script controle total sobre quando a janela abre e quando/como ela é fechada (`input()` aguardando o usuário apertar Enter).

3. **Documentação das funções via mkdocstrings**: a página usa a diretiva de módulo inteiro, documentando todas as funções públicas de `docs_preview` de uma só vez:
   ```markdown
   ::: docs_preview
   ```
   Justificativa da escolha: o Requirement 9.4 exige a documentação de **todas** as seis funções do Preview_Script (`run_mkdocs_build`, `find_free_port`, `start_local_server`, `ensure_playwright_browser_installed`, `open_in_browser` e `main`). Usar a diretiva de módulo inteiro (`::: docs_preview`) é mais simples de manter do que listar seis diretivas individuais (`::: docs_preview.run_mkdocs_build`, `::: docs_preview.find_free_port`, etc.) — se uma nova função for adicionada ao script no futuro, ela aparece automaticamente na página sem exigir edição do Markdown. Como `docs_preview.py` não expõe nenhuma função além dessas seis (não há API "privada" a esconder), não há vantagem em documentá-las uma a uma; a abordagem de módulo inteiro cobre o requisito com uma única diretiva.

4. **Como usar o script**:
   ```bash
   uv run docs_preview.py
   ```
   A página explica que `docs_preview.py` é um "script uv" autocontido (possui metadados PEP 723 no cabeçalho do arquivo declarando `playwright` como dependência), então `uv run docs_preview.py` cria um ambiente efêmero com o Playwright já instalado e executa o script diretamente, sem exigir um `uv add`/`pip install` manual prévio dentro do ambiente principal do projeto para essa execução pontual.

### Observação sobre resolução do módulo `docs_preview`

O módulo `docs_preview` está na raiz do projeto (`docs_preview.py`), no mesmo diretório que `teste.py`. A configuração `plugins.mkdocstrings.handlers.python.paths: [.]`, já presente no `mkdocs.yml` para resolver `teste` (Requirement 8.3), referencia a raiz do projeto como caminho de busca do handler Python — portanto ela já é suficiente para resolver `docs_preview` também, sem necessidade de nenhuma chave adicional em `mkdocs.yml` além da nova entrada em `nav` (Requirement 9.7).

### 9. Pacote TypeScript de exemplo (`src/calcular-media/`) e configuração do TypeDoc

Componente que espelha, em TypeScript, o exemplo Python de `teste.calcular_media` (Componente 6), para que o Code_Examples_Page demonstre o handler `typescript` do Mkdocstrings_Plugin com um pacote real (Requirements 10.1–10.4).

**`src/calcular-media/src/index.ts`** — equivalente da docstring Google de `calcular_media`, agora como JSDoc:

```typescript
/**
 * Calcula a média de uma lista de valores.
 *
 * @param valores - Lista de valores numéricos.
 * @returns Média aritmética dos valores.
 * @throws {Error} Se a lista estiver vazia.
 */
export function calcularMedia(valores: number[]): number {
  if (valores.length === 0) {
    throw new Error("A lista não pode estar vazia.");
  }

  return valores.reduce((soma, valor) => soma + valor, 0) / valores.length;
}
```

**`src/calcular-media/package.json`**:

```json
{
  "name": "calcular-media",
  "version": "1.0.0",
  "types": "src/index.d.ts"
}
```

**`src/calcular-media/tsconfig.json`** — `declaration: true` gera `src/index.d.ts` ao lado de `src/index.ts`; `emitDeclarationOnly` evita que `tsc` também gere `.js` (não necessário aqui, já que o arquivo não é executado, apenas documentado):

IMPORTANTE: `outDir`/`rootDir` NAO devem apontar para a mesma pasta de `include` - o `tsc` exclui automaticamente o `outDir` da compilacao (para evitar recompilar seus proprios arquivos emitidos), e se `outDir` coincidir com a pasta de origem, isso zera os arquivos de entrada (`TS18003: No inputs were found`), erro real encontrado na primeira execucao do workflow de GitHub Actions. Por isso nem `outDir` nem `rootDir` sao definidos aqui - sem `outDir`, o `tsc` emite o `.d.ts` ao lado do `.ts` de origem por padrao:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "declaration": true,
    "emitDeclarationOnly": true,
    "strict": true
  },
  "include": ["src/**/*.ts"]
}
```

**`src/calcular-media/typedoc.json`** — modo `expand`, aponta diretamente para a declaração gerada por `tsc`:

```json
{
  "extends": ["../../typedoc.base.json"],
  "entryPointStrategy": "expand",
  "entryPoints": ["src/index.d.ts"]
}
```

**`typedoc.base.json`** (raiz do projeto) — opções compartilhadas por todos os pacotes descobertos:

```json
{
  "excludeExternals": true,
  "readme": "none"
}
```

**`typedoc.json`** (raiz do projeto) — modo `packages`, descobre cada pasta dentro de `src/`:

```json
{
  "extends": ["./typedoc.base.json"],
  "entryPointStrategy": "packages",
  "entryPoints": ["./src/*"]
}
```

**Toolchain necessária (Requirement 10.9)** — os comandos abaixo **não são executáveis no ambiente atual desta spec**, pois Node.js/npm não estão instalados nesta máquina (ver Error Handling e Testing Strategy abaixo); eles são documentados para quem reproduzir o exemplo em um ambiente com Node.js:

```bash
# 1. Inicializar/instalar dependências de desenvolvimento do pacote de exemplo
npm init -y                                   # ou criação manual do package.json acima
npm install --save-dev typescript typedoc

# 2. Gerar src/index.d.ts a partir de src/index.ts (usa src/calcular-media/tsconfig.json)
npx tsc

# 3. Build do site — o handler `typescript` do mkdocstrings invoca o TypeDoc
#    internamente a partir do typedoc.json da raiz do projeto
uv run mkdocs build
```

### 10. Dockerfile de exemplo, exemplos multi-linguagem e `docs/dockerfile-outras-linguagens.md` — Snippets_Page

Componente que demonstra, para Dockerfile e para linguagens sem handler do Mkdocstrings_Plugin (JavaScript, YAML, Terraform, Shell, SQL), uma alternativa à documentação estruturada via docstring: a incorporação do conteúdo bruto de arquivos reais do projeto em uma página Markdown, através da extensão `pymdownx.snippets` (Requirements 11.1–11.20).

**`Dockerfile`** (raiz do projeto) — Dockerfile_Example, multi-estágio (`builder`/`runtime`), comentado instrução a instrução, adaptado a este projeto real Python/uv. O projeto não possui um pacote `src/` de aplicação (a pasta `src/` existente é o TypeScript_Example_Package do Requirement 10, não a aplicação), então o entrypoint referencia `main.py` diretamente, em vez de `python -m src`:

```dockerfile
# ---------------------------------------------------------------------------
# Estágio 1: builder — instala as dependências do projeto em um ambiente
# isolado, usando o gerenciador uv e os arquivos de lock já existentes
# (pyproject.toml / uv.lock), antes de copiar o código-fonte da aplicação.
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS builder
# Copia o binário oficial do uv (já compilado) para dentro da imagem, em vez
# de instalá-lo via pip, mantendo o estágio de build mais rápido e leve.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
# Define o diretório de trabalho onde o projeto será montado dentro da imagem.
WORKDIR /app
# Copia primeiro apenas os arquivos de manifesto de dependências, para que o
# cache de camadas do Docker seja reaproveitado quando só o código mudar.
COPY pyproject.toml uv.lock ./
# Instala exatamente as dependências travadas em uv.lock (--frozen), sem os
# grupos de desenvolvimento (--no-dev), mantendo o ambiente final mínimo.
RUN uv sync --frozen --no-dev
# Copia o código-fonte real da aplicação (main.py) e do exemplo documentado
# via mkdocstrings (teste.py) para dentro da imagem builder.
COPY main.py teste.py ./

# ---------------------------------------------------------------------------
# Estágio 2: runtime — imagem final, menor, contendo apenas o ambiente
# virtual já resolvido pelo uv e o código necessário para executar a
# aplicação, sem as ferramentas de build usadas no estágio anterior.
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS runtime
# Define o mesmo diretório de trabalho usado no estágio builder.
WORKDIR /app
# Copia o ambiente virtual já criado pelo uv no estágio builder, evitando
# reinstalar dependências e reduzindo o tamanho e o tempo de build da imagem
# final.
COPY --from=builder /app/.venv /app/.venv
# Copia o código-fonte já validado no estágio builder.
COPY --from=builder /app/main.py /app/teste.py ./
# Adiciona o ambiente virtual ao PATH, para que o comando `python` resolva
# para o interpretador e os pacotes instalados pelo uv, sem precisar ativar
# manualmente o ambiente virtual.
ENV PATH="/app/.venv/bin:$PATH"
# Define o comando padrão executado quando o container é iniciado. Este
# projeto não possui um pacote `src/` de aplicação (a pasta `src/`
# existente é o TypeScript_Example_Package do Requirement 10, não a
# aplicação), então o entrypoint real é o script `main.py` na raiz do
# projeto, em vez de `python -m src`.
CMD ["python", "main.py"]
```

**Multi_Language_Examples** (`examples/`) — cinco arquivos pequenos e didáticos, cada um comentado, um por linguagem sem handler de Mkdocstrings_Plugin:

- **`examples/exemplo.js`** — função JavaScript simples, equivalente conceitual a `calcularMedia`:
  ```javascript
  // exemplo.js — função simples em JavaScript, incorporada na Snippets_Page
  // via pymdownx.snippets (não existe handler de mkdocstrings para JS puro).

  // Calcula a média aritmética de uma lista de números.
  function calcularMedia(valores) {
    if (valores.length === 0) {
      throw new Error("A lista não pode estar vazia.");
    }
    return valores.reduce((soma, valor) => soma + valor, 0) / valores.length;
  }

  module.exports = { calcularMedia };
  ```
- **`examples/exemplo.yaml`** — configuração simples:
  ```yaml
  # exemplo.yaml — configuração simples incorporada na Snippets_Page.
  app:
    name: teste-mkdocks
    version: "1.0.0"
    logging:
      level: info
      format: json
  ```
- **`examples/exemplo.tf`** — recurso Terraform simples:
  ```hcl
  # exemplo.tf — recurso Terraform simples incorporado na Snippets_Page.
  resource "local_file" "exemplo" {
    filename = "${path.module}/exemplo-output.txt"
    content  = "Gerado pelo exemplo Terraform da documentação."
  }
  ```
- **`examples/exemplo.sh`** — script de build/deploy simples:
  ```bash
  #!/usr/bin/env bash
  # exemplo.sh — script simples de build/deploy incorporado na Snippets_Page.
  set -euo pipefail

  echo "Construindo a imagem Docker..."
  docker build -t teste-mkdocks:latest .

  echo "Publicando a imagem no registry..."
  docker push teste-mkdocks:latest
  ```
- **`examples/exemplo.sql`** — criação de tabela e consulta simples:
  ```sql
  -- exemplo.sql — criação de tabela e consulta simples incorporada na
  -- Snippets_Page.
  CREATE TABLE medias (
      id SERIAL PRIMARY KEY,
      valor NUMERIC NOT NULL
  );

  SELECT AVG(valor) AS media
  FROM medias;
  ```

**`docs/dockerfile-outras-linguagens.md`** — Snippets_Page. Estrutura da página (Requirements 11.15–11.20):

1. **Introdução — por que não há handler de mkdocstrings para estas linguagens**: explica que o Mkdocstrings_Plugin depende de um handler por linguagem capaz de extrair uma "docstring" estruturada do código-fonte (como o handler `python` faz com docstrings Google, ou o handler `typescript` com JSDoc via TypeDoc_Toolchain). Dockerfile, JavaScript puro (sem um toolchain de documentação configurado), YAML, Terraform, Shell e SQL não possuem um handler oficial equivalente disponível para este projeto — não existe um parser de comentário/"docstring" estruturado e amplamente padronizado para essas linguagens integrado ao Mkdocstrings_Plugin. Por isso, a alternativa adotada é incorporar o conteúdo real do arquivo diretamente na página, em vez de reescrevê-lo manualmente.
2. **Hadolint e Docker Buildx como complementos de qualidade**: menciona, de forma conceitual, que o Hadolint (linter de Dockerfile) e o Docker Buildx (motor de build estendido do Docker, com suporte a multi-estágio e múltiplas plataformas) são práticas complementares recomendadas para lint e validação de build do Dockerfile_Example, sem exigir que essas ferramentas estejam instaladas ou sejam executadas neste ambiente — a página apenas as cita como próximos passos recomendados para quem for usar o Dockerfile_Example em um pipeline real.
3. **Sintaxe de incorporação `--8<--`**: explica que a extensão `pymdownx.snippets`, configurada com `base_path: .` (ver Componente 1), permite incorporar o conteúdo bruto de um arquivo dentro de um bloco de código Markdown através da linha `--8<-- "caminho/arquivo"`, colocada dentro de um bloco cercado (` ``` `) com a linguagem apropriada para destaque de sintaxe — por exemplo:
   ````markdown
   ```dockerfile
   --8<-- "Dockerfile"
   ```
   ````
   O caminho informado é resolvido a partir da raiz do projeto (onde `mkdocs build`/`mkdocs serve` são executados), graças a `base_path: .`.
4. **Uma subseção por arquivo**, cada uma com o bloco de incorporação real inserido na página:
   - **Dockerfile** — bloco com linguagem `dockerfile`:
     ````markdown
     ```dockerfile
     --8<-- "Dockerfile"
     ```
     ````
   - **`examples/exemplo.js`** — bloco com linguagem `javascript`:
     ````markdown
     ```javascript
     --8<-- "examples/exemplo.js"
     ```
     ````
   - **`examples/exemplo.yaml`** — bloco com linguagem `yaml`:
     ````markdown
     ```yaml
     --8<-- "examples/exemplo.yaml"
     ```
     ````
   - **`examples/exemplo.tf`** — bloco com linguagem `hcl`:
     ````markdown
     ```hcl
     --8<-- "examples/exemplo.tf"
     ```
     ````
   - **`examples/exemplo.sh`** — bloco com linguagem `bash`:
     ````markdown
     ```bash
     --8<-- "examples/exemplo.sh"
     ```
     ````
   - **`examples/exemplo.sql`** — bloco com linguagem `sql`:
     ````markdown
     ```sql
     --8<-- "examples/exemplo.sql"
     ```
     ````

> **Nota técnica sobre `base_path`**: como `pymdownx.snippets` é configurada com `base_path: .` no Mkdocs_Config_File (Componente 1), todo caminho usado em `--8<--` é resolvido relativo à raiz do projeto — o mesmo diretório em que `mkdocs build` é executado. Por isso `--8<-- "Dockerfile"` e `--8<-- "examples/exemplo.js"` funcionam sem exigir nenhuma configuração adicional por página, apenas o caminho relativo correto a partir da raiz.

> **Diferença entre incorporação de snippet e mkdocstrings** (Requirement 11.19): a incorporação via `pymdownx.snippets` copia o conteúdo bruto do arquivo referenciado no momento do `mkdocs build` — o texto exibido está sempre sincronizado com o arquivo real, mas nenhuma estrutura é extraída dele (é uma cópia literal, byte a byte, sem conceito de "assinatura" ou "docstring"). Já o Mkdocstrings_Plugin (handlers `python` e `typescript`, Componentes 6 e 9) analisa o código-fonte e extrai, de forma estruturada, a assinatura da função/classe e sua documentação (docstring Google ou comentário JSDoc), formatando-as como seções distintas (`Args`, `Returns`, `Raises`, etc.). A Snippets_Page explica essa distinção explicitamente para que o leitor saiba quando usar cada abordagem.

### 11. `docs/imagens-recursos-visuais.md` — Images_Page

Componente que explica o enriquecimento de imagens do Documentation_Site através do Glightbox_Plugin, de `attr_list`/`pymdownx.blocks.caption` e do recurso nativo `optimize` do tema Material (Requirements 12.1–12.10).

1. **Glightbox_Plugin — instalação e finalidade**: a página descreve o comando de instalação:
   ```bash
   uv add mkdocs-glightbox
   ```
   e a configuração correspondente em `plugins` (Componente 1):
   ```yaml
   plugins:
     - glightbox
   ```
   O Glightbox_Plugin intercepta, no momento do build, toda imagem Markdown (`![alt](caminho)`) renderizada em qualquer página do Documentation_Site e a envolve automaticamente em um comportamento de lightbox (zoom em tela cheia ao clicar, com navegação entre imagens da mesma página) — sem exigir nenhuma marcação adicional por imagem. Esse comportamento se aplica a **qualquer** imagem Markdown da página, inclusive imagens de exemplo referenciadas apenas textualmente.

2. **Ausência de um arquivo de imagem binário real (Requirement 12.4)**: reaproveitando a mesma lógica de "observação textual" já usada na Customization_Page (Componente 5, Requirement 5.6), a Images_Page registra explicitamente que este projeto ainda não possui um arquivo de imagem real em `docs/assets/` para demonstrar o Glightbox_Plugin visualmente. A página explica o comportamento do plugin em prosa e através dos exemplos de sintaxe abaixo, deixando claro que, assim que uma imagem real for adicionada em `docs/assets/`, o Glightbox_Plugin passa a envolvê-la automaticamente em lightbox sem qualquer configuração adicional por página.

3. **Exemplo com `attr_list` (Requirement 12.7)** — dimensiona uma imagem usando a sintaxe de atributos:
   ```markdown
   ![Diagrama do site](assets/logo.png){: width="300" }
   ```
   `attr_list` permite anexar atributos HTML (`width`, `height`, `align`, classes CSS) diretamente após qualquer elemento Markdown — aqui, após a sintaxe de imagem.

4. **Exemplo com `pymdownx.blocks.caption` (Requirement 12.8)** — adiciona uma legenda abaixo de uma imagem:
   ```markdown
   ![Diagrama do site](assets/logo.png)

   /// caption
   Legenda da imagem
   ///
   ```
   O bloco `/// caption ... ///`, posicionado imediatamente após a imagem, é renderizado como um elemento `<figcaption>` associado a ela.

5. **Otimização nativa via `optimize` do Material (Requirement 12.9)**: a página menciona, de forma conceitual, que o tema `material` oferece um plugin nativo `optimize` (habilitável via `plugins: [optimize]`) que converte e comprime automaticamente imagens referenciadas em `docs/` durante o build (ex.: gerando variantes `.webp` e redimensionando imagens grandes), reduzindo o tamanho final do Documentation_Site sem exigir pré-processamento manual das imagens pelo autor do conteúdo. Este projeto não habilita `optimize` no `mkdocs.yml` (não há imagens reais a otimizar ainda — ver item 2 acima); a página apenas documenta sua existência e finalidade como próximo passo recomendado para quando imagens reais forem adicionadas.

### 12. `docs/diagramas-arquitetura.md` — Diagrams_Page

Componente que explica a renderização nativa de diagramas Mermaid pelo Documentation_Site, sem exigir nenhuma ferramenta externa instalada (Requirements 13.1–13.6).

1. **Configuração `custom_fences` (Requirement 13.3)**: a página explica que, por padrão, `pymdownx.superfences` renderiza blocos cercados (` ``` `) apenas como blocos de código com destaque de sintaxe. A opção `custom_fences`, configurada em `markdown_extensions` (Componente 1):
   ```yaml
   markdown_extensions:
     - pymdownx.superfences:
         custom_fences:
           - name: mermaid
             class: mermaid
             format: !!python/name:pymdownx.superfences.fence_code_format
   ```
   instrui especificamente o formato `mermaid` a, em vez de aplicar destaque de sintaxe, envolver o conteúdo do bloco em uma `<div class="mermaid">`. O tema Material já inclui a biblioteca JavaScript do Mermaid, que localiza essas `<div>` no HTML renderizado e desenha o diagrama diretamente no navegador — sem exigir nenhum binário externo instalado no ambiente de build.

2. **Diagrama Mermaid inserido de verdade na página (Requirement 13.2)**:
   ````markdown
   ```mermaid
   flowchart LR
       A[GitHub] --> B[GitHub Actions]
       B --> C[Build MkDocs]
       C --> D[GitHub Pages]
       D --> E[Documentação publicada]
   ```
   ````
   Este bloco `flowchart` representa o fluxo típico de publicação contínua da documentação: um push para o GitHub dispara o workflow de GitHub Actions, que executa o build do MkDocs e publica o resultado estático no GitHub Pages, tornando a documentação publicada acessível aos leitores.

3. **PlantUML e Graphviz como alternativas conceituais (Requirements 13.4–13.5)**: a página menciona, apenas como referência conceitual e sem instalação neste projeto:
   - **PlantUML** — ferramenta para diagramas UML (sequência, classes, componentes), descrita a partir de seu site oficial; exige um binário Java instalado para renderizar os diagramas (via `plantuml.jar` ou um servidor PlantUML), o que o Project_Manifest deste projeto não instala.
   - **Graphviz** — ferramenta para renderização de grafos genéricos a partir da linguagem DOT; exige o binário externo `dot` do Graphviz instalado no sistema operacional, também não instalado por este projeto.
   Ambas são apresentadas como alternativas válidas para casos que o Mermaid não cobre bem (ex.: diagramas UML formais), mas fora do escopo de instalação desta spec — diferentemente do Mermaid, que funciona apenas com a configuração `custom_fences` acima, sem dependências de sistema.

### 13. `docs/integracao-github.md` — GitHub_Integration_Page

Componente que explica a integração do Documentation_Site com um repositório GitHub: links de edição/visualização de página e data de revisão (Requirements 14.1–14.10).

1. **`repo_url`, `repo_name` e `edit_uri` (Requirement 14.6)**: a página explica cada campo definido na raiz do `mkdocs.yml` (Componente 1):
   - `repo_url`: URL completa do repositório, usada pelo tema Material para exibir um ícone/link para o repositório no cabeçalho do site e para montar os links de edição de cada página.
   - `repo_name`: o texto exibido ao lado do ícone do repositório (geralmente `usuário/repositório`).
   - `edit_uri`: o sufixo de caminho, relativo a `repo_url`, usado para montar o link "editar esta página" de cada página (aqui, `edit/main/docs/`, apontando para a branch `main` e a pasta `docs/`).
   A página usa o valor configurado, `https://github.com/seu-usuario/teste-mkdocks` — o Repository_Placeholder_URL —, e instrui explicitamente o leitor a substituí-lo pela URL real de seu próprio repositório (ex.: `https://github.com/sua-org/seu-repo`) antes de publicar o Documentation_Site; enquanto o placeholder permanecer, os links de edição/visualização apontam para um repositório de exemplo inexistente.

2. **`theme.features` — ações de edição e visualização (Requirement 14.7)**: a página explica que `content.action.edit` e `content.action.view` (Componente 1, `theme.features`) fazem o tema Material exibir, no topo de cada página do Documentation_Site, dois botões: um link "Editar esta página" (usando `edit_uri`, geralmente apontando para o editor de arquivos do GitHub) e um link "Ver código-fonte desta página" (apontando para o arquivo Markdown bruto no repositório, usando `repo_url`). Sem essas entradas em `theme.features`, os campos `repo_url`/`edit_uri` continuam habilitando o ícone do repositório no cabeçalho, mas não os botões de ação por página.

3. **Git_Revision_Date_Plugin e a ausência de histórico git (Requirement 14.5)**: a página apresenta a configuração (Componente 1):
   ```yaml
   plugins:
     - git-revision-date-localized:
         fallback_to_build_date: true
         enable_creation_date: true
         type: timeago
   ```
   e explica que o Git_Revision_Date_Plugin lê o histórico de commits do repositório git local para exibir, no rodapé de cada página, a data da última revisão (e, com `enable_creation_date: true`, também a data de criação) em formato relativo (`type: timeago`, ex.: "editado há 2 dias"). A página registra explicitamente que o repositório local deste projeto não possui nenhum commit — logo, sem histórico git para consultar, o plugin falharia ao resolver uma data de revisão para qualquer página. A opção `fallback_to_build_date: true` evita que isso interrompa o build: quando não há histórico git disponível para um arquivo, o plugin usa a data/hora do próprio build como substituto, em vez de lançar um erro.

4. **Workflow de GitHub Actions — referência conceitual (Requirements 14.8–14.9)**: a página apresenta o trecho YAML abaixo apenas como referência conceitual, deixando explícito que ele **não** corresponde a um arquivo real criado neste projeto (não existe `.github/workflows/docs.yml` nesta spec):
   ````markdown
   ```yaml
   # .github/workflows/docs.yml (exemplo ilustrativo, não criado neste projeto)
   name: docs
   on:
     push:
       branches: [main]
   jobs:
     build:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
           with:
             fetch-depth: 0   # histórico completo, necessário para o git-revision-date-localized
         - uses: astral-sh/setup-uv@v3
         - run: uv sync
         - run: uv run mkdocs build
   ```
   ````
   A página explica que, em um pipeline de integração contínua real, `actions/checkout` por padrão baixa apenas o último commit (`fetch-depth: 1`); como o Git_Revision_Date_Plugin precisa percorrer o histórico de cada arquivo para determinar sua data de última modificação, `fetch-depth: 0` (histórico completo) é necessário para que o plugin calcule datas de revisão corretas durante um build em CI — em vez de cair sistematicamente no `fallback_to_build_date` também em produção.

### 14. `docs/extensoes-pymdownx.md` — Pymdown_Extensions_Page

Componente que cataloga as extensões do Pymdown_Extensions_Package relevantes para código e documentação técnica (Requirements 15.1–15.8).

1. **Tabela das 8 extensões (Requirement 15.1)**:

   | Extensão | Finalidade |
   |---|---|
   | `pymdownx.highlight` | Destaque de sintaxe (syntax highlighting) para blocos de código. |
   | `pymdownx.superfences` | Blocos de código cercados avançados, incluindo aninhamento e cercas customizadas (ex.: diagramas Mermaid). |
   | `pymdownx.snippets` | Incorporação do conteúdo bruto de arquivos reais do projeto dentro de blocos de código via `--8<--`. |
   | `pymdownx.tabbed` | Conteúdo organizado em abas alternáveis (ex.: exemplos do mesmo conceito em linguagens diferentes). |
   | `pymdownx.inlinehilite` | Destaque de sintaxe para trechos de código em linha (inline), não apenas em blocos. |
   | `pymdownx.tasklist` | Listas de tarefas (checklists) com caixas de seleção renderizadas em HTML. |
   | `pymdownx.details` | Seções expansíveis/colapsáveis (similar a `<details>`), opcionalmente estilizadas como admonitions. |
   | `pymdownx.emoji` | Renderização de códigos de emoji (ex.: `:rocket:`) como ícones SVG/imagem. |

2. **Exemplo de `pymdownx.tabbed` (Requirement 15.4)** — abas Python/JavaScript/PowerShell para o mesmo conceito (listar arquivos do diretório atual):
   ```markdown
   === "Python"

       ```python
       import os
       print(os.listdir("."))
       ```

   === "JavaScript"

       ```javascript
       const fs = require("fs");
       console.log(fs.readdirSync("."));
       ```

   === "PowerShell"

       ```powershell
       Get-ChildItem .
       ```
   ```
   Com `alternate_style: true` (Componente 1), o tema Material renderiza essas três abas como um seletor horizontal, exibindo apenas o conteúdo da aba ativa por vez.

3. **Exemplo de `pymdownx.tasklist` (Requirement 15.5)**:
   ```markdown
   - [x] Tarefa concluída
   - [ ] Tarefa pendente
   ```
   Com `custom_checkbox: true` (Componente 1), cada item é renderizado como uma caixa de seleção estilizada pelo tema Material, em vez do caractere `☑`/`☐` padrão do navegador.

4. **Exemplo de `pymdownx.details` (Requirement 15.6)**:
   ```markdown
   ??? note "Título"
       Conteúdo colapsado por padrão, exibido ao clicar no título.
   ```
   O bloco `??? note "Título"` (três pontos de interrogação) renderiza uma seção expansível fechada por padrão; `??? note` com quatro pontos de interrogação (`????`) a renderizaria já aberta — a página menciona ambas as variantes.

5. **Exemplo de `pymdownx.emoji` (Requirement 15.7)**:
   ```markdown
   Lançamento da versão 1.0! :rocket:
   ```
   Renderizado como "Lançamento da versão 1.0! 🚀", usando a configuração `emoji_index`/`emoji_generator` do Componente 1 (índice e gerador de SVG do próprio tema Material/Twemoji).

6. **Caixas de nota vs. âncoras de referência: nem tudo é pymdownx (Requirement 19.5)**:

   A página esclarece que nem todo recurso de "caixa" ou "âncora" vem de uma extensão do namespace `pymdownx`:
   - **Caixas de nota/atenção**: `admonition` fornece as caixas sempre visíveis (`!!! note`, `!!! warning`, etc.), já apresentadas no restante do tutorial; `pymdownx.details` (Componente 14, item 4 acima) cobre a variante **colapsável** da mesma ideia (`??? note "Título"`), com ícone e título idênticos aos de `admonition`, mas com conteúdo oculto por padrão.
   - **Âncoras de referência**: `toc`, configurada com `permalink: true` (Componente 1), adiciona um link-âncora (🔗) ao lado de cada título de seção, permitindo copiar um link direto para aquele ponto da página; `footnotes` adiciona notas de rodapé com uma âncora de ida-e-volta — um número sobrescrito no texto (`[^1]`) que leva ao rodapé, e uma seta (`↩`) no próprio rodapé que leva de volta ao ponto de origem no texto.
   - Das quatro extensões citadas nesta seção, apenas `pymdownx.details` pertence ao namespace `pymdownx`; `admonition`, `toc` e `footnotes` são extensões nativas do Python-Markdown.

7. **Extensões de referência (Requirement 19.1 e 19.6)** — Reference_Extensions, cada uma com um exemplo real inserido nesta própria página:

   - `abbr` — abreviação com tooltip ao passar o mouse, definida uma única vez no final da página e usada no texto como `HTML`:
     ```markdown
     A página usa HTML e CSS para estruturar o conteúdo.

     *[HTML]: HyperText Markup Language
     ```
   - `def_list` — lista de definição:
     ```markdown
     Termo
     :   Definição do termo, explicando seu significado.
     ```
   - `footnotes` — nota de rodapé com âncora de ida-e-volta:
     ```markdown
     Texto com referência[^1].

     [^1]: Explicação da nota.
     ```
   - `tables` — tabela Markdown simples:
     ```markdown
     | Extensão | Namespace |
     |---|---|
     | `abbr` | nativa |
     | `pymdownx.mark` | `pymdownx` |
     ```

8. **Extensões de formatação de texto (Requirement 19.2 e 19.6)** — Text_Formatting_Extensions, cada uma com um exemplo real inserido nesta própria página:

   - `pymdownx.mark` — destaque de texto: `==destaque==`
   - `pymdownx.caret` — sobrescrito: `H^2^O` (também usado para sublinhado: `^^sublinhado^^`)
   - `pymdownx.tilde` — subscrito: `H~2~O` (também usado para tachado: `~~tachado~~`)
   - `pymdownx.keys` — combinação de teclas: `++ctrl+shift+p++`
   - `pymdownx.critic` — marcação de revisões (inserções/exclusões): `{--texto removido--}{++texto adicionado++}`
   - `pymdownx.magiclink` — uma URL solta no texto, convertida automaticamente em link clicável sem sintaxe Markdown adicional: `https://www.mkdocs.org`
   - `pymdownx.smartsymbols` — conversão de sequências de caracteres em símbolos tipográficos: `-->` torna-se → e `(c)` torna-se ©

9. **Numeração e destaque de linhas de código (Requirement 19.8)**:

   Reaproveitando a configuração de `pymdownx.highlight` já definida no Componente 1 (`anchor_linenums`, `line_spans`, `pygments_lang_class`), a página demonstra as opções `linenums` e `hl_lines`, suportadas através da integração entre `pymdownx.highlight` e `pymdownx.superfences`:

   ````markdown
   ```python linenums="1" hl_lines="2 4"
   def saudacao(nome: str) -> str:
       mensagem = f"Olá, {nome}!"
       print(mensagem)
       return mensagem
   ```
   ````

   O resultado renderiza o bloco com números de linha a partir de `1` e destaca visualmente as linhas 2 e 4.

10. **Fórmulas matemáticas com Arithmatex (Requirement 19.3, 19.4 e 19.7)**:

    A página explica que `pymdownx.arithmatex`, configurada com `generic: true` (Componente 1), apenas prepara o HTML das fórmulas LaTeX para renderização — sem o `extra_javascript` apontando para os Mathjax_Frontend_Scripts (MathJax, também configurado no Componente 1), o HTML fica pronto, mas nenhuma fórmula aparece de fato na página; os dois precisam estar presentes juntos. Exemplo real de fórmula em bloco:
    ```markdown
    \[ \text{média} = \frac{\sum valores}{n} \]
    ```
    E de fórmula em linha, no meio de uma frase: a famosa equação \(E = mc^2\), escrita em Markdown como `\(E = mc^2\)`.

11. **Quantas extensões habilitar? (Requirement 19.9)**:

    A página encerra com uma observação recomendando não habilitar todas as extensões `pymdown-extensions` de uma vez: comece pelo conjunto essencial — `pymdownx.highlight`, `pymdownx.superfences`, `pymdownx.snippets`, `pymdownx.tabbed`, `pymdownx.details` e `pymdownx.tasklist` — e adicione as demais (como as Reference_Extensions, as Text_Formatting_Extensions e a Arithmatex_Extension catalogadas nesta seção) apenas quando a necessidade de fato aparecer no conteúdo sendo escrito, mantendo o `mkdocs.yml` organizado e evitando funcionalidades redundantes ou nunca utilizadas.

### 15. `docs/outros-plugins.md` — Other_Plugins_Page

Componente que documenta o Macros_Plugin, o Native_Redirect_Hook, o Minify_Plugin, o Awesome_Pages_Plugin e o Exporter_Plugin (Requirements 16.1–16.11 e 18.1–18.5).

1. **Macros_Plugin**:
   ```bash
   uv add mkdocs-macros-plugin
   ```
   ```yaml
   plugins:
     - macros
   ```
   A página explica que o Macros_Plugin expõe um contexto Jinja2 dentro de cada página Markdown, permitindo variáveis e macros reutilizáveis. O exemplo mais simples é uma variável embutida do próprio MkDocs, disponível sem nenhuma configuração adicional:
   ```markdown
   Você está lendo: {{ page.title }}
   ```
   Para macros customizadas, a página descreve a convenção do plugin: um arquivo `main.py` (ou `macros.py`) na raiz do projeto, expondo uma função `define_env(env)` que registra macros Python chamáveis dentro das páginas, por exemplo:
   ```python
   # main.py (ou macros.py), na raiz do projeto
   def define_env(env):
       @env.macro
       def versao_atual():
           return "1.0.0"
   ```
   usada em qualquer página Markdown como `{{ versao_atual() }}`.

2. **Redirecionamentos sem dependência externa (`hooks`)** (Requirements 16.4–16.6):

   **Por que `mkdocs-redirects` foi evitado**: a partir da versão 1.2.3, o pacote `mkdocs-redirects` passou a depender transitivamente do pacote `properdocs` — um fork concorrente do próprio MkDocs, surgido de uma disputa de governança em 2026. A página esclarece que isso **não é malware**: `properdocs` é um projeto legítimo. Ainda assim, é uma dependência desnecessária e controversa para uma funcionalidade tão simples quanto gerar algumas páginas de redirecionamento, e por isso o design evita essa cadeia de dependência em favor de uma alternativa totalmente nativa do MkDocs.

   **A alternativa nativa `hooks`**: desde a versão 1.4, o MkDocs oferece a opção de configuração `hooks` (documentada oficialmente em [mkdocs.org/user-guide/configuration/#hooks](https://www.mkdocs.org/user-guide/configuration/#hooks)), que permite registrar um ou mais scripts Python locais como manipuladores dos mesmos eventos do ciclo de build que um plugin usaria (`on_config`, `on_page_markdown`, `on_post_build`, etc.) — sem instalar nenhum pacote adicional do PyPI. Basta que o script exponha funções com o nome do evento desejado; o MkDocs as descobre e chama automaticamente. A página apresenta a configuração usada neste projeto (Componente 1):
   ```yaml
   hooks:
     - hooks/redirects.py
   ```

   **Conteúdo completo de `hooks/redirects.py`** (Native_Redirect_Hook), inserido de fato na página: um dicionário `REDIRECTS` mapeando o caminho antigo `'preview.md'` para o caminho real atual `'playwright-preview.md'` (a mesma renomeação hipotética ilustrada no exemplo anterior deste design — ver Componente 8), e uma função `on_post_build(config, **kwargs)` que, para cada entrada do mapeamento, escreve um arquivo HTML de redirecionamento dentro de `config["site_dir"]`, usando `<meta http-equiv="refresh" content="0; url=...">`:
   ```python
   """hooks/redirects.py — Native_Redirect_Hook.

   Gera páginas de redirecionamento HTML (meta refresh) para caminhos antigos
   de página, sem depender do pacote `mkdocs-redirects` (nem, por
   consequência, do pacote `properdocs`). Referenciado na opção `hooks` do
   mkdocs.yml.
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
   ```
   A página explica que esse script replica o comportamento essencial do `mkdocs-redirects` (gerar, para `docs/preview.md`, um arquivo `site/preview/index.html` que redireciona para `site/playwright-preview/index.html`) rodando durante o evento `on_post_build` — ou seja, depois que o MkDocs já gerou todas as páginas normais em `site/`, o hook apenas adiciona os arquivos de redirecionamento extras, sem interferir no restante do build.

3. **Minify_Plugin**:
   ```bash
   uv add mkdocs-minify-plugin
   ```
   ```yaml
   plugins:
     - minify:
         minify_html: true
   ```
   A página explica que o Minify_Plugin, com `minify_html: true`, remove espaços em branco, comentários e formatação redundante do HTML gerado para cada página durante o build, reduzindo o tamanho final dos arquivos publicados em `site/` sem alterar a renderização visível ao leitor.

4. **Awesome_Pages_Plugin**:
   ```bash
   uv add mkdocs-awesome-pages-plugin
   ```
   ```yaml
   plugins:
     - awesome-pages
   ```
   A página explica a finalidade geral do plugin — permitir organizar a navegação por pasta através de arquivos `.pages` colocados dentro de `docs/`, sem precisar listar manualmente cada página na seção `nav` do `mkdocs.yml`. Em seguida, a página registra a observação honesta exigida pelo Requirement 16.10: como o `mkdocs.yml` deste projeto já define a seção `nav` explicitamente (Componente 1, com todas as 13 entradas do tutorial), o Awesome_Pages_Plugin **não reorganiza** a navegação deste site específico — conforme a própria documentação oficial do plugin, quando uma seção `nav` explícita está presente no arquivo de configuração, ela tem precedência, e os arquivos `.pages` são ignorados para fins de ordenação/estrutura de `nav`. O plugin permanece habilitado nesta configuração apenas para fins de demonstração (Requirement 16.9), sem efeito prático sobre a navegação atual.
   Como referência, para um projeto **sem** `nav` explícita, a página mostra o formato de um arquivo `.pages` que poderia ser colocado dentro de uma subpasta de `docs/` para controlar título e ordem daquela seção:
   ```yaml
   # docs/alguma-pasta/.pages
   title: "Título da Seção"
   nav:
     - introducao.md
     - ...
     - avancado.md
   ```

5. **Exportação para PDF (`mkdocs-exporter`)** (Requirements 18.1–18.5):
   ```bash
   uv add mkdocs-exporter
   ```
   ```yaml
   plugins:
     - exporter:
         formats:
           pdf:
             enabled: true
   ```
   A página explica que o Exporter_Plugin, com `formats.pdf.enabled: true`, gera uma versão em PDF de cada página do Documentation_Site durante o build. Para isso, o plugin abre cada página já renderizada em um navegador headless e usa esse navegador para "imprimir" o PDF — a mesma técnica de automação de navegador documentada na Preview_Page (Componente 8, Requirement 9) para o Preview_Script. Por isso, o Exporter_Plugin **reaproveita o Playwright_Package já instalado no projeto** (via `uv add playwright` + `uv run playwright install chromium`, Requirement 9.1–9.2) em vez de depender de uma ferramenta de renderização de PDF separada: qualquer navegador Chromium já disponível no cache local do Playwright passa a ser usado também pelo Exporter_Plugin, sem instalação adicional de binário.
   A página explica que, após o build, cada página do Documentation_Site passa a exibir um botão/link de download do PDF correspondente (inserido pelo plugin no topo ou no rodapé do conteúdo renderizado, dependendo do tema), permitindo ao leitor obter uma versão para impressão/leitura offline daquela página sem precisar gerar o PDF manualmente.

### 16. Arquivo real de GitHub Actions (`.github/workflows/docs.yml`) e tutorial de CI/CD

Componente que substitui, pelo arquivo real, o trecho YAML até então apenas ilustrativo apresentado no Componente 13 (GitHub_Integration_Page, Requirements 14.8–14.9) — o GitHub_Actions_Workflow (Requirements 20.4–20.12), responsável por buildar o Documentation_Site com `uv` e publicá-lo no GitHub Pages do Real_Repository_URL (`https://github.com/dataRainBR/mkdocs-documentation`).

**`.github/workflows/docs.yml`** — conteúdo completo e real:

```yaml
name: Build e publica a documentação

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Clonar o repositório
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Configurar Node.js (necessário para o TypeDoc)
        uses: actions/setup-node@v4
        with:
          node-version: "20"

      - name: Instalar TypeScript e TypeDoc
        run: npm install --global typescript typedoc

      - name: Gerar as declarações TypeScript (.d.ts)
        run: tsc -p src/calcular-media/tsconfig.json

      - name: Instalar o uv
        uses: astral-sh/setup-uv@v3

      - name: Instalar dependências Python
        run: uv sync

      - name: Instalar o Chromium do Playwright
        run: uv run playwright install --with-deps chromium

      - name: Buildar a documentação
        run: uv run mkdocs build --strict

      - name: Publicar artefato do GitHub Pages
        uses: actions/upload-pages-artifact@v3
        with:
          path: site

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Publicar no GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

**Explicação passo a passo do job `build`** (Requirement 20.10):

1. **Clonar o repositório** (`actions/checkout@v4`, `fetch-depth: 0`) — baixa o histórico completo de commits, em vez do padrão `fetch-depth: 1` (apenas o último commit). Histórico completo é necessário para que o Git_Revision_Date_Plugin (Componente 1 e 13, Requirement 14.4) calcule corretamente a data de última revisão/criação de cada página a partir do histórico git real, em vez de cair sistematicamente no `fallback_to_build_date` também em produção.
2. **Configurar Node.js** (`actions/setup-node@v4`, `node-version: "20"`) e **Instalar TypeScript e TypeDoc** (`npm install --global typescript typedoc`) — diferentemente do ambiente local de desenvolvimento desta spec (onde Node.js/npm não estão instalados, ver Componente 9 e a observação de Testing Strategy sobre o Requirement 10), o runner do GitHub Actions **tem** Node.js disponível depois destas duas etapas. Isso permite que a etapa seguinte gere de fato o `.d.ts` do TypeScript_Example_Package e que o build em CI consiga buildar a Code_Examples_Page com a diretiva `::: calcular-media` (`handler: typescript`) funcionando de ponta a ponta — algo que não pôde ser validado localmente nesta spec.
3. **Gerar as declarações TypeScript (`tsc -p src/calcular-media/tsconfig.json`)** — executa o compilador TypeScript com a configuração do TypeScript_Example_Package (Componente 9), produzindo `src/calcular-media/src/index.d.ts`, que o handler `typescript` do Mkdocstrings_Plugin consome durante o build do MkDocs.
4. **Instalar o uv** (`astral-sh/setup-uv@v3`) e **Instalar dependências Python** (`uv sync`) — preparam o ambiente Python do projeto a partir de `pyproject.toml`/`uv.lock`, da mesma forma que um desenvolvedor faria localmente.
5. **Instalar o Chromium do Playwright** (`uv run playwright install --with-deps chromium`) — necessário para que o Exporter_Plugin (Componente 15, Requirement 18) consiga abrir cada página renderizada em um navegador headless e gerar o PDF correspondente durante o build; sem essa etapa, o build falharia ao tentar abrir um navegador Chromium ainda não instalado no runner.
6. **Buildar a documentação** (`uv run mkdocs build --strict`) — gera o Documentation_Site estático em `site/`, com `--strict` garantindo que qualquer referência quebrada (ex.: item de `nav` sem arquivo correspondente, ver Property 1) interrompa o workflow em vez de publicar um site incompleto.
7. **Publicar artefato do GitHub Pages** (`actions/upload-pages-artifact@v3`, `path: site`) — empacota o conteúdo de `site/` como um artefato de build, pronto para ser consumido pelo job `deploy`.

**Explicação do job `deploy`** (Requirement 20.6):

O job `deploy` depende do `build` através de `needs: build`, só executando se o build for concluído com sucesso. Ele usa o ambiente especial `github-pages` do GitHub (que expõe a URL publicada em `steps.deployment.outputs.page_url`) e publica o artefato gerado pelo job anterior através de `actions/deploy-pages@v4` — a forma oficialmente recomendada atualmente para publicar no GitHub Pages, em vez do padrão mais antigo de fazer commit do site estático em uma branch `gh-pages`.

**Permissões do workflow** (Requirement 20.12):

```yaml
permissions:
  contents: read
  pages: write
  id-token: write
```

`contents: read` permite ao workflow ler o código do repositório (necessário para o checkout); `pages: write` autoriza o workflow a publicar no GitHub Pages; `id-token: write` permite que o job `deploy` obtenha um token OIDC de curta duração usado internamente por `actions/deploy-pages` para autenticar a publicação. Com essas três permissões, o workflow publica no GitHub Pages sem exigir nenhum token/secret configurado manualmente pelo usuário no repositório.

**Configuração necessária no site do GitHub, fora do workflow** (Requirement 20.11):

No repositório `dataRainBR/mkdocs-documentation`, é preciso acessar **Settings → Pages → Build and deployment → Source** e selecionar **"GitHub Actions"** como fonte de publicação (em vez da opção padrão **"Deploy from a branch"**) — sem essa configuração manual no site do GitHub, o GitHub Pages não aceita o artefato publicado por `actions/deploy-pages`, mesmo com o workflow configurado corretamente.

**Nota sobre o remote git e o push do código** (Requirement 20.13):

Caso o repositório local do projeto ainda não possua um remote git configurado, adicionar um remote apontando para o Real_Repository_URL (`git remote add origin https://github.com/dataRainBR/mkdocs-documentation.git`) é uma ação segura e reversível — ela apenas registra, no `.git/config` local, um endereço de referência, sem enviar nenhum dado ao repositório remoto por si só. Já o commit e o push do código para esse repositório real (etapa que de fato tornaria o GitHub_Actions_Workflow executável e o Documentation_Site publicável) é uma decisão que depende de o leitor revisar e confirmar o conteúdo a ser publicado, e deve ser executada separadamente, por fora da implementação automática desta spec.

## Data Models

Não há modelos de dados em tempo de execução (esta é uma funcionalidade de documentação estática). Os "dados" do sistema são os próprios artefatos de arquivo:

- **Config model** (`mkdocs.yml`): mapa YAML com as chaves `site_name`, `docs_dir`, `nav` (lista ordenada de pares título→arquivo), `theme` (objeto com `name`, `logo`, `favicon`, `font`, `palette`), `plugins` (lista, incluindo o objeto `mkdocstrings.handlers.{python,typescript}`), `markdown_extensions` (lista).
- **Page model**: cada item de `nav` é um par `(título: str, caminho_relativo: str)` que deve corresponder a um arquivo existente dentro de `docs/`.
- **Code reference model**: a string `teste.calcular_media`, resolvida pelo handler Python do mkdocstrings como `módulo.função`, usando `paths: [.]` para localizar `teste.py` na raiz do projeto. O mesmo modelo se aplica à referência de módulo inteiro `docs_preview`, resolvida pelo mesmo `paths: [.]` a partir de `docs_preview.py`, também na raiz do projeto.

## Error Handling

| Cenário de erro | Tratamento |
|---|---|
| `mkdocs build` falha por chave inválida no YAML | Corrigir a sintaxe/estrutura do `mkdocs.yml` antes de prosseguir; validar localmente com `uv run mkdocs build --strict` durante o desenvolvimento. |
| mkdocstrings não encontra o módulo `teste` (`ModuleNotFoundError`) | Garantir `plugins.mkdocstrings.handlers.python.paths: [.]` no `mkdocs.yml` (Requirement 8.3), e executar o build a partir da raiz do projeto. |
| Item de `nav` aponta para um arquivo `.md` inexistente em `docs/` | O build do MkDocs falha explicitamente; todo arquivo referenciado em `nav` deve ser criado em `docs/` antes do build (ver Property 1). |
| `theme.logo`/`theme.favicon` aponta para um arquivo que não existe em `docs/assets/` | Não é um erro fatal de build — o MkDocs/Material usa o ícone padrão; a Customization_Page documenta esse comportamento em vez de exigir um binário de imagem (Requirement 5.6). |
| Docstring de `calcular_media` for alterada em `teste.py` e o bloco de código estático em `exemplos-codigo.md` não for atualizado | Não é um erro de build, mas uma inconsistência de conteúdo; coberta pela Property 2 abaixo, que deve ser revalidada manualmente ou via teste automatizado sempre que `teste.py` mudar. |
| mkdocstrings não encontra o módulo `docs_preview` (`ModuleNotFoundError`) ao renderizar `playwright-preview.md` | Não deve ocorrer: `docs_preview.py` está na raiz do projeto, no mesmo diretório que `teste.py`, já coberto por `plugins.mkdocstrings.handlers.python.paths: [.]` (Requirement 8.3); se ainda assim ocorrer, confirmar que o build é executado a partir da raiz do projeto, como nos demais casos de resolução de módulo acima. |
| `playwright install chromium` não foi executado antes de `uv run docs_preview.py` | Não é um erro de build da documentação — é tratado em tempo de execução pelo próprio Preview_Script (`ensure_playwright_browser_installed`), que roda `playwright install chromium` automaticamente antes de abrir o navegador; a Preview_Page documenta o comando explicitamente para quem quiser instalar o navegador manualmente com antecedência (Requirement 9.2). |
| TypeDoc/Node.js não instalado no ambiente de build → a diretiva `::: calcular-media` (handler `typescript`) falha ao buildar | Não deve bloquear as demais páginas do Documentation_Site: a limitação é documentada explicitamente em `exemplos-codigo.md` (observação do Requirement 10.10), em vez de impedir a geração das outras Tutorial_Pages. Se um `uv run mkdocs build --strict` real precisar passar nesse ambiente sem Node.js, a diretiva `::: calcular-media` deve ser tratada como conhecida-pendente (documentada como não validada localmente) até que o leitor rode o build em uma máquina com Node.js/TypeDoc_Toolchain instalado. |
| Caminho de snippet inexistente ou incorreto referenciado via `--8<--` na Snippets_Page | O `pymdownx.snippets` falha explicitamente o build do MkDocs quando o arquivo referenciado não existe a partir de `base_path: .` (raiz do projeto); todo caminho usado em `--8<-- "caminho/arquivo"` (ex.: `Dockerfile`, `examples/exemplo.js`) deve apontar para um arquivo real existente antes do build, validado com `uv run mkdocs build --strict` (ver Property 1 e Testing Strategy, cobertura estendida ao Requirement 11). |
| `git-revision-date-localized` sem histórico git local e sem `fallback_to_build_date` | Sem nenhum commit no repositório, o plugin não consegue resolver uma data de revisão a partir do histórico e o build quebraria; `fallback_to_build_date: true` (Requirement 14.4) evita esse erro usando a data/hora do build como substituto — comportamento documentado explicitamente pela GitHub_Integration_Page (Requirement 14.5). |
| `awesome-pages` não reorganiza a navegação deste site | Não é um erro — é o comportamento esperado e documentado do plugin: quando o `mkdocs.yml` já define `nav` explicitamente (como neste projeto, com 13 entradas), os arquivos `.pages` são ignorados para fins de ordenação/estrutura de `nav`. A Other_Plugins_Page registra essa limitação em prosa (Requirement 16.10), em vez de remover a seção `nav` existente para "forçar" o plugin a ter efeito. |
| Script `hooks/redirects.py` referenciado em `hooks` não existe ou contém erro de sintaxe | O MkDocs falha explicitamente ao carregar o hook durante `mkdocs build`, antes mesmo de iniciar a renderização das páginas. A lógica do Native_Redirect_Hook (dicionário `REDIRECTS` e função `on_post_build`) pode ser validada localmente de forma isolada — por exemplo, importando o módulo e chamando `on_post_build` com um `config` de teste simulado — sem exigir um build real e completo do Documentation_Site apenas para verificar essa lógica. |

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

A maior parte dos critérios de aceitação desta funcionalidade descreve conteúdo textual fixo de páginas de documentação (ex.: "a página de instalação descreve o comando X"), que são melhor verificados por testes de exemplo (presença de strings/seções específicas) ou testes de integração (build real do site), e não por propriedades universais sobre um espaço de entradas variável. As duas propriedades abaixo cobrem as únicas invariantes estruturais da funcionalidade que se generalizam para além do estado atual e específico das páginas.

### Property 1: Consistência entre nav, arquivos de página e site gerado

Para toda entrada `(título, caminho)` presente na seção `nav` do `mkdocs.yml`, deve existir um arquivo Markdown correspondente em `docs/<caminho>` e, após `mkdocs build`, um arquivo HTML correspondente dentro de `site/` — isto é, nenhuma entrada de `nav` SHALL referenciar uma página que não existe, e toda página de `nav` SHALL aparecer no site gerado.

**Validates: Requirements 1.2, 1.3, 2.3, 8.1, 8.2, 9.7**

### Property 2: Fidelidade do exemplo de código à fonte

Para qualquer conteúdo atual da função `calcular_media` em `teste.py`, o bloco de código estático exibido em `exemplos-codigo.md` SHALL ser idêntico, caractere a caractere, ao código-fonte real da função, e a saída HTML gerada pela diretiva `::: teste.calcular_media` SHALL conter as seções da docstring (`Args`, `Returns`, `Raises`) tal como definidas no docstring atual da função — garantindo que nenhuma das duas formas de exibição (bloco estático ou mkdocstrings) fique desatualizada em relação ao código real.

**Validates: Requirements 6.1, 6.2, 8.3**

## Testing Strategy

**Testes de propriedade (property-based, mínimo 100 iterações onde aplicável):**
- Property 1 é, na prática, verificada sobre a lista fixa e conhecida de entradas de `nav` (não há geração aleatória de entradas novas), então sua implementação como teste automatizado é: carregar `mkdocs.yml`, iterar sobre todas as entradas de `nav`, e para cada uma verificar a existência do arquivo `.md` em `docs/` e do `.html` correspondente em `site/` após o build. Isso cobre robustamente qualquer adição/remoção futura de páginas, sem exigir dados aleatórios.
- Property 2 é verificada lendo `teste.py` com `inspect.getsource(calcular_media)` e comparando com o bloco de código em `docs/exemplos-codigo.md`, e lendo `site/exemplos-codigo/index.html` após o build para confirmar a presença de `Args`, `Returns` e `Raises` (ou seus equivalentes renderizados) vindos da docstring.

**Testes de exemplo / integração (1–3 execuções, sem necessidade de randomização):**
- Presença de cada página esperada em `docs/` (Requirement 1.2) e dos links a partir de `index.md` (Requirement 1.3).
- Presença das chaves `theme.name: material`, `theme.palette`, `theme.logo`, `plugins` (`search`, `mkdocstrings.handlers.python`, `mkdocstrings.handlers.typescript`) e `markdown_extensions` (`pymdownx.highlight`, `pymdownx.superfences`) no `mkdocs.yml` parseado (Requirements 2.2, 2.4–2.6, 2.8, 2.9).
- Presença dos comandos de instalação dos 4 pacotes em `instalacao.md` (Requirements 3.1–3.4).
- Presença das explicações de `nav`/`theme`/`plugins`/`markdown_extensions` em `configuracao-yaml.md` (Requirements 4.1–4.4).
- Presença das explicações de fontes/paleta/logo/favicon e da observação sobre ausência de imagem real em `personalizacao.md` (Requirements 5.1–5.6).
- Presença da explicação "bloco estático vs. mkdocstrings" em `exemplos-codigo.md` (Requirement 6.3).
- Presença das 6 etapas e respectivos comandos (`uv add ...`, `uv run mkdocs new .`, `uv run mkdocs build`, `uv run mkdocs serve`) em `exemplos-notebook.md` (Requirements 7.1–7.2).
- Presença dos comandos `uv add playwright` / `uv run playwright install chromium` / `uv run docs_preview.py`, da explicação sobre a finalidade do Playwright no Preview_Script e da diretiva `::: docs_preview` em `playwright-preview.md` (Requirements 9.1–9.6); e, após o build, presença da seção HTML correspondente às seis funções do módulo (`run_mkdocs_build`, `find_free_port`, `start_local_server`, `ensure_playwright_browser_installed`, `open_in_browser`, `main`) em `site/playwright-preview/index.html`.
- Execução real de `uv run mkdocs build --strict` na raiz do projeto, confirmando código de saída `0` e ausência de avisos de referência quebrada (Requirement 8.1).
- Presença e conteúdo do `Dockerfile` (dois estágios `builder`/`runtime`, comentário em cada instrução, referência a `pyproject.toml`/`uv.lock`) na raiz do projeto, e dos cinco Multi_Language_Examples (`examples/exemplo.js`, `.yaml`, `.tf`, `.sh`, `.sql`) (Requirements 11.1–11.8).
- Presença de `pymdown-extensions` nas dependências do `pyproject.toml` (Requirement 11.9) e das chaves `markdown_extensions.pymdownx.snippets.base_path`, `pymdownx.superfences`, `pymdownx.highlight` (`anchor_linenums`, `line_spans`, `pygments_lang_class`), `admonition`, `pymdownx.inlinehilite` e `toc.permalink` no `mkdocs.yml` parseado (Requirements 11.10–11.13).
- Presença da explicação sobre a ausência de handler de mkdocstrings para estas linguagens, da menção a Hadolint/Docker Buildx, e da explicação "incorporação de snippet vs. mkdocstrings" em `dockerfile-outras-linguagens.md` (Requirements 11.15, 11.16, 11.19), escrita em português (Requirement 11.20).
- Após o build, verificação de que `site/dockerfile-outras-linguagens/index.html` contém o conteúdo real incorporado do `Dockerfile` e de cada um dos cinco Multi_Language_Examples — confirmando que a sintaxe `--8<--` resolveu corretamente cada caminho a partir de `base_path: .` e que o HTML gerado reflete o conteúdo atual dos arquivos reais, e não um texto copiado manualmente (Requirements 11.17, 11.18).
- Presença das novas chaves em `mkdocs.yml` parseado: `repo_url`, `repo_name`, `edit_uri`, `theme.features` (`content.action.edit`, `content.action.view`), `hooks` (lista contendo `hooks/redirects.py`), `plugins` (`glightbox`, `git-revision-date-localized` com `fallback_to_build_date`/`enable_creation_date`/`type`, `macros`, `minify` com `minify_html`, `awesome-pages`, `exporter` com `formats.pdf.enabled`) e `markdown_extensions` (`attr_list`, `md_in_html`, `pymdownx.blocks.caption`, `pymdownx.superfences.custom_fences` para `mermaid`, `pymdownx.tabbed` com `alternate_style`, `pymdownx.tasklist` com `custom_checkbox`, `pymdownx.details`, `pymdownx.emoji`) (Requirements 12.2, 12.5, 12.6, 13.1, 14.1, 14.2, 14.4, 15.2, 15.3, 16.2, 16.4, 16.7, 16.9, 18.2).
- Presença, no `pyproject.toml`, das dependências `mkdocs-glightbox`, `mkdocs-git-revision-date-localized-plugin`, `mkdocs-macros-plugin`, `mkdocs-minify-plugin`, `mkdocs-awesome-pages-plugin` e `mkdocs-exporter` (Requirements 12.1, 14.3, 16.1, 17.3, 18.1).
- Presença do arquivo `hooks/redirects.py` na raiz do projeto, contendo o dicionário `REDIRECTS` e a função `on_post_build` (Native_Redirect_Hook), e da chave `hooks: [hooks/redirects.py]` no `mkdocs.yml` parseado (Requirements 16.4, 16.5).
- Após o build, verificação de que `site/preview/index.html` existe e contém a tag `<meta http-equiv="refresh" ...>` apontando para a página real `playwright-preview` — confirmando que o Native_Redirect_Hook gerou corretamente o redirecionamento durante o evento `on_post_build` (Requirement 16.5).
- Presença da configuração `plugins.exporter.formats.pdf.enabled: true` no `mkdocs.yml` parseado e da dependência `mkdocs-exporter` no `pyproject.toml` (Requirements 18.1, 18.2).
- Após o build, verificação de que `site/diagramas-arquitetura/index.html` contém o elemento (`<div class="mermaid">` ou SVG renderizado) correspondente ao diagrama `flowchart` da Diagrams_Page (Requirement 13.2), e que `site/extensoes-pymdownx/index.html` contém as abas Python/JavaScript/PowerShell renderizadas, a checklist do `pymdownx.tasklist`, a seção expansível do `pymdownx.details` e o emoji renderizado pelo `pymdownx.emoji` (Requirements 15.4–15.7).
- Presença de cada uma das 5 Ecosystem_Pages em `docs/` (Requirement 17.1), das 5 novas entradas em `nav` (Requirement 17.2), e execução real de `uv run mkdocs build --strict` confirmando código de saída `0` após a adição das Ecosystem_Pages e dos novos plugins/extensões (Requirement 17.4), com uma página renderizada em `site/` para cada Ecosystem_Page (Requirement 17.5).
- Presença, no `mkdocs.yml` parseado, das Reference_Extensions (`abbr`, `def_list`, `footnotes`, `tables`) e das Text_Formatting_Extensions (`pymdownx.mark`, `pymdownx.caret`, `pymdownx.tilde`, `pymdownx.keys`, `pymdownx.critic`, `pymdownx.magiclink`, `pymdownx.smartsymbols`) na seção `markdown_extensions`, da Arithmatex_Extension (`pymdownx.arithmatex` com `generic: true`), e da opção `extra_javascript` (nível raiz) contendo `javascripts/mathjax.js` e a URL do CDN do MathJax (Requirements 19.1–19.4).
- Presença do arquivo `docs/javascripts/mathjax.js` na raiz do Docs_Directory, contendo a configuração `window.MathJax` com os delimitadores `\(...\)`/`\[...\]` (Requirement 19.4).
- Após o build, verificação de que `site/extensoes-pymdownx/index.html` contém os elementos renderizados de cada nova extensão do Requirement 19: o tooltip de `abbr`, a lista de definição de `def_list`, a nota de rodapé e sua âncora de ida-e-volta de `footnotes`, a tabela de `tables`, o `<mark>`/sobrescrito/subscrito/`<kbd>` de `pymdownx.mark`/`caret`/`tilde`/`keys`, a marcação de revisão de `pymdownx.critic`, o link automático de `pymdownx.magiclink`, os símbolos tipográficos de `pymdownx.smartsymbols`, o bloco de código com `linenums`/`hl_lines` destacados, e as fórmulas em bloco e em linha preparadas pela Arithmatex_Extension (Requirements 19.6–19.8).
- Presença do arquivo `.github/workflows/docs.yml` na raiz do projeto, com sintaxe YAML válida (parseável sem erros), contendo as chaves `jobs.build.steps` (checkout com `fetch-depth: 0`, setup do Node.js/TypeScript/TypeDoc, geração do `.d.ts`, setup do `uv`, `uv sync`, instalação do Chromium do Playwright, `uv run mkdocs build --strict`, `actions/upload-pages-artifact`) e `jobs.deploy` (`needs: build`, `actions/deploy-pages`), e a seção `permissions` com `contents: read`, `pages: write` e `id-token: write` (Requirements 20.4–20.9, 20.12).
- Presença dos valores reais `https://github.com/dataRainBR/mkdocs-documentation` (`repo_url`), `dataRainBR/mkdocs-documentation` (`repo_name`) e `edit/main/docs/` (`edit_uri`) no `mkdocs.yml` parseado, confirmando a substituição do Repository_Placeholder_URL pelo Real_Repository_URL (Requirement 20.3).
- Presença da nova seção "Modos claro e escuro" em `personalizacao.md`, incluindo as três explicações exigidas (detecção automática via `prefers-color-scheme`, botão de alternância manual via `toggle`, e persistência da escolha via `localStorage` entre visitas) e o bloco YAML de `theme.palette` reafirmado (Requirement 20.1).
- Presença, em `integracao-github.md`, do conteúdo real do GitHub_Actions_Workflow explicado passo a passo, dos passos de habilitação do GitHub Pages com a fonte "GitHub Actions", da explicação das permissões `pages: write`/`id-token: write`, e da nota sobre `git remote add origin` como etapa segura e reversível, distinta da decisão de commit/push (Requirements 20.10–20.13).

**Observação sobre a validação do Requirement 10 (ambiente sem Node.js):**
- Diferentemente das demais seções acima, a verificação do Requirement 10 nesta spec é, em sua maior parte, **manual/documental**, e não automatizada por um build real: o ambiente original em que esta spec foi construída não possui Node.js/npm instalados, logo `npm install`, `npx tsc` e a parte do `uv run mkdocs build` que invoca o TypeDoc_Toolchain via handler `typescript` não puderam ser executados aqui.
- O que **pode** ser verificado automaticamente neste ambiente, sem Node.js: presença e conteúdo textual dos arquivos `src/calcular-media/src/index.ts`, `package.json`, `tsconfig.json`, `typedoc.json`, `typedoc.base.json` e `typedoc.json` da raiz (Requirements 10.1–10.4); ausência da chave `paths` em `plugins.mkdocstrings.handlers.typescript` no `mkdocs.yml` parseado (Requirement 10.5); presença do bloco de código estático de `calcularMedia`, da diretiva `::: calcular-media` com `handler: typescript`, da explicação "bloco estático vs. mkdocstrings" e da observação sobre a ausência do Node.js em `exemplos-codigo.md` (Requirements 10.6–10.11).
- O que **não** pode ser verificado automaticamente neste ambiente, e deve ser validado manualmente pelo leitor em uma máquina com Node.js instalado: que `npx tsc` gera corretamente `src/calcular-media/src/index.d.ts`, e que `uv run mkdocs build` renderiza com sucesso a saída HTML da diretiva `::: calcular-media` a partir desse `.d.ts` (equivalente, para TypeScript, à verificação de Property 2 já feita para o exemplo em Python).
