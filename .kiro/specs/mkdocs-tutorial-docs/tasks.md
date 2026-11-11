# Implementation Plan: mkdocs-tutorial-docs

## Overview

Este plano implementa a documentação MkDocs do projeto em quatro etapas: (1) criação do `mkdocs.yml` completo na raiz, (2) criação da estrutura `docs/` e `docs/assets/`, (3) redação de cada página de conteúdo do tutorial em pt-BR (incluindo a integração real com `teste.py` via mkdocstrings), e (4) validação de que `mkdocs build` processa o `mkdocs.yml` criado sem erros. O projeto é gerenciado por `uv`/Python (ver `pyproject.toml`), então os comandos usam `uv run` e os testes automatizados usam `pytest`.

## Tasks

- [x] 1. Criar o arquivo de configuração `mkdocs.yml` na raiz do projeto
  - [x] 1.1 Escrever `mkdocs.yml` completo
    - Definir `site_name`, `site_description` e `docs_dir: docs`
    - Definir `nav` com as 6 entradas na ordem: Início (`index.md`), Instalação (`instalacao.md`), Configuração do mkdocs.yml (`configuracao-yaml.md`), Personalização (`personalizacao.md`), Exemplos de código (`exemplos-codigo.md`), Exemplos do notebook (`exemplos-notebook.md`)
    - Definir `theme.name: material` com `theme.font` (text/code), `theme.palette` (variantes light/dark com `primary`/`accent`/`toggle`), `theme.logo: assets/logo.png` e `theme.favicon: assets/favicon.png`
    - Definir `plugins` com `search` e `mkdocstrings` configurado para os handlers `python` (com `paths: [.]` e `options.docstring_style: google`) e `typescript` (com `paths: [.]`)
    - Definir `markdown_extensions` com `admonition`, `pymdownx.highlight`, `pymdownx.superfences`, `pymdownx.inlinehilite` e `toc`
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9_

- [x] 2. Criar a estrutura de diretórios `docs/` e `docs/assets/`
  - [x] 2.1 Criar o diretório `docs/` e a subpasta `docs/assets/`
    - Adicionar um arquivo `.gitkeep` (ou README curto) em `docs/assets/` para garantir que a pasta vazia seja versionada, já que o projeto ainda não possui arquivos binários de logo/favicon reais
    - _Requirements: 1.1, 1.4_

- [x] 3. Escrever as páginas de conteúdo do tutorial
  - [x] 3.1 Escrever `docs/index.md`
    - Título e parágrafo de abertura explicando o propósito do tutorial
    - Lista de links em Markdown para as 5 Tutorial_Pages, na mesma ordem do `nav`
    - _Requirements: 1.3_

  - [x] 3.2 Escrever `docs/instalacao.md` (Installation_Page, pt-BR)
    - Introdução sobre o que será instalado e por quê
    - Comando `uv add mkdocs mkdocs-material "mkdocstrings[python]" mkdocstrings-typescript` com explicação individual dos 4 pacotes
    - Nota alternativa com `pip install`
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

  - [x] 3.3 Escrever `docs/configuracao-yaml.md` (Configuration_Page, pt-BR)
    - Uma seção por chave de configuração: `nav`, `theme`, `plugins` (explicando `mkdocstrings` para os handlers `python` e `typescript`) e `markdown_extensions`
    - Reaproveitar os trechos de YAML reais criados na Tarefa 1.1 como exemplo em cada seção
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

  - [x] 3.4 Escrever `docs/personalizacao.md` (Customization_Page, pt-BR)
    - Seções sobre `theme.font`, `theme.palette`, `theme.logo` e `theme.favicon`
    - Indicar `docs/assets/` como local recomendado para imagens, logo e favicon
    - Incluir observação textual informando que o projeto ainda não possui um arquivo de imagem binário real, sem exigir a criação de um PNG/ICO
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_

  - [x] 3.5 Escrever `docs/exemplos-codigo.md` (Code_Examples_Page, pt-BR)
    - Bloco de código estático com o conteúdo exato (caractere a caractere) da função `calcular_media` copiado de `teste.py`
    - Diretiva mkdocstrings `::: teste.calcular_media` para gerar a documentação a partir do docstring real
    - Explicação da diferença entre o bloco estático e a geração via mkdocstrings
    - _Requirements: 6.1, 6.2, 6.3, 6.4_

  - [ ]* 3.6 Escrever teste de propriedade para fidelidade do exemplo de código à fonte
    - **Property 2: Fidelidade do exemplo de código à fonte**
    - **Validates: Requirements 6.1, 6.2, 8.3**
    - Adicionar `pytest` como dependência de desenvolvimento via `uv add --dev pytest` caso ainda não exista
    - Usar `inspect.getsource(teste.calcular_media)` e comparar com o bloco de código presente em `docs/exemplos-codigo.md`
    - Executar `uv run mkdocs build` dentro do teste (ou em fixture) e verificar que `site/exemplos-codigo/index.html` contém as seções `Args`, `Returns` e `Raises` renderizadas a partir do docstring
    - Criar o teste em `tests/test_exemplos_codigo.py`

  - [x] 3.7 Escrever `docs/exemplos-notebook.md` (Notebook_Examples_Page, pt-BR)
    - Refletir, em texto explicativo próprio (não cópia literal), as 6 etapas do roteiro de `mkdocks.ipynb`: instalação, inicialização do projeto, build, visualização local, configuração do `mkdocs.yml` e personalizações
    - Apresentar o comando de terminal correspondente a cada etapa aplicável (`uv add ...`, `uv run mkdocs new .`, `uv run mkdocs build`, `uv run mkdocs serve`)
    - _Requirements: 7.1, 7.2, 7.3_

- [x] 4. Checkpoint - revisar conteúdo das páginas
  - Ensure all tests pass, ask the user if questions arise.

- [x] 5. Validar que `mkdocs build` roda sem erros a partir do `mkdocs.yml` criado
  - [x] 5.1 Executar `uv run mkdocs build --strict` na raiz do projeto e corrigir erros encontrados
    - Corrigir referências inválidas de `nav`, chaves de YAML malformadas ou falhas de resolução do módulo `teste` pelo mkdocstrings (ajustando `plugins.mkdocstrings.handlers.python.paths`) até o build terminar sem erros nem avisos de referência quebrada
    - _Requirements: 8.1, 8.2, 8.3_

  - [ ]* 5.2 Escrever teste de propriedade para consistência entre nav, páginas e site gerado
    - **Property 1: Consistência entre nav, arquivos de página e site gerado**
    - **Validates: Requirements 1.2, 1.3, 2.3, 8.1, 8.2**
    - Carregar e parsear `mkdocs.yml`, iterar sobre todas as entradas de `nav` e verificar que cada caminho existe em `docs/`
    - Executar `uv run mkdocs build` e verificar que cada entrada de `nav` possui um arquivo HTML correspondente em `site/`
    - Criar o teste em `tests/test_nav_consistency.py`

  - [ ]* 5.3 Escrever testes de exemplo/integração para o conteúdo das páginas e do `mkdocs.yml`
    - Verificar presença das chaves `theme.name: material`, `theme.palette`, `theme.logo`, `theme.favicon`, `plugins` (`search`, `mkdocstrings.handlers.python`, `mkdocstrings.handlers.typescript`) e `markdown_extensions` (`pymdownx.highlight`, `pymdownx.superfences`) no `mkdocs.yml` parseado
    - Verificar presença dos comandos de instalação dos 4 pacotes em `instalacao.md`, das explicações de `nav`/`theme`/`plugins`/`markdown_extensions` em `configuracao-yaml.md`, das explicações de fontes/paleta/logo/favicon em `personalizacao.md`, e das 6 etapas com comandos em `exemplos-notebook.md`
    - Criar o teste em `tests/test_paginas_conteudo.py`
    - _Requirements: 2.2, 2.4, 2.5, 2.6, 2.8, 2.9, 3.1, 3.2, 3.3, 3.4, 4.1, 4.2, 4.3, 4.4, 5.1, 5.2, 5.3, 5.4, 7.1, 7.2_

- [x] 6. Checkpoint final - garantir que o build e os testes passam
  - Ensure all tests pass, ask the user if questions arise.

- [x] 7. Adicionar a página de preview com Playwright ao tutorial
  - [x] 7.1 Atualizar `mkdocs.yml` com a 7ª entrada de `nav`
    - Adicionar a entrada `"Preview com Playwright": playwright-preview.md` à seção `nav`, imediatamente após "Exemplos do notebook"
    - _Requirements: 9.7_

  - [x] 7.2 Escrever `docs/playwright-preview.md` (Preview_Page, pt-BR)
    - Instalação do Playwright: comandos `uv add playwright` e `uv run playwright install chromium`, explicando por que ambos são necessários em sequência
    - Explicação do que é o Playwright e o motivo de seu uso no Preview_Script (`docs_preview.py`) como ferramenta de automação de navegador para abrir o Documentation_Site já buildado
    - Documentação das funções do Preview_Script via mkdocstrings, usando a diretiva de módulo inteiro `::: docs_preview` (conforme decidido no design, em vez de diretivas individuais por função)
    - Explicação de como executar o script com `uv run docs_preview.py`
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5, 9.6_

  - [x] 7.3 Validar que `uv run mkdocs build --strict` continua rodando sem erros
    - Executar o build na raiz do projeto e corrigir eventuais erros, incluindo a resolução do módulo `docs_preview` pelo mkdocstrings através de `plugins.mkdocstrings.handlers.python.paths: [.]` já existente
    - Confirmar que a Preview_Page aparece no site gerado através da nova entrada de `nav`
    - _Requirements: 9.4, 9.7, 8.1, 8.2_

- [x] 8. Adicionar exemplo real de TypeScript via mkdocstrings-typescript/TypeDoc
  - [x] 8.1 Criar o pacote TypeScript de exemplo em `src/calcular-media/`
    - Criar `src/index.ts` com a função `calcularMedia` e JSDoc completo (`@param`, `@returns`, `@throws`), equivalente à função `calcular_media` de `teste.py`
    - Criar `package.json` com `name: "calcular-media"` e `types: "src/index.d.ts"`
    - Criar `tsconfig.json` com `declaration`/`emitDeclarationOnly` habilitados para gerar `src/index.d.ts`
    - Criar `typedoc.json` estendendo a config raiz, com `entryPointStrategy: "expand"` e `entryPoints: ["src/index.d.ts"]`
    - _Requirements: 10.1, 10.2, 10.3_

  - [x] 8.2 Criar `typedoc.base.json` e `typedoc.json` na raiz do projeto
    - Configurar `entryPointStrategy: "packages"` e `entryPoints: ["./src/*"]`
    - _Requirements: 10.4_

  - [x] 8.3 Corrigir `mkdocs.yml` removendo a chave `paths: [.]` não suportada
    - Remover `paths: [.]` do bloco `plugins.mkdocstrings.handlers.typescript`, já que essa opção não é documentada por esse handler
    - _Requirements: 10.5_

  - [x] 8.4 Atualizar `docs/exemplos-codigo.md` com a seção "Exemplo em TypeScript"
    - Adicionar bloco de código estático com o conteúdo de `calcularMedia` (copiado de `src/calcular-media/src/index.ts`)
    - Adicionar a diretiva `::: calcular-media` com `handler: typescript`
    - Explicar a diferença entre o bloco estático e a geração via mkdocstrings, de forma análoga à explicação já existente para o exemplo em Python
    - Documentar os passos de instalação/build do toolchain Node.js/TypeDoc (`npm install`, `npx tsc`, etc.)
    - Incluir observação explícita sobre a limitação de ambiente: Node.js/npm não estão instalados nesta máquina, portanto o build dessa diretiva específica não foi validado localmente
    - _Requirements: 10.6, 10.7, 10.8, 10.9, 10.10, 10.11_

  - [x] 8.5 Tentar validar `uv run mkdocs build --strict` com a nova diretiva TypeScript
    - Executar o comando e documentar o resultado real obtido (esperado: falha ou erro relacionado à ausência de Node.js/TypeDoc ao processar a diretiva `::: calcular-media`)
    - Confirmar que as demais páginas/diretivas (Python, Playwright, etc.) continuam funcionando normalmente
    - Caso o build falhe inteiro por causa dessa única diretiva, registrar esse comportamento no design/observação da página em vez de tentar contornar artificialmente a ausência do Node.js
    - _Requirements: 10.10_

- [x] 9. Adicionar documentação de Dockerfile e outras linguagens via pymdownx.snippets
  - [x] 9.1 Adicionar a dependência `pymdown-extensions` ao `pyproject.toml`
    - Executar `uv add pymdown-extensions`, ou editar `pyproject.toml` diretamente caso `uv` não esteja disponível/confiável neste ambiente
    - _Requirements: 11.9_

  - [x] 9.2 Criar o `Dockerfile` multi-estágio na raiz do projeto
    - Criar os estágios `builder` e `runtime`, com comentário explicativo para cada instrução
    - Adaptar ao projeto real: Python 3.12 + uv, `uv sync --frozen --no-dev`, `CMD ["python", "main.py"]`
    - _Requirements: 11.1, 11.2, 11.3, 11.4_

  - [x] 9.3 Criar os 5 arquivos de exemplo em `examples/`
    - Criar `exemplo.js`, `exemplo.yaml`, `exemplo.tf`, `exemplo.sh` e `exemplo.sql`, cada um pequeno, didático e comentado, conforme o design.md (Componente 10)
    - _Requirements: 11.5, 11.6, 11.7, 11.8_

  - [x] 9.4 Atualizar `mkdocs.yml` com a 8ª entrada de `nav` e as extensões de snippets/highlight
    - Adicionar a entrada `"Dockerfile e outras linguagens": dockerfile-outras-linguagens.md` à seção `nav`, imediatamente após "Preview com Playwright"
    - Atualizar `markdown_extensions` para incluir `pymdownx.snippets` (`base_path: .`) e `pymdownx.highlight` (`anchor_linenums: true`, `line_spans: __span`, `pygments_lang_class: true`)
    - Preservar `admonition`, `pymdownx.superfences`, `pymdownx.inlinehilite` e `toc` (`permalink: true`)
    - _Requirements: 11.10, 11.11, 11.12, 11.13, 11.14_

  - [x] 9.5 Escrever `docs/dockerfile-outras-linguagens.md` (Snippets_Page, pt-BR)
    - Introduzir o motivo pelo qual não existe handler do Mkdocstrings_Plugin para essas linguagens
    - Mencionar Hadolint e Docker Buildx como práticas complementares de lint/build, sem exigir instalação ou execução
    - Explicar a sintaxe de incorporação `--8<--` da extensão `pymdownx.snippets`
    - Criar uma subseção por arquivo (Dockerfile + os 5 exemplos de `examples/`), cada uma com o bloco de incorporação real inserido na página e o destaque de sintaxe correto (`dockerfile`, `javascript`, `yaml`, `hcl`, `bash`, `sql`)
    - Explicar a diferença entre incorporação de snippet (conteúdo bruto do arquivo) e geração via mkdocstrings (documentação estruturada a partir de docstrings)
    - _Requirements: 11.15, 11.16, 11.17, 11.18, 11.19, 11.20_

  - [x] 9.6 Validar `uv run mkdocs build --strict` com a nova página e extensões
    - Confirmar que o Dockerfile e os 5 exemplos são incorporados corretamente no HTML gerado, verificando `site/dockerfile-outras-linguagens/index.html`
    - Dado que o build já está conhecidamente quebrado pela diretiva TypeScript (Tarefa 8), repetir a mesma abordagem de diagnóstico da Tarefa 8.5: testar temporariamente sem a diretiva `::: calcular-media` para isolar e confirmar que o conteúdo desta tarefa não introduz nenhum erro adicional, e então restaurar o estado original
    - _Requirements: 8.1, 8.2, 11.14_

- [x] 10. Adicionar capítulos do ecossistema MkDocs Material: imagens, diagramas, GitHub, pymdownx e outros plugins
  - [x] 10.1 Adicionar as dependências dos novos plugins ao `pyproject.toml`
    - Executar `uv add mkdocs-glightbox mkdocs-git-revision-date-localized-plugin mkdocs-macros-plugin mkdocs-redirects mkdocs-minify-plugin mkdocs-awesome-pages-plugin`
    - _Requirements: 12.1, 14.3, 16.1_

  - [x] 10.2 Remover `mkdocs-redirects` e adicionar `mkdocs-exporter` ao `pyproject.toml`
    - Executar `uv remove mkdocs-redirects` (remove também a dependência transitiva `properdocs`)
    - Executar `uv add mkdocs-exporter`
    - _Requirements: 16.4, 18.1_

  - [x] 10.3 Atualizar `mkdocs.yml` com as novas configurações do ecossistema Material
    - Adicionar `repo_url`/`repo_name`/`edit_uri` (placeholder) e `theme.features` com `content.action.edit` e `content.action.view`
    - Adicionar a opção `hooks: [hooks/redirects.py]` próxima ao topo do `mkdocs.yml`
    - Adicionar as 5 novas entradas de `nav` (após "Dockerfile e outras linguagens"): Imagens e recursos visuais, Diagramas e arquitetura, Integração com GitHub, Extensões pymdownx, Outros plugins
    - Adicionar os 6 novos plugins em `plugins`: `glightbox`; `git-revision-date-localized` com `fallback_to_build_date: true`, `enable_creation_date: true`, `type: timeago`; `macros`; `minify` com `minify_html: true`; `awesome-pages`; `exporter` configurado com `formats.pdf.enabled: true`
    - Adicionar as novas `markdown_extensions`: `attr_list`, `md_in_html`, `pymdownx.blocks.caption`, `pymdownx.tabbed` com `alternate_style: true`, `pymdownx.tasklist` com `custom_checkbox: true`, `pymdownx.details`, `pymdownx.emoji` com `emoji_index`/`emoji_generator`, e `custom_fences` do mermaid dentro de `pymdownx.superfences`
    - Conforme o design.md (Componente 1 atualizado)
    - _Requirements: 12.2, 12.5, 12.6, 13.1, 14.1, 14.2, 14.4, 15.2, 15.3, 16.2, 16.4, 16.7, 16.9, 17.2, 18.2_

  - [x] 10.4 Criar o script `hooks/redirects.py`
    - Criar o arquivo `hooks/redirects.py` na raiz do projeto, implementando um dicionário `REDIRECTS` (`{'preview.md': 'playwright-preview.md'}`) e uma função `on_post_build(config, **kwargs)` que gera um HTML de redirecionamento (`<meta http-equiv="refresh" ...>`) em `config["site_dir"]` para cada entrada, conforme o design.md (Componente 15)
    - _Requirements: 16.4, 16.5_

  - [x] 10.5 Escrever `docs/imagens-recursos-visuais.md` (Images_Page, pt-BR)
    - Explicar a finalidade do glightbox e seu comportamento sobre qualquer imagem Markdown, com observação sobre a ausência de imagem binária real no projeto
    - Incluir exemplos de `attr_list` e `pymdownx.blocks.caption`
    - Mencionar o recurso `optimize` do Material
    - _Requirements: 12.3, 12.4, 12.7, 12.8, 12.9, 12.10_

  - [x] 10.6 Escrever `docs/diagramas-arquitetura.md` (Diagrams_Page, pt-BR)
    - Explicar o `custom_fences` do mermaid dentro de `pymdownx.superfences`
    - Inserir um diagrama ```mermaid flowchart``` real na página (GitHub → GitHub Actions → Build MkDocs → GitHub Pages → Documentação publicada)
    - Mencionar conceitualmente PlantUML e Graphviz, sem exigir instalação
    - _Requirements: 13.2, 13.3, 13.4, 13.5, 13.6_

  - [x] 10.7 Escrever `docs/integracao-github.md` (GitHub_Integration_Page, pt-BR)
    - Explicar `repo_url`/`repo_name`/`edit_uri` e o Repository_Placeholder_URL, e as `theme.features` de botões de edição/visualização
    - Explicar o `git-revision-date-localized`, com observação sobre a ausência de commits locais e por que `fallback_to_build_date: true` é necessário
    - Incluir um trecho YAML ilustrativo de workflow de GitHub Actions com `fetch-depth: 0` (apenas referência conceitual)
    - _Requirements: 14.5, 14.6, 14.7, 14.8, 14.9, 14.10_

  - [x] 10.8 Escrever `docs/extensoes-pymdownx.md` (Pymdown_Extensions_Page, pt-BR)
    - Incluir tabela com as 8 extensões pymdownx relevantes
    - Incluir exemplos reais de abas (`pymdownx.tabbed`, com Python/JavaScript/PowerShell), checklist (`pymdownx.tasklist`), seção expansível (`pymdownx.details`) e emoji (`pymdownx.emoji`)
    - _Requirements: 15.1, 15.4, 15.5, 15.6, 15.7, 15.8_

  - [x] 10.9 Escrever `docs/outros-plugins.md` (Other_Plugins_Page, pt-BR)
    - Documentar `macros` (instalação, configuração, exemplo de uso)
    - Documentar a alternativa nativa via `hooks` (`Native_Redirect_Hook`), explicando por que `mkdocs-redirects` foi evitado (dependência em `properdocs`) e mostrando o script `hooks/redirects.py` real
    - Documentar `minify` com `minify_html: true`
    - Documentar `awesome-pages`, com observação honesta sobre não ter efeito com `nav` explícita neste projeto, e um exemplo de arquivo `.pages` como referência
    - Documentar o `mkdocs-exporter` (instalação, configuração `formats.pdf.enabled: true`, reaproveitamento do Playwright já instalado)
    - _Requirements: 16.3, 16.4, 16.5, 16.6, 16.7, 16.9, 18.1, 18.2, 18.3, 18.4, 18.5_

  - [x] 10.10 Validar `uv run mkdocs build --strict` com todos os novos capítulos, plugins e extensões
    - Repetir a abordagem de diagnóstico de isolamento da diretiva TypeScript (Tarefas 8.5/9.6) para confirmar que nenhum erro adicional foi introduzido pelos novos plugins/páginas
    - Verificar que `git-revision-date-localized` não quebra o build mesmo sem histórico git, graças a `fallback_to_build_date: true`
    - Verificar que o diagrama mermaid, as abas, o tasklist, os details e o emoji são renderizados corretamente no HTML gerado
    - Verificar que o redirect gerado (`site/preview/index.html`) de fato redireciona para a página real
    - Verificar que o plugin `exporter` não quebra o build e que o `hooks/redirects.py` é carregado sem erro pelo MkDocs
    - _Requirements: 8.1, 8.2, 17.1_

- [x] 11. Adicionar os componentes restantes do catálogo de extensões pymdownx
  - [x] 11.1 Atualizar `mkdocs.yml`: novas extensões pymdownx e Arithmatex/MathJax
    - Adicionar à `markdown_extensions` as extensões `abbr`, `def_list`, `footnotes`, `tables`, `pymdownx.mark`, `pymdownx.caret`, `pymdownx.tilde`, `pymdownx.keys`, `pymdownx.critic`, `pymdownx.magiclink` e `pymdownx.smartsymbols`
    - Adicionar `pymdownx.arithmatex` com `generic: true`
    - Adicionar a opção raiz `extra_javascript` apontando para `javascripts/mathjax.js` e o CDN do MathJax 3
    - _Requirements: 19.1, 19.2, 19.3, 19.4_

  - [x] 11.2 Criar o arquivo `docs/javascripts/mathjax.js`
    - Implementar a configuração `window.MathJax` conforme o design.md (Componente 1)
    - _Requirements: 19.4_

  - [x] 11.3 Estender `docs/extensoes-pymdownx.md` com as 6 novas subseções do design.md (Componente 14)
    - Distinção entre caixas de nota (`admonition`/`pymdownx.details`) e âncoras de referência (`toc.permalink`/`footnotes`)
    - Extensões de referência (`abbr`, `def_list`, `footnotes`, `tables`) com exemplos reais
    - Extensões de formatação de texto (`mark`, `caret`, `tilde`, `keys`, `critic`, `magiclink`, `smartsymbols`) com exemplos reais
    - Numeração/destaque de linhas (`linenums`/`hl_lines`)
    - Fórmulas matemáticas com Arithmatex (exemplo em bloco e em linha)
    - Observação final sobre não habilitar todas as extensões indiscriminadamente
    - _Requirements: 19.5, 19.6, 19.7, 19.8, 19.9, 19.10_

  - [x] 11.4 Validar `uv run mkdocs build --strict` com as novas extensões
    - Repetir a abordagem de diagnóstico de isolamento da diretiva TypeScript (Tarefas 8.5/9.6/10.10) para confirmar que nenhum erro adicional foi introduzido
    - Verificar no HTML gerado que `abbr`, `def_list`, `footnotes`, `tables`, `mark`, `caret`, `tilde`, `keys`, `critic`, `magiclink`, `smartsymbols`, `linenums`/`hl_lines` e a fórmula do Arithmatex são renderizados corretamente em `site/extensoes-pymdownx/index.html`
    - _Requirements: 8.1, 8.2_

- [x] 12. Configurar modos claro/escuro detalhados e integração real com GitHub Actions
  - [x] 12.1 Atualizar `mkdocs.yml`: substituir `repo_url`/`repo_name`/`edit_uri` pelos valores reais
    - Substituir os placeholders por `repo_url: https://github.com/dataRainBR/mkdocs-documentation`, `repo_name: dataRainBR/mkdocs-documentation` e `edit_uri: edit/main/docs/`
    - Conforme o design.md (Componente 1 atualizado)
    - _Requirements: 20.3_

  - [x] 12.2 Estender `docs/personalizacao.md` com a nova seção "Modos claro e escuro"
    - Explicar a detecção automática via `prefers-color-scheme`, o botão de alternância `toggle` e a persistência no `localStorage`
    - Reaproveitar o trecho real de `theme.palette` já existente no `mkdocs.yml`
    - Conforme o design.md (Componente 5 atualizado)
    - _Requirements: 20.1, 20.2_

  - [x] 12.3 Criar o arquivo real `.github/workflows/docs.yml`
    - Criar os jobs `build` e `deploy`, com checkout usando `fetch-depth: 0`, setup de Node.js/TypeScript/TypeDoc com geração do `.d.ts`, setup do `uv`, instalação do Chromium do Playwright, build `--strict` e publicação via `actions/upload-pages-artifact` + `actions/deploy-pages`
    - Conforme o design.md (Componente 16)
    - _Requirements: 20.4, 20.5, 20.6_

  - [x] 12.4 Estender `docs/integracao-github.md` com o tutorial real de CI/CD
    - Apresentar o conteúdo do `.github/workflows/docs.yml` explicado passo a passo
    - Explicar as `permissions` do workflow
    - Explicar os passos manuais de configuração no GitHub (Settings → Pages → Source → "GitHub Actions"), incluindo a nota sobre `git remote add origin` ser seguro/reversível enquanto o commit/push real é uma decisão separada do usuário
    - _Requirements: 20.7, 20.8, 20.9_

  - [x] 12.5 Validar a sintaxe YAML do workflow e o build do MkDocs com a nova configuração
    - Validar a sintaxe YAML do `.github/workflows/docs.yml` carregando-o com um parser YAML
    - Executar `uv run mkdocs build --strict` com a nova configuração de `repo_url`/`repo_name`/`edit_uri`
    - Repetir a abordagem de diagnóstico de isolamento da diretiva TypeScript (Tarefas 8.5/9.6/10.10/11.4) para confirmar que nenhum erro adicional foi introduzido
    - _Requirements: 8.1, 8.2_

## Notes

- Tasks marcadas com `*` são opcionais (testes) e podem ser puladas para um MVP mais rápido, mas recomenda-se executá-las para validar as Properties 1 e 2 do design.
- Cada tarefa referencia os critérios de aceitação granulares do `requirements.md`.
- Os checkpoints garantem validação incremental antes de avançar.
- As dependências `mkdocs`, `mkdocs-material`, `mkdocstrings[python]` e `mkdocstrings-typescript` já estão declaradas em `pyproject.toml`; a Tarefa 3.2 documenta o comando de instalação para o leitor do tutorial, não para o ambiente de desenvolvimento em si.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "2.1"] },
    { "id": 1, "tasks": ["3.1", "3.2", "3.3", "3.4", "3.5", "3.7"] },
    { "id": 2, "tasks": ["3.6"] },
    { "id": 3, "tasks": ["5.1"] },
    { "id": 4, "tasks": ["5.2", "5.3"] },
    { "id": 5, "tasks": ["7.1", "7.2"] },
    { "id": 6, "tasks": ["7.3"] },
    { "id": 7, "tasks": ["8.1", "8.2", "8.3"] },
    { "id": 8, "tasks": ["8.4"] },
    { "id": 9, "tasks": ["8.5"] },
    { "id": 10, "tasks": ["9.1", "9.2", "9.3", "9.4"] },
    { "id": 11, "tasks": ["9.5"] },
    { "id": 12, "tasks": ["9.6"] },
    { "id": 13, "tasks": ["10.1"] },
    { "id": 14, "tasks": ["10.2"] },
    { "id": 15, "tasks": ["10.3", "10.4"] },
    { "id": 16, "tasks": ["10.5", "10.6", "10.7", "10.8", "10.9"] },
    { "id": 17, "tasks": ["10.10"] },
    { "id": 18, "tasks": ["11.1", "11.2"] },
    { "id": 19, "tasks": ["11.3"] },
    { "id": 20, "tasks": ["11.4"] },
    { "id": 21, "tasks": ["12.1", "12.2", "12.3"] },
    { "id": 22, "tasks": ["12.4"] },
    { "id": 23, "tasks": ["12.5"] }
  ]
}
```
