# Configuração do `mkdocs.yml`

O arquivo `mkdocs.yml`, na raiz do projeto, é o **arquivo de configuração central** do MkDocs. Nele você define o título do site, qual tema usar, quais plugins habilitar, quais extensões de Markdown ativar e qual é a estrutura do menu de navegação. É a partir dele que os comandos `mkdocs build` e `mkdocs serve` sabem exatamente como montar o site.

Esta página explica, em detalhes e passo a passo, as quatro seções principais do `mkdocs.yml` deste projeto: `nav`, `theme`, `plugins` e `markdown_extensions`. Todos os trechos de YAML mostrados abaixo foram copiados diretamente do `mkdocs.yml` real do projeto.

## `nav`: a estrutura de navegação do site

```yaml
nav:
  - Início: index.md
  - Instalação: instalacao.md
  - "Configuração do mkdocs.yml": configuracao-yaml.md
  - "Identidade visual": personalizacao.md
  - "Exemplos de código": exemplos-codigo.md
  - "Exemplos do notebook": exemplos-notebook.md
```

A seção `nav` define o **menu de navegação** (a barra lateral ou superior) do site gerado. É ela que determina quais páginas existem, em que ordem aparecem e com qual título são exibidas para quem está lendo a documentação.

Cada linha da lista segue o mesmo padrão: um mapeamento entre um **título exibido** no menu e o **caminho de um arquivo `.md`** dentro da pasta `docs/`. Por exemplo, a entrada:

```yaml
- "Configuração do mkdocs.yml": configuracao-yaml.md
```

diz ao MkDocs: "crie uma entrada no menu chamada *Configuração do mkdocs.yml* e, quando o leitor clicar nela, mostre o conteúdo do arquivo `docs/configuracao-yaml.md`". Os caminhos à direita (`index.md`, `instalacao.md`, `configuracao-yaml.md`, etc.) são sempre relativos à pasta configurada em `docs_dir` (neste projeto, a pasta `docs/`), nunca caminhos absolutos.

Alguns detalhes importantes sobre essa sintaxe:

- Quando o título não contém caracteres especiais (como `:` ou acentos problemáticos para o YAML), ele pode ser escrito sem aspas, como em `Início: index.md`.
- Quando o título contém um `:` no meio do texto (como em `"Configuração do mkdocs.yml"`), ele precisa ser colocado entre aspas, pois o `:` tem significado especial em YAML (separa chave e valor). Por isso `"Configuração do mkdocs.yml"` e `"Exemplos de código"` aparecem entre aspas no arquivo.
- A **ordem das entradas na lista define a ordem do menu**: neste projeto, o menu começa com Início → Instalação → Configuração do mkdocs.yml → Identidade visual → Exemplos de código → Exemplos do notebook.
- Cada arquivo referenciado em `nav` precisa realmente existir dentro de `docs/`. Se um caminho estiver errado ou o arquivo não existir, o `mkdocs build` falha (ou gera um aviso, dependendo do modo `--strict`).

## `theme`: a aparência visual do site

```yaml
theme:
  name: material
  logo: assets/logo.png
  favicon: assets/datarain-logo.ico
  font:
    text: Roboto
    code: Roboto Mono
  palette:
    - scheme: default
      primary: custom
      accent: custom
      toggle:
        icon: material/weather-sunny
        name: "Ativar modo escuro"
    - scheme: slate
      primary: custom
      accent: custom
      toggle:
        icon: material/weather-night
        name: "Ativar modo claro"
  features:
    - content.action.edit
    - content.action.view
    - navigation.instant
    - navigation.tabs
    - navigation.sections
    - navigation.top
    - navigation.footer
    - navigation.indexes
    - content.code.copy
    - content.code.annotate
    - content.tabs.link
    - search.suggest
    - search.highlight

extra_css:
  - stylesheets/extra.css
```

A seção `theme` define **qual tema visual** o MkDocs deve usar para renderizar o site e como esse tema deve se comportar. A chave `name: material` é a mais importante dela: diz ao MkDocs para usar o tema [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) em vez do tema padrão, mais simples, que vem embutido no MkDocs.

Por que usar o tema `material`? Alguns motivos práticos:

- Ele entrega, sem esforço extra, um layout moderno e responsivo (funciona bem tanto no computador quanto no celular).
- Já vem com suporte a modo claro/escuro, busca integrada com destaque dos termos encontrados, navegação em abas/seções e muitos outros recursos visuais.
- É o tema mais usado e mais documentado do ecossistema MkDocs, o que facilita encontrar exemplos e resolver dúvidas.

As demais chaves dentro de `theme` neste arquivo — `font`, `palette` e `logo`/`favicon` — controlam a aparência do site. As cores institucionais são definidas em `docs/stylesheets/extra.css`, carregado pela opção `extra_css` do `mkdocs.yml`. Esses detalhes estão documentados em [Identidade visual](personalizacao.md).

## `plugins`: funcionalidades adicionais do MkDocs

```yaml
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
        typescript:
          paths: [.]
```

A seção `plugins` é uma lista dos **plugins habilitados** no site. Cada plugin adiciona uma funcionalidade ao MkDocs que não existe no comportamento padrão da ferramenta. Este projeto habilita dois plugins: `search` e `mkdocstrings`.

### O plugin `search`

```yaml
plugins:
  - search
```

`search` é o plugin de **busca do site**. Ele é responsável por indexar o conteúdo de todas as páginas Markdown durante o build e gerar o índice de busca usado pela caixa de pesquisa que aparece no topo do site (fornecida pelo tema Material). É graças a esse plugin que um leitor consegue digitar um termo na busca e ser levado diretamente à página e à seção onde esse termo aparece, sem precisar navegar manualmente pelo menu.

### O plugin `mkdocstrings`

```yaml
- mkdocstrings:
    handlers:
      python:
        paths: [.]
        options:
          show_source: true
          show_root_heading: true
          docstring_style: google
      typescript:
        paths: [.]
```

`mkdocstrings` é o plugin responsável por **gerar documentação automaticamente a partir do código-fonte e das suas docstrings/comentários de documentação**, em vez de o autor precisar escrever manualmente, em Markdown, a assinatura e a descrição de cada função ou classe. Ele funciona através de *handlers*: cada handler sabe ler e documentar código de uma linguagem específica.

Este projeto configura dois handlers:

- **`python`**: lê código Python e extrai docstrings de funções, classes e módulos. É esse handler que permite, por exemplo, escrever `::: teste.calcular_media` em uma página Markdown (como é feito em [Exemplos de código](exemplos-codigo.md)) e ter a documentação daquela função gerada automaticamente a partir do seu docstring real.
- **`typescript`**: faz o mesmo processo, mas para código TypeScript, documentando funções/tipos a partir de comentários de documentação em arquivos `.ts`.

Dentro do handler `python`, três opções merecem destaque:

- **`paths: [.]`** — diz ao `mkdocstrings` para procurar os módulos Python **a partir da raiz do projeto** (representada por `.`). Isso é necessário porque, por padrão, o handler Python resolve módulos a partir do diretório em que o comando `mkdocs` é executado; adicionar `paths: [.]` torna essa resolução explícita e robusta, garantindo que o módulo `teste` (o arquivo `teste.py` na raiz do projeto) seja encontrado mesmo que o build seja disparado de um diretório diferente ou por alguma ferramenta que altere o diretório de trabalho atual.
- **`show_source: true`** — faz com que o código-fonte da função/classe documentada também seja exibido junto com a documentação gerada, não apenas o texto do docstring.
- **`docstring_style: google`** — informa ao `mkdocstrings` que os docstrings do projeto seguem o formato do [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) (com seções como `Args:`, `Returns:` e `Raises:`), para que ele saiba interpretar e formatar corretamente cada seção do docstring.

O handler `typescript` recebe apenas `paths: [.]`, pelo mesmo motivo do handler Python: garantir que os arquivos TypeScript do projeto sejam localizados a partir da raiz, independentemente de onde o comando de build é executado.

## `markdown_extensions`: recursos extras de renderização do Markdown

```yaml
markdown_extensions:
  - admonition
  - pymdownx.highlight
  - pymdownx.superfences
  - pymdownx.inlinehilite
  - toc:
      permalink: true
```

A seção `markdown_extensions` lista **extensões do Python-Markdown** (a biblioteca que o MkDocs usa para converter `.md` em HTML) que adicionam uma sintaxe ou um comportamento de renderização além do Markdown padrão. Sem essas extensões, vários recursos usados nas páginas deste tutorial (como caixas de aviso e blocos de código coloridos) simplesmente não funcionariam. Este projeto habilita cinco extensões:

- **`admonition`** — adiciona a sintaxe de *admonitions*, ou seja, caixas de aviso/nota/dica destacadas visualmente do restante do texto. Com essa extensão, um bloco como:

  ```markdown
  !!! note "Observação"
      Este é um texto de observação.
  ```

  é renderizado como uma caixa colorida e destacada, chamando a atenção do leitor para informações importantes, avisos ou dicas, em vez de aparecer apenas como um parágrafo comum.

- **`pymdownx.highlight`** — fornece o mecanismo de **destaque de sintaxe (syntax highlighting)** para blocos de código, colorindo palavras-chave, strings, comentários etc. de acordo com a linguagem do bloco (Python, YAML, Bash, etc.). Essa extensão não funciona isoladamente: ela é a base usada pela extensão `pymdownx.superfences` logo abaixo para efetivamente colorir o código exibido nas páginas.

- **`pymdownx.superfences`** — melhora os blocos de código delimitados por três crases (` ```python `, ` ```yaml `, ` ```bash `, etc.), permitindo que eles sejam renderizados com o destaque de sintaxe fornecido por `pymdownx.highlight` e também possibilitando blocos de código aninhados dentro de outros elementos (como dentro de uma *admonition*). Todos os blocos de código vistos nesta própria página de documentação (os trechos YAML acima, por exemplo) dependem dessa extensão para aparecer formatados e coloridos corretamente.

- **`pymdownx.inlinehilite`** — estende o destaque de sintaxe para **trechos de código em linha**, ou seja, pequenos pedaços de código citados no meio de uma frase usando crase simples, como `` `mkdocs build` ``. Sem essa extensão, apenas os blocos de código de múltiplas linhas (com três crases) receberiam destaque; com ela, até referências curtas a comandos ou nomes de função dentro de um parágrafo normal ficam estilizadas de forma consistente.

- **`toc` com `permalink: true`** — habilita e configura o **sumário automático (table of contents)** da página, gerado a partir dos títulos (`#`, `##`, `###`, etc.) usados no Markdown. A opção `permalink: true` adiciona, ao lado de cada título renderizado, um pequeno link-âncora clicável que aponta diretamente para aquela seção, permitindo compartilhar ou favoritar o link de uma seção específica da página (por exemplo, um link direto para a seção "`plugins`: funcionalidades adicionais do MkDocs" desta própria página).

## Resumo

| Seção | Para que serve | Página relacionada |
|---|---|---|
| `nav` | Define o menu de navegação, mapeando título → arquivo `.md` em `docs/` | — |
| `theme` | Define o tema visual (Material) e seus detalhes (fonte, paleta, logo, favicon) | [Identidade visual](personalizacao.md) |
| `plugins` | Habilita busca (`search`) e documentação automática de código (`mkdocstrings`, handlers `python` e `typescript`) | [Exemplos de código](exemplos-codigo.md) |
| `markdown_extensions` | Habilita recursos extras de Markdown: admonitions, destaque de sintaxe e sumário com links âncora | — |
