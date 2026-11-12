# Arquivos Markdown e navegação

Este capítulo mostra como organizar os arquivos de conteúdo de um projeto MkDocs, escrever páginas com títulos, listas e links e controlar onde cada página aparece nos menus do site.

## Como organizar as pastas

O arquivo `mkdocs.yml` fica na raiz do repositório, e o conteúdo publicado fica dentro da pasta definida por `docs_dir`. Neste projeto, `docs_dir: docs`, então páginas, imagens e outros recursos do site devem ficar em `docs/` — não na raiz do repositório.

Atualmente, este projeto mantém os capítulos diretamente em `docs/` e separa os recursos estáticos em suas próprias pastas:

```text
projeto/
├── mkdocs.yml
└── docs/
    ├── index.md
    ├── instalacao.md
    ├── configuracao-yaml.md
    ├── markdown-e-navegacao.md
    └── assets/
        ├── logo.png
        └── exemplo.png
```

Use `docs/index.md` como página inicial. Para uma documentação pequena ou média, manter os Markdown diretamente em `docs/` é simples e funciona bem. Em projetos maiores, agrupe capítulos relacionados em subpastas e crie subpastas dentro de `assets/` para separar imagens, diagramas e outros recursos.

Os nomes de arquivos devem ser curtos e descritivos. Prefira letras minúsculas, hífens entre palavras e evite espaços, acentos e nomes genéricos como `pagina1.md`.

Cada arquivo `.md` dentro de `docs/` pode se tornar uma página do site, mas a localização física e a posição nos menus são coisas diferentes: pastas organizam os arquivos; a configuração `nav` determina a hierarquia exibida ao leitor.

Se a documentação crescer, uma estrutura alternativa pode separar os capítulos por assunto:

```text
docs/
├── index.md
└── guia/
    ├── index.md
    ├── instalacao.md
    └── configuracao.md
```

o caminho usado no `nav` para a página de instalação é `guia/instalacao.md`, relativo a `docs/`. Em links dentro de Markdown, o caminho é relativo ao arquivo atual: em `docs/guia/instalacao.md`, use `[Configuração](configuracao.md)` para apontar a `docs/guia/configuracao.md`. Para um recurso compartilhado em `docs/assets/imagens/exemplo.png`, o mesmo arquivo `instalacao.md` pode usar `![Exemplo](../assets/imagens/exemplo.png)`.

## Como escrever uma página

Markdown usa caracteres simples para indicar a estrutura do conteúdo. Um arquivo de página normalmente começa com um título principal e segue com subtítulos:

```markdown
# Instalação

Uma introdução breve sobre o objetivo desta página.

## Pré-requisitos

Confira os itens necessários antes de começar.

### Instalar as dependências

Siga as etapas na ordem indicada.
```

Use apenas um título de nível 1 (`#`) para o título principal. Organize os assuntos com `##` e detalhes relacionados com `###`; não pule níveis sem motivo. O MkDocs Material usa esses títulos para montar o sumário da página e, conforme o tamanho da tela e a configuração, exibi-lo na navegação lateral direita.

### Tópicos e passos

Use hífen para listas de tópicos e números para instruções que devem ser seguidas em ordem:

```markdown
## O que você vai precisar

- Python instalado
- A ferramenta `uv`

## Etapas

1. Abra o terminal na pasta do projeto.
2. Instale as dependências.
3. Inicie o servidor local.
```

### Links, código e imagens

Links internos apontam para outros arquivos Markdown. Blocos de código devem indicar a linguagem para que o tema aplique o realce de sintaxe:

Consulte também [Configuração](configuracao-yaml.md).

```bash
uv run mkdocs serve
```

Imagens e outros arquivos estáticos devem ficar dentro de `docs/`, por exemplo em `docs/assets/`. A partir de um Markdown localizado diretamente em `docs/`, uma imagem pode ser referenciada assim:

```markdown
![Descrição da imagem](assets/exemplo.png)
```

Escreva um texto alternativo (`alt`) que explique o conteúdo visual. Para exemplos de dimensionamento, legenda e ampliação de imagens, veja [Imagens e recursos visuais](imagens-recursos-visuais.md).

## Adicionar uma página à navegação

Criar um arquivo Markdown não garante que ele apareça no menu. Com um `nav` explícito, adicione o arquivo à lista no `mkdocs.yml`, usando um título para o menu e o caminho relativo a `docs/`:

```yaml
nav:
  - Início: index.md
  - Começar:
      - Instalação: instalacao.md
      - "Markdown e navegação": markdown-e-navegacao.md
      - Configuração: configuracao-yaml.md
      - Guia:
          - guia/index.md
          - Instalação detalhada: guia/instalacao.md
          - Configuração detalhada: guia/configuracao.md
```

A indentação define os níveis da hierarquia: `Começar` é uma seção e os itens indentados são suas páginas. Os títulos definem os rótulos que o leitor vê; eles não precisam ser iguais ao nome do arquivo. A ordem das entradas determina a ordem no menu.

Quando uma seção tem sua própria página de índice, como `guia/index.md`, colocá-la como primeiro item do grupo torna o título da seção um link para essa página. O recurso `navigation.indexes` já está habilitado neste projeto e permite esse comportamento. Cada arquivo listado precisa existir dentro de `docs/`.

Depois de editar o `nav`, confira se todos os caminhos existem e execute:

```bash
uv run mkdocs build --strict
```

Esse projeto mantém a navegação no `mkdocs.yml`. Se o `nav` explícito for removido, plugins como `awesome-pages` podem participar da descoberta e organização automática das páginas, mas essa é outra estratégia de configuração.

## Menu superior e navegação lateral

Neste projeto, `navigation.tabs` e o `nav` trabalham juntos:

- **Menu superior:** os itens de primeiro nível (`Início`, `Começar`, `Conteúdo`, `Ferramentas` e `GitHub`) aparecem como abas. Por isso, capítulos novos devem ser colocados dentro de um grupo existente, como `Começar`, para não criar uma aba adicional no cabeçalho.
- **Menu lateral esquerdo:** ao selecionar uma aba, as páginas e subseções listadas dentro daquele grupo são exibidas na navegação lateral. `navigation.sections` organiza os itens em seções; os rótulos e a ordem vêm do `nav`.
- **Sumário lateral direito:** é montado automaticamente a partir dos títulos da página. A extensão `toc` já está habilitada neste projeto, e `permalink: true` adiciona links diretos aos títulos. Não é preciso cadastrar cada título no `nav`.

O recurso Material `toc.integrate` pode mover os itens do sumário da página para a navegação lateral esquerda. Para usá-lo, inclua-o em `theme.features` no `mkdocs.yml`:

```yaml
theme:
  features:
    - navigation.tabs
    - navigation.sections
    - toc.integrate
```

Sem `toc.integrate`, mantenha o sumário independente na lateral direita, como no comportamento padrão do Material em telas largas. Em telas menores, o tema adapta os painéis de navegação ao espaço disponível.

!!! tip "Resumo da configuração"
    `nav` controla quais páginas e grupos aparecem na navegação; os títulos Markdown (`#`, `##`, `###`) controlam o sumário da página. O cabeçalho superior exibe os grupos de primeiro nível quando `navigation.tabs` está ativo.
