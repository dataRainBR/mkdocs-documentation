# Requirements Document

## Introduction

Esta funcionalidade cria a documentação do projeto usando MkDocs, com um tutorial em português (pt-BR) sobre instalação dos pacotes MkDocs, configuração do arquivo `mkdocs.yml` e customização visual do tema Material. A documentação é composta por múltiplas páginas organizadas em um menu de navegação (`nav`), inclui exemplos de código extraídos de `teste.py` (documentado via docstring e consumido tanto como bloco de código quanto via mkdocstrings) e uma página de exemplos que reflete o roteiro de seções presente em `mkdocks.ipynb`. O resultado final é um site MkDocs funcional, construído a partir de um `mkdocs.yml` real na raiz do projeto e de uma pasta `docs/` com o conteúdo das páginas, pronto para ser processado pelos comandos `mkdocs build` e `mkdocs serve`.

## Glossary

- **Documentation_Site**: O site estático gerado pelo MkDocs a partir do arquivo `mkdocs.yml` e da pasta `docs/` do projeto.
- **Mkdocs_Config_File**: O arquivo `mkdocs.yml` localizado na raiz do projeto, que define título, tema, plugins, extensões Markdown e a estrutura de navegação do Documentation_Site.
- **Docs_Directory**: A pasta `docs/` na raiz do projeto, contendo os arquivos Markdown de cada página do tutorial e os recursos estáticos (imagens, fontes, favicon).
- **Installation_Page**: A página do tutorial que descreve a instalação dos pacotes `mkdocs`, `mkdocs-material`, `mkdocstrings[python]` e `mkdocstrings-typescript`.
- **Configuration_Page**: A página do tutorial que explica os componentes principais do Mkdocs_Config_File (`nav`, `theme`, `plugins`, `markdown_extensions`).
- **Customization_Page**: A página do tutorial que explica como personalizar fontes, cores/paleta do tema Material e logo/imagens do Documentation_Site.
- **Code_Examples_Page**: A página do tutorial que demonstra o uso da função `calcular_media` de `teste.py` como bloco de código e via mkdocstrings.
- **Notebook_Examples_Page**: A página do tutorial que reflete, em texto explicativo próprio, o roteiro de seções presente em `mkdocks.ipynb`.
- **Mkdocstrings_Plugin**: O plugin MkDocs responsável por gerar documentação de código a partir de docstrings, configurado no Mkdocs_Config_File para os handlers Python e TypeScript.
- **Tutorial_Pages**: O conjunto formado por Installation_Page, Configuration_Page, Customization_Page, Code_Examples_Page e Notebook_Examples_Page.
- **Preview_Script**: O script `docs_preview.py` localizado na raiz do projeto, responsável por buildar o Documentation_Site e abri-lo em um navegador via Playwright_Package.
- **Playwright_Package**: O pacote Python `playwright`, utilizado pelo Preview_Script como ferramenta de automação de navegador para abrir o Documentation_Site já buildado.
- **Preview_Page**: A página do tutorial que documenta o Preview_Script e o Playwright_Package, incluindo instalação, finalidade, documentação das funções do Preview_Script e forma de execução.
- **TypeScript_Example_Package**: O pacote TypeScript de exemplo, equivalente em comportamento à função `calcular_media` de `teste.py`, contendo os arquivos `package.json`, `tsconfig.json`, `typedoc.json` e `src/index.ts` com a função `calcularMedia` documentada via JSDoc.
- **TypeDoc_Toolchain**: O conjunto de ferramentas Node.js — npm, o pacote TypeDoc e o compilador TypeScript (`tsc`) — necessário para instalar dependências, gerar os arquivos de declaração (`.d.ts`) do TypeScript_Example_Package e permitir que o handler `typescript` do Mkdocstrings_Plugin extraia sua documentação.
- **Typedoc_Root_Config**: Os arquivos `typedoc.base.json` e `typedoc.json` localizados na raiz do projeto, responsáveis por configurar o TypeDoc_Toolchain no modo `entryPointStrategy: "packages"` para descobrir o TypeScript_Example_Package dentro de `src/*`.
- **Pymdown_Extensions_Package**: O pacote Python `pymdown-extensions`, adicionado às dependências do Project_Manifest através do comando `uv add pymdown-extensions`, responsável por fornecer a extensão Markdown `pymdownx.snippets`.
- **Project_Manifest**: O arquivo `pyproject.toml` localizado na raiz do projeto, que declara as dependências Python do projeto, incluindo o Pymdown_Extensions_Package.
- **Dockerfile_Example**: O arquivo `Dockerfile` localizado na raiz do projeto, contendo múltiplos estágios de build (`builder` e `runtime`) e comentários explicativos para cada instrução, compatível com o projeto Python/uv existente.
- **Multi_Language_Examples**: O conjunto de cinco arquivos de exemplo reais, localizados no diretório `examples/` na raiz do projeto, um para cada uma das linguagens JavaScript, YAML, Terraform, Shell e SQL.
- **Snippets_Page**: A página do tutorial que explica a técnica de incorporação de arquivos reais do projeto em páginas Markdown através da extensão `pymdownx.snippets` e da sintaxe `--8<--`, incluindo o Dockerfile_Example e os Multi_Language_Examples incorporados de verdade na página.
- **Images_Page**: A página do tutorial (`docs/imagens-recursos-visuais.md`) que explica lightbox, legendas e otimização de imagens do Documentation_Site.
- **Diagrams_Page**: A página do tutorial (`docs/diagramas-arquitetura.md`) que explica a renderização nativa de diagramas Mermaid e menciona PlantUML e Graphviz como alternativas conceituais.
- **GitHub_Integration_Page**: A página do tutorial (`docs/integracao-github.md`) que explica a integração do Documentation_Site com um repositório GitHub, incluindo ações de edição/visualização de página e data de revisão.
- **Pymdown_Extensions_Page**: A página do tutorial (`docs/extensoes-pymdownx.md`) que cataloga as extensões do Pymdown_Extensions_Package relevantes para código e documentação técnica.
- **Other_Plugins_Page**: A página do tutorial (`docs/outros-plugins.md`) que documenta o Macros_Plugin, o Native_Redirect_Hook, o Minify_Plugin, o Awesome_Pages_Plugin e o Exporter_Plugin.
- **Ecosystem_Pages**: O conjunto formado por Images_Page, Diagrams_Page, GitHub_Integration_Page, Pymdown_Extensions_Page e Other_Plugins_Page.
- **Glightbox_Plugin**: O plugin MkDocs `mkdocs-glightbox`, responsável por adicionar comportamento de lightbox (zoom em tela cheia) às imagens do Documentation_Site.
- **Repository_Placeholder_URL**: A URL de exemplo `https://github.com/seu-usuario/teste-mkdocks`, utilizada como valor placeholder nos campos `repo_url` e `edit_uri` do Mkdocs_Config_File, a ser substituída pelo leitor pela URL real de seu próprio repositório antes de publicar o Documentation_Site.
- **Git_Revision_Date_Plugin**: O plugin MkDocs `mkdocs-git-revision-date-localized-plugin`, responsável por exibir a data de última revisão e de criação de cada página do Documentation_Site a partir do histórico git do repositório.
- **Macros_Plugin**: O plugin MkDocs `mkdocs-macros-plugin`, responsável por permitir o uso de variáveis e macros Jinja2 reutilizáveis dentro das páginas Markdown do Documentation_Site.
- **Native_Redirect_Hook**: Um script Python local (`hooks/redirects.py`), referenciado na opção `hooks` do Mkdocs_Config_File, responsável por gerar páginas de redirecionamento entre um caminho antigo e um caminho atual do Documentation_Site durante o evento `on_post_build`, sem depender de nenhum pacote adicional do PyPI.
- **Minify_Plugin**: O plugin MkDocs `mkdocs-minify-plugin`, responsável por minificar o HTML gerado para cada página do Documentation_Site.
- **Awesome_Pages_Plugin**: O plugin MkDocs `mkdocs-awesome-pages-plugin`, responsável por permitir configuração de navegação por pasta através de arquivos `.pages`, sem efeito sobre uma seção `nav` definida explicitamente no Mkdocs_Config_File.
- **Exporter_Plugin**: O plugin MkDocs `mkdocs-exporter` (pacote Python instalado via `uv add mkdocs-exporter`), configurado na seção `plugins` do Mkdocs_Config_File com a opção `formats.pdf.enabled` igual a `true`, responsável por exportar páginas do Documentation_Site para PDF através de um navegador headless, reaproveitando o Playwright_Package já instalado no projeto.
- **Reference_Extensions**: O conjunto formado pelas extensões nativas do Python-Markdown `abbr`, `def_list`, `footnotes` e `tables`, responsáveis, respectivamente, por abreviações com tooltip, listas de definição, notas de rodapé com âncora de ida-e-volta e tabelas Markdown.
- **Text_Formatting_Extensions**: O conjunto formado pelas extensões `pymdownx.mark`, `pymdownx.caret`, `pymdownx.tilde`, `pymdownx.keys`, `pymdownx.critic`, `pymdownx.magiclink` e `pymdownx.smartsymbols`, responsáveis, respectivamente, por destaque de texto, sobrescrito e sublinhado, subscrito e tachado, representação visual de combinações de teclas, marcação de revisões (inserções e exclusões), conversão automática de URLs soltas em links clicáveis e conversão de sequências de caracteres em símbolos tipográficos.
- **Arithmatex_Extension**: A extensão `pymdownx.arithmatex`, configurada no Mkdocs_Config_File com a opção `generic` igual a `true`, responsável por preparar o HTML de fórmulas matemáticas escritas em notação LaTeX para renderização por um motor de exibição matemática no navegador.
- **Mathjax_Frontend_Scripts**: Os arquivos JavaScript do MathJax referenciados na opção `extra_javascript` do Mkdocs_Config_File, necessários para que o Documentation_Site renderize visualmente, no navegador, as fórmulas preparadas pela Arithmatex_Extension.
- **Real_Repository_URL**: O endereço real do repositório GitHub do projeto, `https://github.com/dataRainBR/mkdocs-documentation`, com branch padrão `main`, utilizado a partir do Requirement 20 para substituir o Repository_Placeholder_URL definido no Requirement 14 nos campos `repo_url`, `repo_name` e `edit_uri` do Mkdocs_Config_File.
- **GitHub_Actions_Workflow**: O arquivo real de workflow do GitHub Actions, localizado em `.github/workflows/` na raiz do projeto, responsável por buildar o Documentation_Site com o gerenciador `uv` e publicá-lo no GitHub Pages através da abordagem oficial de artefato e deploy (`actions/upload-pages-artifact` e `actions/deploy-pages`).

## Requirements

### Requirement 1: Estrutura de pastas e arquivos da documentação

**User Story:** Como desenvolvedor do projeto, eu quero uma pasta `docs/` com múltiplas páginas Markdown organizadas, para que o tutorial seja navegável e fácil de manter.

#### Acceptance Criteria

1. THE Docs_Directory SHALL existir na raiz do projeto.
2. THE Docs_Directory SHALL conter um arquivo Markdown separado para cada uma das Tutorial_Pages.
3. THE Docs_Directory SHALL conter uma página inicial (`index.md`) com a visão geral do tutorial e links para as Tutorial_Pages.
4. WHERE recursos estáticos de personalização (imagens, logo, favicon) são referenciados pela Customization_Page, THE Docs_Directory SHALL conter uma subpasta `assets/` destinada a esses recursos.

### Requirement 2: Arquivo de configuração mkdocs.yml

**User Story:** Como desenvolvedor do projeto, eu quero um `mkdocs.yml` completo na raiz do projeto, para que o Documentation_Site seja gerado a partir de uma configuração real e funcional.

#### Acceptance Criteria

1. THE Mkdocs_Config_File SHALL existir na raiz do projeto.
2. THE Mkdocs_Config_File SHALL definir a seção `theme` com o tema `material`.
3. THE Mkdocs_Config_File SHALL definir a seção `nav` listando a página inicial e cada uma das Tutorial_Pages na ordem: instalação, configuração do `mkdocs.yml`, personalização, exemplos de código e exemplos do notebook.
4. THE Mkdocs_Config_File SHALL definir a seção `plugins` incluindo o Mkdocstrings_Plugin configurado com o handler `python`.
5. THE Mkdocs_Config_File SHALL definir, dentro da seção `plugins`, a configuração do Mkdocstrings_Plugin para o handler `typescript`.
6. THE Mkdocs_Config_File SHALL definir a seção `markdown_extensions` com as extensões necessárias para renderizar blocos de código com destaque de sintaxe (ex.: `pymdownx.highlight`, `pymdownx.superfences`).
7. THE Mkdocs_Config_File SHALL referenciar o Docs_Directory como diretório de origem do conteúdo do Documentation_Site.
8. WHERE a Customization_Page descreve customização de paleta de cores, THE Mkdocs_Config_File SHALL conter, na seção `theme`, a configuração de `palette` com ao menos uma variante de cor do mkdocs-material.
9. WHERE a Customization_Page descreve customização de logo, THE Mkdocs_Config_File SHALL conter, na seção `theme`, o campo `logo` apontando para um caminho dentro de `docs/assets/`.

### Requirement 3: Conteúdo da página de instalação

**User Story:** Como leitor da documentação, eu quero uma página que explique como instalar os pacotes do MkDocs, para que eu consiga preparar o ambiente do projeto.

#### Acceptance Criteria

1. THE Installation_Page SHALL descrever o comando de instalação do pacote `mkdocs`.
2. THE Installation_Page SHALL descrever o comando de instalação do pacote `mkdocs-material`.
3. THE Installation_Page SHALL descrever o comando de instalação do pacote `mkdocstrings` com o extra `python`.
4. THE Installation_Page SHALL descrever o comando de instalação do pacote `mkdocstrings-typescript`.
5. THE Installation_Page SHALL estar escrita em português (pt-BR).

### Requirement 4: Conteúdo da página de configuração do mkdocs.yml

**User Story:** Como leitor da documentação, eu quero uma página que explique os principais componentes do `mkdocs.yml`, para que eu entenda como configurar meu próprio site MkDocs.

#### Acceptance Criteria

1. THE Configuration_Page SHALL explicar a finalidade da seção `nav` do Mkdocs_Config_File.
2. THE Configuration_Page SHALL explicar a finalidade da seção `theme` do Mkdocs_Config_File.
3. THE Configuration_Page SHALL explicar a finalidade da seção `plugins` do Mkdocs_Config_File, incluindo o Mkdocstrings_Plugin para os handlers Python e TypeScript.
4. THE Configuration_Page SHALL explicar a finalidade da seção `markdown_extensions` do Mkdocs_Config_File.
5. THE Configuration_Page SHALL estar escrita em português (pt-BR).

### Requirement 5: Conteúdo da página de personalização

**User Story:** Como leitor da documentação, eu quero uma página que explique como personalizar a aparência do site, para que eu consiga adaptar fontes, cores e identidade visual ao meu projeto.

#### Acceptance Criteria

1. THE Customization_Page SHALL explicar como configurar fontes personalizadas através da seção `theme.font` do Mkdocs_Config_File.
2. THE Customization_Page SHALL explicar como configurar a paleta de cores do tema Material através da seção `theme.palette` do Mkdocs_Config_File.
3. THE Customization_Page SHALL explicar como adicionar um logo ao Documentation_Site através do campo `theme.logo` do Mkdocs_Config_File.
4. THE Customization_Page SHALL explicar como adicionar um favicon ao Documentation_Site através do campo `theme.favicon` do Mkdocs_Config_File.
5. THE Customization_Page SHALL indicar `docs/assets/` como o local recomendado para armazenar imagens, logo e favicon.
6. IF nenhum arquivo de imagem real estiver disponível no projeto, THEN THE Customization_Page SHALL indicar essa ausência através de uma observação textual, sem exigir a criação de um arquivo binário de imagem.

### Requirement 6: Conteúdo da página de exemplos de código

**User Story:** Como leitor da documentação, eu quero ver exemplos de código a partir de `teste.py`, para que eu entenda como o mkdocstrings documenta funções Python automaticamente.

#### Acceptance Criteria

1. THE Code_Examples_Page SHALL exibir o código-fonte da função `calcular_media` como um bloco de código Markdown.
2. THE Code_Examples_Page SHALL exibir a documentação da função `calcular_media` gerada via uma diretiva do Mkdocstrings_Plugin referenciando `teste.calcular_media`.
3. THE Code_Examples_Page SHALL explicar a diferença entre apresentar um bloco de código estático e usar o Mkdocstrings_Plugin para gerar documentação a partir de docstrings.
4. THE Code_Examples_Page SHALL estar escrita em português (pt-BR).

### Requirement 7: Conteúdo da página de exemplos do notebook

**User Story:** Como leitor da documentação, eu quero uma página que reflita o roteiro de `mkdocks.ipynb`, para que eu tenha uma visão sequencial de instalação, inicialização, build e visualização do site.

#### Acceptance Criteria

1. THE Notebook_Examples_Page SHALL apresentar, em texto explicativo próprio, as etapas correspondentes às seções de `mkdocks.ipynb`: instalação, inicialização do projeto, build, configuração do `mkdocs.yml`, personalizações e visualização no navegador.
2. THE Notebook_Examples_Page SHALL apresentar cada etapa com o respectivo comando de terminal, quando aplicável.
3. THE Notebook_Examples_Page SHALL estar escrita em português (pt-BR).

### Requirement 8: Build funcional do site de documentação

**User Story:** Como desenvolvedor do projeto, eu quero que o site MkDocs seja gerado sem erros, para que a documentação criada esteja efetivamente disponível e consumível.

#### Acceptance Criteria

1. WHEN o comando `mkdocs build` é executado na raiz do projeto, THE Documentation_Site SHALL ser gerado sem erros de configuração.
2. WHEN o Documentation_Site é gerado, THE Documentation_Site SHALL incluir uma página renderizada para cada entrada definida na seção `nav` do Mkdocs_Config_File.
3. IF a geração do Documentation_Site falhar devido a uma referência inválida do Mkdocstrings_Plugin a `teste.calcular_media`, THEN THE Mkdocs_Config_File SHALL ser ajustado para que o caminho do módulo seja resolvido corretamente a partir da raiz do projeto.

### Requirement 9: Conteúdo da página de preview com Playwright

**User Story:** Como leitor da documentação, eu quero uma página que explique o Preview_Script e o Playwright_Package, para que eu entenda como pré-visualizar o Documentation_Site localmente no navegador.

#### Acceptance Criteria

1. THE Preview_Page SHALL descrever o comando `uv add playwright` para adicionar o Playwright_Package às dependências do projeto.
2. THE Preview_Page SHALL descrever o comando `uv run playwright install chromium` para instalação do navegador Chromium utilizado pelo Playwright_Package.
3. THE Preview_Page SHALL explicar a finalidade do Playwright_Package e o motivo de seu uso no Preview_Script como ferramenta de automação de navegador para abrir o Documentation_Site já buildado.
4. THE Preview_Page SHALL exibir a documentação das funções `run_mkdocs_build`, `find_free_port`, `start_local_server`, `ensure_playwright_browser_installed`, `open_in_browser` e `main` do Preview_Script, gerada via uma diretiva do Mkdocstrings_Plugin referenciando o módulo `docs_preview`.
5. THE Preview_Page SHALL descrever o comando `uv run docs_preview.py` como forma de executar o Preview_Script.
6. THE Preview_Page SHALL estar escrita em português (pt-BR).
7. WHEN o Documentation_Site é gerado, THE Documentation_Site SHALL incluir a Preview_Page acessível através da seção `nav` do Mkdocs_Config_File.

### Requirement 10: Exemplo real de TypeScript documentado via mkdocstrings-typescript

**User Story:** Como leitor da documentação, eu quero ver um exemplo real de pacote TypeScript documentado através da integração completa do handler `typescript` do Mkdocstrings_Plugin com o TypeDoc_Toolchain, para que eu entenda como configurar e usar essa integração em meu próprio projeto.

#### Acceptance Criteria

1. THE TypeScript_Example_Package SHALL conter um arquivo `src/index.ts` que declara a função `calcularMedia`, equivalente em comportamento à função `calcular_media` de `teste.py`.
2. THE TypeScript_Example_Package SHALL documentar, via comentário JSDoc na função `calcularMedia`, o parâmetro recebido, o valor de retorno e o erro lançado quando a lista recebida estiver vazia.
3. THE TypeScript_Example_Package SHALL conter os arquivos `package.json`, `tsconfig.json` e `typedoc.json` necessários para que o TypeDoc_Toolchain processe o TypeScript_Example_Package no modo `entryPointStrategy: "expand"`.
4. THE Typedoc_Root_Config SHALL conter os arquivos `typedoc.base.json` e `typedoc.json` na raiz do projeto, configurados com `entryPointStrategy: "packages"` e `entryPoints: ["./src/*"]` para descobrir o TypeScript_Example_Package.
5. THE Mkdocs_Config_File SHALL definir, dentro da seção `plugins.mkdocstrings.handlers.typescript`, apenas opções documentadas pelo handler `typescript`, removendo a opção `paths` configurada anteriormente para esse handler.
6. THE Code_Examples_Page SHALL exibir o código-fonte da função `calcularMedia` como um bloco de código Markdown, na mesma página em que o exemplo equivalente em Python é apresentado.
7. THE Code_Examples_Page SHALL exibir a documentação da função `calcularMedia` gerada via uma diretiva do Mkdocstrings_Plugin que referencia o TypeScript_Example_Package com o handler `typescript`.
8. THE Code_Examples_Page SHALL explicar a diferença entre apresentar o bloco de código estático da função `calcularMedia` e usar o Mkdocstrings_Plugin para gerar sua documentação a partir do TypeScript_Example_Package, de forma equivalente à explicação já feita para o exemplo em Python.
9. THE Code_Examples_Page SHALL descrever os passos de instalação e build do TypeDoc_Toolchain — incluindo `npm install`, a instalação do TypeDoc e a geração dos arquivos de declaração (`.d.ts`) via `tsc` — como pré-requisito para que a diretiva do Mkdocstrings_Plugin referenciando o TypeScript_Example_Package funcione.
10. IF o ambiente onde a Documentation_Site é construída não possuir o TypeDoc_Toolchain instalado, THEN THE Code_Examples_Page SHALL registrar uma observação explícita informando que a renderização dessa diretiva específica não pôde ser validada por um build local nesse ambiente, devendo ser validada pelo leitor em um ambiente com Node.js instalado.
11. THE Code_Examples_Page SHALL estar escrita em português (pt-BR).

### Requirement 11: Documentação de Dockerfile e outras linguagens via incorporação de snippets

**User Story:** Como leitor da documentação, eu quero uma página que explique como documentar um Dockerfile e outras linguagens sem handler do Mkdocstrings_Plugin através da incorporação de arquivos reais do projeto, para que eu entenda como manter exemplos de código sincronizados com os arquivos reais sem copiar e colar manualmente seu conteúdo.

#### Acceptance Criteria

1. THE Dockerfile_Example SHALL conter ao menos dois estágios de build nomeados `builder` e `runtime`.
2. THE Dockerfile_Example SHALL conter, para cada instrução de cada estágio, um comentário explicativo descrevendo o propósito dessa instrução.
3. THE Dockerfile_Example SHALL ser compatível com a estrutura do projeto Python gerenciado por uv, referenciando os arquivos `pyproject.toml` e `uv.lock` existentes na raiz do projeto.
4. THE Multi_Language_Examples SHALL conter um arquivo com extensão `.js` exemplificando código JavaScript.
5. THE Multi_Language_Examples SHALL conter um arquivo com extensão `.yaml` exemplificando configuração YAML.
6. THE Multi_Language_Examples SHALL conter um arquivo com extensão `.tf` exemplificando código Terraform.
7. THE Multi_Language_Examples SHALL conter um arquivo com extensão `.sh` exemplificando script Shell.
8. THE Multi_Language_Examples SHALL conter um arquivo com extensão `.sql` exemplificando código SQL.
9. THE Project_Manifest SHALL declarar o Pymdown_Extensions_Package como dependência do projeto.
10. THE Mkdocs_Config_File SHALL definir, na seção `markdown_extensions`, a extensão `pymdownx.snippets` configurada com a opção `base_path` igual a `.`.
11. THE Mkdocs_Config_File SHALL definir, na seção `markdown_extensions`, a extensão `pymdownx.superfences`.
12. THE Mkdocs_Config_File SHALL definir, na seção `markdown_extensions`, a extensão `pymdownx.highlight` configurada com as opções `anchor_linenums` igual a `true`, `line_spans` igual a `__span` e `pygments_lang_class` igual a `true`.
13. THE Mkdocs_Config_File SHALL manter, na seção `markdown_extensions`, as extensões `admonition`, `pymdownx.inlinehilite` e `toc` configurada com a opção `permalink` igual a `true`.
14. THE Mkdocs_Config_File SHALL definir a seção `nav` incluindo uma entrada para a Snippets_Page.
15. THE Snippets_Page SHALL explicar o motivo pelo qual não existe um handler do Mkdocstrings_Plugin para Dockerfile e para as linguagens dos Multi_Language_Examples.
16. THE Snippets_Page SHALL mencionar Hadolint e Docker Buildx como práticas complementares recomendadas para lint e validação de build de um Dockerfile, sem exigir a instalação ou execução dessas ferramentas.
17. THE Snippets_Page SHALL incorporar o conteúdo real do Dockerfile_Example através de um bloco de código com a sintaxe `--8<--` da extensão `pymdownx.snippets` e com destaque de sintaxe da linguagem `dockerfile`.
18. THE Snippets_Page SHALL incorporar o conteúdo real de cada um dos Multi_Language_Examples através de um bloco de código com a sintaxe `--8<--` da extensão `pymdownx.snippets`, com destaque de sintaxe `javascript` para o arquivo `.js`, `yaml` para o arquivo `.yaml`, `hcl` para o arquivo `.tf`, `bash` para o arquivo `.sh` e `sql` para o arquivo `.sql`.
19. THE Snippets_Page SHALL explicar que a incorporação via `pymdownx.snippets` referencia o conteúdo bruto do arquivo original, em contraste com o Mkdocstrings_Plugin, que extrai documentação estruturada a partir de docstrings.
20. THE Snippets_Page SHALL estar escrita em português (pt-BR).

### Requirement 12: Conteúdo da página de imagens e recursos visuais

**User Story:** Como leitor da documentação, eu quero uma página que explique lightbox, legendas e otimização de imagens, para que eu saiba como enriquecer imagens no meu próprio site MkDocs.

#### Acceptance Criteria

1. THE Project_Manifest SHALL declarar o Glightbox_Plugin como dependência do projeto.
2. THE Mkdocs_Config_File SHALL definir, na seção `plugins`, o Glightbox_Plugin.
3. THE Images_Page SHALL explicar a finalidade do Glightbox_Plugin como mecanismo de lightbox (zoom em tela cheia) para imagens do Documentation_Site.
4. IF nenhum arquivo de imagem binário real estiver disponível no projeto para demonstrar o Glightbox_Plugin, THEN THE Images_Page SHALL registrar essa ausência através de uma observação textual equivalente à adotada pela Customization_Page, explicando o comportamento do Glightbox_Plugin sobre qualquer imagem Markdown da página.
5. THE Mkdocs_Config_File SHALL definir, na seção `markdown_extensions`, as extensões `attr_list` e `md_in_html`.
6. THE Mkdocs_Config_File SHALL definir, na seção `markdown_extensions`, a extensão `pymdownx.blocks.caption`.
7. THE Images_Page SHALL apresentar um exemplo de sintaxe Markdown que utiliza `attr_list` para alinhar ou dimensionar uma imagem.
8. THE Images_Page SHALL apresentar um exemplo de sintaxe Markdown que utiliza `pymdownx.blocks.caption` para adicionar uma legenda a uma imagem.
9. THE Images_Page SHALL mencionar o recurso `optimize` do tema `material` como mecanismo nativo de otimização de imagens do Documentation_Site.
10. THE Images_Page SHALL estar escrita em português (pt-BR).

### Requirement 13: Conteúdo da página de diagramas e arquitetura

**User Story:** Como leitor da documentação, eu quero uma página que explique a renderização de diagramas Mermaid, para que eu entenda como documentar arquitetura e fluxos sem instalar ferramentas externas.

#### Acceptance Criteria

1. THE Mkdocs_Config_File SHALL definir, na seção `markdown_extensions`, a extensão `pymdownx.superfences` configurada com a opção `custom_fences` associando o formato `mermaid` à classe `mermaid`.
2. THE Diagrams_Page SHALL apresentar ao menos um bloco de código com a cerca ```mermaid``` renderizado como um diagrama `flowchart` pelo Documentation_Site.
3. THE Diagrams_Page SHALL explicar a configuração `custom_fences` do Mkdocs_Config_File necessária para que o Documentation_Site renderize diagramas Mermaid nativamente.
4. THE Diagrams_Page SHALL mencionar PlantUML e Graphviz como alternativas conceituais para diagramas UML e grafos, respectivamente.
5. THE Diagrams_Page SHALL indicar que PlantUML e Graphviz exigem, respectivamente, um binário Java e um binário externo não instalados pelo Project_Manifest, apresentando-os apenas como referência conceitual sem exigir sua instalação.
6. THE Diagrams_Page SHALL estar escrita em português (pt-BR).

### Requirement 14: Conteúdo da página de integração com GitHub

**User Story:** Como leitor da documentação, eu quero uma página que explique a integração do site com um repositório GitHub, para que eu saiba como habilitar ações de edição de página e datas de revisão no meu próprio projeto.

#### Acceptance Criteria

1. THE Mkdocs_Config_File SHALL definir os campos `repo_url`, `repo_name` e `edit_uri` utilizando o Repository_Placeholder_URL.
2. THE Mkdocs_Config_File SHALL definir, na seção `theme.features`, as entradas `content.action.edit` e `content.action.view`.
3. THE Project_Manifest SHALL declarar o Git_Revision_Date_Plugin como dependência do projeto.
4. THE Mkdocs_Config_File SHALL definir, na seção `plugins`, o Git_Revision_Date_Plugin configurado com as opções `fallback_to_build_date` igual a `true`, `enable_creation_date` igual a `true` e `type` igual a `timeago`.
5. THE GitHub_Integration_Page SHALL explicar que o repositório local do projeto não possui nenhum commit, e que, por esse motivo, a opção `fallback_to_build_date` evita que o Git_Revision_Date_Plugin interrompa a geração do Documentation_Site por ausência de histórico git.
6. THE GitHub_Integration_Page SHALL explicar o significado do Repository_Placeholder_URL, instruindo o leitor a substituí-lo pela URL real de seu próprio repositório antes de publicar o Documentation_Site.
7. THE GitHub_Integration_Page SHALL explicar a finalidade das entradas `content.action.edit` e `content.action.view` como links de edição e de visualização de cada página no repositório remoto.
8. THE GitHub_Integration_Page SHALL descrever a opção `fetch-depth: 0` na etapa de checkout de um workflow de GitHub Actions como prática necessária para que o Git_Revision_Date_Plugin tenha acesso ao histórico completo de commits durante um build em integração contínua.
9. THE GitHub_Integration_Page SHALL indicar que a configuração de GitHub Actions é apresentada apenas como referência conceitual, sem exigir a criação de um arquivo de workflow executável neste projeto.
10. THE GitHub_Integration_Page SHALL estar escrita em português (pt-BR).

### Requirement 15: Conteúdo da página de extensões pymdownx para código e documentação técnica

**User Story:** Como leitor da documentação, eu quero uma página que catalogue as extensões `pymdown-extensions` voltadas para código, para que eu saiba quais extensões usar e como aplicá-las em minha própria documentação técnica.

#### Acceptance Criteria

1. THE Pymdown_Extensions_Page SHALL apresentar uma tabela listando as extensões `pymdownx.highlight`, `pymdownx.superfences`, `pymdownx.snippets`, `pymdownx.tabbed`, `pymdownx.inlinehilite`, `pymdownx.tasklist`, `pymdownx.details` e `pymdownx.emoji`, com uma descrição de finalidade para cada uma.
2. THE Mkdocs_Config_File SHALL definir, na seção `markdown_extensions`, a extensão `pymdownx.tabbed` configurada com a opção `alternate_style` igual a `true`.
3. THE Mkdocs_Config_File SHALL definir, na seção `markdown_extensions`, as extensões `pymdownx.tasklist`, `pymdownx.details` e `pymdownx.emoji`.
4. THE Pymdown_Extensions_Page SHALL apresentar um exemplo de sintaxe Markdown com abas `=== "Python"`, `=== "JavaScript"` e `=== "PowerShell"` renderizado através da extensão `pymdownx.tabbed`.
5. THE Pymdown_Extensions_Page SHALL apresentar um exemplo de checklist renderizado através da extensão `pymdownx.tasklist`.
6. THE Pymdown_Extensions_Page SHALL apresentar um exemplo de seção expansível renderizado através da extensão `pymdownx.details`.
7. THE Pymdown_Extensions_Page SHALL apresentar um exemplo de emoji renderizado através da extensão `pymdownx.emoji`.
8. THE Pymdown_Extensions_Page SHALL estar escrita em português (pt-BR).

### Requirement 16: Conteúdo da página de outros plugins do ecossistema MkDocs Material

**User Story:** Como leitor da documentação, eu quero uma página que documente plugins complementares do ecossistema MkDocs Material, para que eu saiba como usar macros, redirecionamentos, minificação e organização de navegação em meu próprio projeto.

#### Acceptance Criteria

1. THE Project_Manifest SHALL declarar o Macros_Plugin, o Minify_Plugin e o Awesome_Pages_Plugin como dependências do projeto.
2. THE Mkdocs_Config_File SHALL definir, na seção `plugins`, o Macros_Plugin.
3. THE Other_Plugins_Page SHALL explicar a finalidade do Macros_Plugin como mecanismo de variáveis e macros Jinja2 reutilizáveis dentro das páginas Markdown do Documentation_Site, com um exemplo de uso.
4. THE Mkdocs_Config_File SHALL definir a opção `hooks` referenciando um script Python local (`hooks/redirects.py`) que implementa o Native_Redirect_Hook.
5. THE Native_Redirect_Hook SHALL gerar, durante o evento `on_post_build`, uma página HTML de redirecionamento para ao menos um mapeamento de um caminho de página antiga hipotética para o caminho de uma página real existente do Documentation_Site (ex.: `preview.md` para `playwright-preview.md`).
6. THE Other_Plugins_Page SHALL explicar a finalidade do Native_Redirect_Hook e o motivo pelo qual ele foi escolhido em vez do pacote `mkdocs-redirects`, evitando a dependência transitiva no pacote `properdocs`, apresentando o mapeamento implementado.
7. THE Mkdocs_Config_File SHALL definir, na seção `plugins`, o Minify_Plugin configurado com a opção `minify_html` igual a `true`.
8. THE Other_Plugins_Page SHALL explicar a finalidade do Minify_Plugin como mecanismo de minificação do HTML gerado pelo Documentation_Site.
9. THE Mkdocs_Config_File SHALL definir, na seção `plugins`, o Awesome_Pages_Plugin.
10. THE Other_Plugins_Page SHALL explicar que o Awesome_Pages_Plugin não altera a ordem de navegação do Documentation_Site enquanto a seção `nav` do Mkdocs_Config_File permanecer definida explicitamente.
11. THE Other_Plugins_Page SHALL estar escrita em português (pt-BR).

### Requirement 17: Build funcional do site de documentação com os capítulos do ecossistema de plugins

**User Story:** Como desenvolvedor do projeto, eu quero que as cinco novas páginas sejam integradas à navegação e à configuração do site, para que o Documentation_Site continue sendo gerado sem erros após a adição do catálogo de extensões e plugins.

#### Acceptance Criteria

1. THE Docs_Directory SHALL conter um arquivo Markdown separado para cada uma das Ecosystem_Pages, nos caminhos `docs/imagens-recursos-visuais.md`, `docs/diagramas-arquitetura.md`, `docs/integracao-github.md`, `docs/extensoes-pymdownx.md` e `docs/outros-plugins.md`.
2. THE Mkdocs_Config_File SHALL definir a seção `nav` incluindo uma entrada para cada uma das Ecosystem_Pages.
3. THE Project_Manifest SHALL declarar todas as dependências Python correspondentes ao Glightbox_Plugin, ao Git_Revision_Date_Plugin, ao Macros_Plugin, ao Minify_Plugin, ao Awesome_Pages_Plugin e ao Exporter_Plugin.
4. WHEN o comando `mkdocs build` é executado na raiz do projeto, THE Documentation_Site SHALL ser gerado sem erros de configuração após a adição das Ecosystem_Pages e dos plugins e extensões descritos nos Requirements 12 a 16.
5. WHEN o Documentation_Site é gerado, THE Documentation_Site SHALL incluir uma página renderizada para cada uma das Ecosystem_Pages.

### Requirement 18: Exportação de páginas para PDF com mkdocs-exporter

**User Story:** Como leitor da documentação, eu quero que a página de outros plugins explique o Exporter_Plugin, para que eu saiba como exportar páginas do meu próprio site MkDocs para PDF reaproveitando o Playwright_Package já instalado no projeto.

#### Acceptance Criteria

1. THE Project_Manifest SHALL declarar o Exporter_Plugin como dependência do projeto.
2. THE Mkdocs_Config_File SHALL definir, na seção `plugins`, o Exporter_Plugin configurado com a opção `formats.pdf.enabled` igual a `true`.
3. THE Other_Plugins_Page SHALL explicar a finalidade do Exporter_Plugin como mecanismo de exportação de páginas do Documentation_Site para PDF através de um navegador headless.
4. THE Other_Plugins_Page SHALL explicar que o Exporter_Plugin reaproveita o Playwright_Package já instalado no projeto, o mesmo pacote utilizado pelo Preview_Script, para renderizar as páginas antes de gerar o PDF.
5. THE Other_Plugins_Page SHALL estar escrita em português (pt-BR).

### Requirement 19: Componentes restantes do catálogo de extensões pymdownx

**User Story:** Como leitor da documentação, eu quero que a Pymdown_Extensions_Page cubra as Reference_Extensions, as Text_Formatting_Extensions e a Arithmatex_Extension ainda não documentadas, para que eu conheça o catálogo completo de extensões `pymdown-extensions` e saiba quando aplicar cada uma em minha própria documentação técnica.

#### Acceptance Criteria

1. THE Mkdocs_Config_File SHALL definir, na seção `markdown_extensions`, as Reference_Extensions `abbr`, `def_list`, `footnotes` e `tables`.
2. THE Mkdocs_Config_File SHALL definir, na seção `markdown_extensions`, as Text_Formatting_Extensions `pymdownx.mark`, `pymdownx.caret`, `pymdownx.tilde`, `pymdownx.keys`, `pymdownx.critic`, `pymdownx.magiclink` e `pymdownx.smartsymbols`.
3. THE Mkdocs_Config_File SHALL definir, na seção `markdown_extensions`, a Arithmatex_Extension configurada com a opção `generic` igual a `true`.
4. THE Mkdocs_Config_File SHALL definir a opção `extra_javascript` apontando para os Mathjax_Frontend_Scripts necessários para renderizar as fórmulas produzidas pela Arithmatex_Extension.
5. THE Pymdown_Extensions_Page SHALL ser estendida com uma seção que explica a diferença entre caixas de nota/atenção, fornecidas pela extensão `admonition` e por `pymdownx.details` na variante colapsável, e âncoras de referência, fornecidas por `toc` configurada com `permalink` e pela extensão `footnotes`, esclarecendo que nem todas essas extensões pertencem ao namespace `pymdownx`.
6. THE Pymdown_Extensions_Page SHALL apresentar um exemplo real de cada uma das Reference_Extensions e de cada uma das Text_Formatting_Extensions, inserido de verdade no conteúdo da página.
7. THE Pymdown_Extensions_Page SHALL apresentar um exemplo real de fórmula matemática renderizada através da Arithmatex_Extension com os Mathjax_Frontend_Scripts configurados.
8. THE Pymdown_Extensions_Page SHALL apresentar um exemplo real de bloco de código com as opções `linenums` e `hl_lines` da extensão `pymdownx.highlight` já configurada, demonstrando numeração de linhas e destaque de linhas específicas.
9. THE Pymdown_Extensions_Page SHALL incluir uma observação orientando o leitor a não habilitar todas as extensões `pymdown-extensions` indiscriminadamente, recomendando iniciar por um conjunto essencial formado por `pymdownx.highlight`, `pymdownx.superfences`, `pymdownx.snippets`, `pymdownx.tabbed`, `pymdownx.details` e `pymdownx.tasklist`, e adicionar as demais extensões conforme a necessidade.
10. THE Pymdown_Extensions_Page SHALL estar escrita em português (pt-BR).

### Requirement 20: Modos claro/escuro detalhados e integração real com GitHub Actions

**User Story:** Como leitor da documentação, eu quero uma seção dedicada explicando o funcionamento dos modos claro e escuro do site e uma integração real e funcional com GitHub Actions e GitHub Pages, para que eu entenda em detalhe esse recurso de tema e consiga publicar minha própria documentação usando o repositório real do projeto.

#### Acceptance Criteria

1. THE Customization_Page SHALL conter uma seção dedicada explicando os modos claro e escuro do Documentation_Site, detalhando a detecção automática via `prefers-color-scheme`, o botão de alternância manual (`toggle`) e a persistência da escolha do visitante entre visitas através de armazenamento local do navegador.
2. THE Mkdocs_Config_File SHALL manter, na seção `theme.palette` referenciada por essa nova seção da Customization_Page, as duas variantes `media: "(prefers-color-scheme: light)"` e `media: "(prefers-color-scheme: dark)"` já definidas no Requirement 1.
3. THE Mkdocs_Config_File SHALL definir os campos `repo_url`, `repo_name` e `edit_uri` com os valores reais do Real_Repository_URL, substituindo o Repository_Placeholder_URL definido no Requirement 14.
4. THE GitHub_Actions_Workflow SHALL existir no caminho `.github/workflows/` do projeto.
5. THE GitHub_Actions_Workflow SHALL conter uma etapa que builda o Documentation_Site utilizando o gerenciador `uv`.
6. THE GitHub_Actions_Workflow SHALL conter as etapas `actions/upload-pages-artifact` e `actions/deploy-pages` para publicar o Documentation_Site no GitHub Pages.
7. THE GitHub_Actions_Workflow SHALL definir a etapa de checkout do repositório com a opção `fetch-depth: 0`.
8. THE GitHub_Actions_Workflow SHALL conter as etapas de instalação do Node.js, do TypeScript e do TypeDoc, e de geração dos arquivos de declaração (`.d.ts`) do TypeScript_Example_Package antes da etapa de build do Documentation_Site, necessárias para que o handler `typescript` do Mkdocstrings_Plugin funcione no ambiente de execução do GitHub Actions.
9. THE GitHub_Actions_Workflow SHALL conter uma etapa de instalação do navegador Chromium do Playwright_Package, necessária para o Exporter_Plugin durante o build do Documentation_Site.
10. THE GitHub_Integration_Page SHALL apresentar o conteúdo real do GitHub_Actions_Workflow, explicado passo a passo.
11. THE GitHub_Integration_Page SHALL explicar os passos de habilitação do GitHub Pages com a fonte "GitHub Actions" no repositório do Real_Repository_URL.
12. THE GitHub_Integration_Page SHALL explicar a configuração das permissões `pages: write` e `id-token: write` do GitHub_Actions_Workflow.
13. IF o repositório local do projeto não possuir um remote git configurado, THEN THE GitHub_Integration_Page SHALL indicar a adição do remote apontando para o Real_Repository_URL como uma etapa segura e reversível, distinta da decisão de realizar commit e push do código, que permanece a critério do leitor.
14. THE GitHub_Integration_Page SHALL estar escrita em português (pt-BR).
