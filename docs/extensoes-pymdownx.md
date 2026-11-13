# Extensões pymdownx

## 1. Introdução

O pacote [`pymdown-extensions`](https://facelessuser.github.io/pymdown-extensions/) já está instalado neste projeto (ele foi adicionado ao `pyproject.toml` na Tarefa 9.1, para suportar a incorporação de arquivos via `pymdownx.snippets`, usada na página [Dockerfile e outras linguagens](dockerfile-outras-linguagens.md)). Esse pacote reúne um conjunto bem maior de extensões Markdown do que apenas `snippets` — a maioria delas pensada especificamente para documentação técnica e exemplos de código, que é exatamente o caso deste tutorial.

Esta página cataloga as **8 extensões `pymdownx` mais relevantes para código** usadas (ou disponíveis) neste projeto. Quatro delas já apareceram em páginas anteriores e são apenas revisadas rapidamente aqui, com um link de volta para onde foram detalhadas. As outras quatro — `pymdownx.tabbed`, `pymdownx.tasklist`, `pymdownx.details` e `pymdownx.emoji` — são o foco desta página, cada uma com um exemplo real, processado pelo MkDocs no momento do build (não apenas um trecho ilustrativo de Markdown).

## 2. As 8 extensões

| Extensão | Finalidade |
|---|---|
| `pymdownx.highlight` | Destaque de sintaxe (*syntax highlighting*) em blocos de código. |
| `pymdownx.superfences` | Blocos de código avançados, com suporte a aninhamento e a cercas customizadas (como os diagramas Mermaid). |
| `pymdownx.snippets` | Incorporação do conteúdo real de arquivos do projeto dentro de blocos de código, via `--8<--`. |
| `pymdownx.tabbed` | Abas para alternar entre conteúdos relacionados (ex.: o mesmo exemplo em linguagens diferentes). |
| `pymdownx.inlinehilite` | Destaque de sintaxe para código citado em linha, entre crase simples (`` `assim` ``). |
| `pymdownx.tasklist` | Checklists técnicos, com caixas de marcação renderizadas de verdade. |
| `pymdownx.details` | Seções expansíveis/colapsáveis. |
| `pymdownx.emoji` | Emojis e ícones. |

As quatro primeiras linhas da tabela já foram apresentadas em detalhe em páginas anteriores deste tutorial:

- `pymdownx.highlight` e `pymdownx.superfences` — introduzidas na página [Configuração do mkdocs.yml](configuracao-yaml.md) e usadas em praticamente todo bloco de código deste tutorial, incluindo o diagrama Mermaid da página [Diagramas e arquitetura](diagramas-arquitetura.md), que depende do `custom_fences` do `superfences`.
- `pymdownx.snippets` — detalhada em profundidade na página [Dockerfile e outras linguagens](dockerfile-outras-linguagens.md), incluindo a sintaxe `--8<--` e a opção `base_path: .`.
- `pymdownx.inlinehilite` — habilitada no `mkdocs.yml` desde a Tarefa 1.1 e usada implicitamente sempre que um nome de arquivo, comando ou identificador é citado entre crase simples ao longo deste tutorial (por exemplo, `mkdocs.yml` ou `calcular_media` em qualquer página).

As quatro seções seguintes cobrem as extensões restantes, cada uma com um exemplo real inserido nesta própria página.

### Código inline colorido com `pymdownx.inlinehilite`

Para destacar a sintaxe de um pequeno trecho de código dentro de uma frase, use `#!` seguido da linguagem dentro das crases. Por exemplo, `#!python print("Olá, mundo!")` renderiza o código Python com as mesmas cores de sintaxe dos blocos de código.

??? info "Ver o Markdown usado"
    ```markdown
    Código Python em uma frase: `#!python print("Olá, mundo!")`
    ```

## 3. Abas com `pymdownx.tabbed`

A extensão `pymdownx.tabbed` transforma uma sequência de blocos marcados com `=== "Título"` em abas clicáveis, todas visíveis na mesma área da página — o leitor alterna entre elas sem precisar rolar a página para comparar o conteúdo. Ela está configurada no `mkdocs.yml` com a opção `alternate_style: true`, que faz as abas usarem o estilo visual do tema Material (uma faixa de botões acima do conteúdo) em vez do estilo padrão da extensão.

A sintaxe é:

- cada aba começa com `=== "Título da aba"`, na margem esquerda da linha;
- o conteúdo da aba vem na(s) linha(s) seguinte(s), indentado com **4 espaços** — exatamente como um item de lista Markdown aninhado. Esse conteúdo pode ser qualquer Markdown válido, incluindo um bloco de código inteiro, como nos exemplos abaixo;
- uma linha em branco (sem indentação) separa uma aba da próxima.

Abaixo, um exemplo real com três abas, mostrando a mesma instrução ("Hello World") em três linguagens diferentes:

=== "Python"

    ```python
    print("Hello World")
    ```

=== "JavaScript"

    ```javascript
    console.log("Hello World");
    ```

=== "PowerShell"

    ```powershell
    Write-Host "Hello World"
    ```

??? info "Ver o Markdown usado"
    ````markdown
    === "Python"

        ```python
        print("Hello World")
        ```

    === "JavaScript"

        ```javascript
        console.log("Hello World");
        ```

    === "PowerShell"

        ```powershell
        Write-Host "Hello World"
        ```
    ````

## 4. Checklist com `pymdownx.tasklist`

A extensão `pymdownx.tasklist` transforma itens de lista Markdown escritos como `- [x]` ou `- [ ]` em caixas de marcação **de verdade** — não apenas o texto literal `[x]`/`[ ]`, mas um elemento HTML renderizado visualmente como uma caixa de seleção. `[x]` marca o item como concluído (caixa marcada) e `[ ]` (um espaço entre os colchetes) marca o item como pendente (caixa vazia).

Exemplo real, representando um checklist de progresso deste próprio tutorial:

- [x] Instalar o MkDocs e o tema Material
- [x] Configurar o `mkdocs.yml`
- [ ] Publicar o site no GitHub Pages

??? info "Ver o Markdown usado"
    ```markdown
    - [x] Instalar o MkDocs e o tema Material
    - [x] Configurar o `mkdocs.yml`
    - [ ] Publicar o site no GitHub Pages
    ```

No `mkdocs.yml` deste projeto, `pymdownx.tasklist` está configurada com a opção `custom_checkbox: true`. Sem essa opção, a extensão renderizaria um `<input type="checkbox" disabled>` HTML comum — a caixa de marcação padrão do navegador, com a aparência do sistema operacional do leitor. Com `custom_checkbox: true`, o tema Material substitui essa caixa padrão pelos ícones customizados do próprio tema (um quadrado com marca de visto para itens concluídos, um quadrado vazio para pendentes), mantendo a aparência visual consistente com o restante do site, em vez de depender do estilo nativo de cada navegador/sistema operacional.

## 5. Seção expansível com `pymdownx.details`

A extensão `pymdownx.details` cria uma seção de conteúdo que começa **recolhida** (escondida) e só é revelada quando o leitor clica em seu título — equivalente ao elemento HTML `<details>`/`<summary>`, mas escrito em uma sintaxe parecida com a dos admonitions (as caixas de aviso `!!! nota`/`!!! atenção` já usadas em páginas anteriores deste tutorial).

A diferença de sintaxe entre as duas é um único caractere no marcador de abertura:

- `!!! tipo "Título"` (três pontos de exclamação) — usado pela extensão `admonition` — cria uma caixa de aviso **sempre visível**, com todo o conteúdo exposto desde o carregamento da página.
- `??? tipo "Título"` (três pontos de interrogação) — usado pela extensão `pymdownx.details` — cria a mesma caixa visualmente, mas **colapsada por padrão**: o leitor só vê o título até clicar nele para expandir o conteúdo.

Exemplo real:

??? note "Clique para expandir"
    Este conteúdo começa escondido e só aparece quando o leitor clica no título.

??? info "Ver o Markdown usado"
    ```markdown
    ??? note "Clique para expandir"
        Este conteúdo começa escondido e só aparece quando o leitor clica no título.
    ```

Esse comportamento é útil para conteúdo complementar ou opcional — como um trecho de log de erro, uma explicação mais longa para quem quiser se aprofundar, ou uma seção "veja também" — que não precisa competir por atenção com o conteúdo principal da página, mas que continua disponível a um clique de distância.

## 6. Emoji com `pymdownx.emoji`

A extensão `pymdownx.emoji` substitui códigos no formato `:nome-do-emoji:` pelo ícone correspondente, renderizado como imagem/SVG em vez de depender da fonte de emoji nativa do sistema operacional ou navegador do leitor. No `mkdocs.yml` deste projeto, ela está configurada com:

??? info "Ver a configuração no mkdocs.yml"
    ````yaml
    markdown_extensions:
      - pymdownx.emoji:
          emoji_index: !!python/name:material.extensions.emoji.twemoji
          emoji_generator: !!python/name:material.extensions.emoji.to_svg
    ````

- `emoji_index` aponta para o índice de nomes de emoji do [Twemoji](https://twemoji.twitter.com/) (o conjunto de emojis de código aberto originalmente criado pelo Twitter, distribuído junto com o tema Material), que é a tabela usada para traduzir um nome como `rocket` para o emoji correspondente.
- `emoji_generator` define que cada emoji encontrado é gerado como uma imagem SVG embutida na página, em vez de depender de uma fonte de emoji instalada no sistema do leitor — garantindo que o emoji tenha a mesma aparência em qualquer navegador ou sistema operacional.

Exemplo real:

:rocket: Documentação publicada com sucesso!

??? info "Ver o Markdown usado"
    ```markdown
    :rocket: Documentação publicada com sucesso!
    ```

Nesse parágrafo, `:rocket:` foi substituído pelo ícone de um foguete no momento em que esta página foi processada pelo `mkdocs build`/`mkdocs serve` — o texto `:rocket:` em si não aparece na versão final renderizada do site.

## 7. Caixas de nota vs. âncoras de referência: nem tudo é pymdownx

Até aqui, boa parte das extensões desta página pertence ao namespace `pymdownx`. Mas nem todo recurso visual de "caixa" ou "âncora" vem desse namespace — vale esclarecer a origem de cada um antes de seguir para as próximas seções.

### Caixas de nota e aviso com `admonition`

A extensão nativa `admonition` cria caixas destacadas com `!!! tipo "Título"`. O tema Material escolhe automaticamente a cor e o ícone de acordo com o tipo; não é necessário inserir um emoji ou configurar o ícone manualmente. A sintaxe básica é:

Os tipos abaixo mostram as caixas visuais oferecidas pelo tema Material:

!!! note "Nota"
    Use para registrar contexto ou uma informação complementar.

!!! abstract "Resumo"
    Use para resumir uma seção ou apresentar uma visão geral.

!!! info "Informação"
    Use para apresentar informação neutra ou uma tarefa pendente.

!!! tip "Dica"
    Use para sugerir uma boa prática ou um atalho.

!!! success "Concluído"
    Use para indicar um resultado esperado ou uma etapa bem-sucedida.

!!! question "Pergunta"
    Use para destacar uma pergunta frequente ou uma resposta.

!!! warning "Atenção"
    Use para destacar uma condição que pode causar um problema.

!!! failure "Falha"
    Use para descrever uma operação que não foi concluída.

!!! danger "Perigo"
    Use para alertar sobre uma ação destrutiva ou uma falha grave.

!!! bug "Bug"
    Use para documentar um defeito conhecido.

!!! example "Exemplo"
    Use para introduzir um exemplo ou caso de uso.

!!! quote "Citação"
    Use para destacar uma citação.

Cada tipo seleciona um ícone e uma aparência. O texto entre aspas define o título, que pode ser escrito em português, e o conteúdo deve ficar indentado quatro espaços. Estes são os nomes dos tipos e seus aliases:

| Tipo visual | Tipos alternativos |
|---|---|
| `note` | — |
| `abstract` | `summary`, `tldr` |
| `info` | `todo` |
| `tip` | `hint`, `important` |
| `success` | `check`, `done` |
| `question` | `help`, `faq` |
| `warning` | `caution`, `attention` |
| `failure` | `fail`, `missing` |
| `danger` | `error` |
| `bug` | — |
| `example` | — |
| `quote` | — |

Os nomes da coluna **Tipos alternativos** podem ser usados no lugar do tipo visual e geram a mesma caixa e o mesmo ícone. Por exemplo, `!!! summary "Resumo"` equivale a `!!! abstract "Resumo"`.

O bloco abaixo mostra a escrita Markdown de cada caixa acima, inclusive como colocar um bloco de código dentro de uma admonition. As caixas recolhíveis (`???`) são demonstradas separadamente na seção de `pymdownx.details`.

??? info "Ver o Markdown usado para todas as caixas"
    ````markdown
    !!! note "Nota"
        Use para registrar contexto ou uma informação complementar.

    !!! abstract "Resumo"
        Use para resumir uma seção ou apresentar uma visão geral.

    !!! info "Informação"
        Use para apresentar informação neutra ou uma tarefa pendente.

    !!! tip "Dica"
        Use para sugerir uma boa prática ou um atalho.

    !!! success "Concluído"
        Use para indicar um resultado esperado ou uma etapa bem-sucedida.

    !!! question "Pergunta"
        Use para destacar uma pergunta frequente ou uma resposta.

    !!! warning "Atenção"
        Use para destacar uma condição que pode causar um problema.

    !!! failure "Falha"
        Use para descrever uma operação que não foi concluída.

    !!! danger "Perigo"
        Use para alertar sobre uma ação destrutiva ou uma falha grave.

    !!! bug "Bug"
        Use para documentar um defeito conhecido.

    !!! example "Exemplo"
        Use para introduzir um exemplo ou caso de uso.

    !!! quote "Citação"
        Use para destacar uma citação.

    !!! info "Comando de exemplo"
        ```bash
        uv run mkdocs build
        ```
    ````

**Caixas recolhíveis**: existe uma variante expansível, habilitada por `pymdownx.details`.

- `admonition` (extensão nativa do Python-Markdown) cria caixas sempre visíveis usando `!!! tipo "Título"`.
- `pymdownx.details` cria caixas recolhíveis usando `??? tipo "Título"`; o leitor clica no título para expandir o conteúdo.

Para iniciar a caixa recolhível já aberta, acrescente `+` ao marcador:

???+ tip "Aberta por padrão"
    O leitor pode recolher este conteúdo clicando no título.

??? info "Ver o Markdown usado para caixas recolhíveis"
    ````markdown
    ??? note "Começa recolhida"
        O leitor clica no título para ver este conteúdo.

    ???+ tip "Aberta por padrão"
        O leitor pode recolher este conteúdo clicando no título.
    ````

### Âncoras de seção com `toc`

A extensão `toc` gera IDs a partir dos títulos e, com `permalink: true`, mostra um ícone de link ao lado deles. Clique nesse ícone para copiar o endereço direto da seção. Também é possível criar um link para o título manualmente usando seu fragmento, como `#exemplo-de-ancora`.

O conteúdo-fonte necessário é o título em Markdown e a opção no `mkdocs.yml`:

#### Exemplo de âncora

[Ir para o exemplo](#exemplo-de-ancora)

??? info "Ver o Markdown e a configuração da âncora"
    ```markdown
    ## Exemplo de âncora

    <!-- Link para esse título dentro da mesma página -->
    [Ir para o exemplo](#exemplo-de-ancora)
    ```

??? info "Ver a configuração do permalink no mkdocs.yml"
    ```yaml
    markdown_extensions:
      - toc:
          permalink: true
    ```

Neste exemplo, o MkDocs cria o ID `exemplo-de-ancora` a partir do título; o ícone de permalink é gerado automaticamente.

### Notas de rodapé com `footnotes`

A extensão `footnotes` cria uma referência numerada no texto e a explicação correspondente no fim da página. O número leva à nota; a seta na nota leva de volta à frase original:

Este parágrafo contém uma nota de rodapé.[^ancora-exemplo]

??? info "Ver o Markdown usado para a nota de rodapé"
    ```markdown
    Este parágrafo contém uma nota de rodapé.[^ancora-exemplo]

    [^ancora-exemplo]: Esta é a explicação apresentada no rodapé.
    ```

[^ancora-exemplo]: Esta é a explicação apresentada no rodapé.

Para usar as âncoras do sumário ou as notas de rodapé, habilite as extensões no arquivo `mkdocs.yml`:

??? info "Ver a configuração do sumário e das notas de rodapé"
    ````yaml
    markdown_extensions:
      - toc:
          permalink: true
      - footnotes
    ````

`admonition`, `toc` e `footnotes` são extensões nativas do Python-Markdown; `pymdownx.details` vem do pacote `pymdown-extensions`. O fato de uma extensão produzir uma caixa ou um ícone não determina de qual pacote ela vem.

## 8. Extensões de referência: `abbr`, `def_list`, `footnotes`, `tables`, `md_in_html`

Estas extensões nativas do Python-Markdown cobrem necessidades comuns de documentação de referência: abreviações, listas de definição, notas de rodapé, tabelas e Markdown dentro de elementos HTML.

### `abbr`

A extensão `abbr` permite definir uma abreviação uma única vez (em qualquer ponto do documento, geralmente ao final) e faz com que toda ocorrência dessa sigla no texto da página ganhe um tooltip explicativo ao passar o mouse por cima, sem precisar marcar cada ocorrência manualmente.

Este site usa HTML e CSS para estruturar e estilizar o conteúdo.

??? info "Ver o Markdown usado para abreviações"
    ```markdown
    Este site usa HTML e CSS para estruturar e estilizar o conteúdo.

    *[HTML]: HyperText Markup Language
    *[CSS]: Cascading Style Sheets
    ```

*[HTML]: HyperText Markup Language
*[CSS]: Cascading Style Sheets

### `def_list`

A extensão `def_list` cria listas de definição — um termo seguido de sua explicação, com a sintaxe `Termo` em uma linha e `:   Definição` (dois espaços após os dois-pontos) na linha seguinte:

MkDocs
:   Gerador de site estático a partir de arquivos Markdown.

Material
:   Tema visual para o MkDocs.

??? info "Ver o Markdown usado para a lista de definições"
    ```markdown
    MkDocs
    :   Gerador de site estático a partir de arquivos Markdown.

    Material
    :   Tema visual para o MkDocs.
    ```

### `footnotes`

A extensão `footnotes` cria notas de rodapé com âncora de ida-e-volta: a marcação `[^1]` no meio do texto gera um número de referência sobrescrito e clicável, que leva até a explicação correspondente no final da página; e a explicação, por sua vez, traz uma seta que leva de volta ao ponto exato do texto onde a nota foi referenciada.

O MkDocs é escrito em Python[^1].

??? info "Ver o Markdown usado para a nota de rodapé"
    ```markdown
    O MkDocs é escrito em Python[^1].

    [^1]: Uma linguagem de programação de alto nível.
    ```

[^1]: Uma linguagem de programação de alto nível.

### `tables`

A extensão `tables` interpreta a sintaxe de tabelas do Markdown (linhas separadas por `|`, com uma linha de `---` definindo o cabeçalho) e a renderiza como uma tabela HTML:

| Extensão | Namespace |
|---|---|
| `abbr` | nativa |
| `pymdownx.mark` | `pymdownx` |

??? info "Ver o Markdown usado para a tabela"
    ````markdown
    | Extensão | Namespace |
    |---|---|
    | `abbr` | nativa |
    | `pymdownx.mark` | `pymdownx` |
    ````

### `md_in_html`

A extensão `md_in_html` permite que o Markdown seja processado dentro de um elemento HTML, desde que o elemento tenha o atributo `markdown="1"`. Isso é útil quando a estrutura HTML é necessária, mas o conteúdo deve continuar usando formatação Markdown:

Resultado renderizado:

<div markdown="1">

Este parágrafo dentro de HTML contém **negrito** e `código inline`.
</div>

??? info "Ver o Markdown usado dentro do HTML"
    ````markdown
    <div markdown="1">

    Este parágrafo dentro de HTML contém **negrito** e `código inline`.

    </div>
    ````

Sem o atributo `markdown="1"`, o conteúdo dentro do elemento HTML pode ser tratado como HTML bruto, sem a conversão da sintaxe Markdown.

## 9. Extensões de formatação de texto: `mark`, `caret`, `tilde`, `keys`, `critic`, `magiclink`, `smartsymbols`

Estas sete extensões do pacote `pymdown-extensions` adicionam sintaxes curtas para formatações de texto que o Markdown puro não cobre.

### `pymdownx.mark`

Marca um trecho como destacado (equivalente ao elemento HTML `<mark>`), com a sintaxe `==texto==`:

Este é um ==texto destacado==.

??? info "Ver o Markdown usado"
    ```markdown
    Este é um ==texto destacado==.
    ```

### `pymdownx.caret`

A sintaxe `texto^sobrescrito^` cria um sobrescrito, útil para fórmulas como potências: H^2^O. A sintaxe `^^texto^^` (com os dois acentos circunflexos duplicados) cria sublinhado: ^^sublinhado^^.

??? info "Ver o Markdown usado"
    ```markdown
    A água é H^2^O.
    Este texto está ^^sublinhado^^.
    ```

### `pymdownx.tilde`

A sintaxe `~~texto~~` cria texto tachado: ~~texto tachado~~. A sintaxe `texto~subscrito~` cria subscrito, útil para fórmulas químicas: H~2~O.

??? info "Ver o Markdown usado"
    ```markdown
    Este texto está ~~tachado~~.
    A fórmula da água é H~2~O.
    ```

### `pymdownx.keys`

A sintaxe `++tecla1+tecla2++` renderiza uma combinação de teclas como teclas de teclado estilizadas:

Pressione ++ctrl+shift+p++ para abrir a paleta de comandos.

??? info "Ver o Markdown usado"
    ```markdown
    Pressione ++ctrl+shift+p++ para abrir a paleta de comandos.
    ```

### `pymdownx.critic`

Marca revisões de texto no estilo "controle de alterações": `{--texto removido--}` mostra o trecho removido (com um traço sobre o texto) e `{++texto adicionado++}` mostra o trecho inserido (sublinhado), ambos visíveis simultaneamente para fins de revisão:

O MkDocs {--era--}{++é++} fácil de usar.

??? info "Ver o Markdown usado"
    ```markdown
    O MkDocs {--era--}{++é++} fácil de usar.
    ```

### `pymdownx.magiclink`

Converte automaticamente qualquer URL solta no texto em um link clicável, sem a necessidade da sintaxe `[texto](url)`:

Veja mais em https://www.mkdocs.org.

??? info "Ver o Markdown usado"
    ```markdown
    Veja mais em https://www.mkdocs.org.
    ```

### `pymdownx.smartsymbols`

Converte sequências específicas de caracteres digitados em símbolos tipográficos equivalentes. Por exemplo, `-->` é convertido em → e `(c)` é convertido em ©, como neste parágrafo de exemplo: o fluxo segue de A --> B, e o conteúdo é (c) deste projeto.

??? info "Ver o Markdown usado"
    ```markdown
    O fluxo segue de A --> B, e o conteúdo é (c) deste projeto.
    ```

## 10. Numeração e destaque de linhas de código

As opções `linenums` e `hl_lines` fazem parte da configuração de `pymdownx.highlight` (já habilitada neste projeto desde a Tarefa 9.4) e funcionam em conjunto com `pymdownx.superfences`, podendo ser aplicadas a qualquer bloco de código cercado por três crases, indicando as opções entre aspas logo após o nome da linguagem:

```python linenums="1" hl_lines="2 4"
import pandas as pd

df = pd.read_csv("dados.csv")
print(df.head())
```

??? info "Ver o Markdown usado com numeração e destaque"
    ````markdown
    ```python linenums="1" hl_lines="2 4"
    import pandas as pd

    df = pd.read_csv("dados.csv")
    print(df.head())
    ```
    ````

`linenums="1"` numera as linhas do bloco a partir de 1, exibindo a numeração à esquerda do código. `hl_lines="2 4"` destaca visualmente (com um fundo diferenciado) as linhas 2 e 4 do bloco — nesse exemplo, a linha da leitura do CSV e a linha do `print`.

## 11. Fórmulas matemáticas com Arithmatex

A extensão `pymdownx.arithmatex`, configurada neste projeto com `generic: true`, prepara o HTML de fórmulas escritas em LaTeX para que um motor de renderização matemática no navegador possa processá-las — mas **sozinha ela não renderiza nada visualmente**. É necessário também configurar a opção raiz `extra_javascript` apontando para esse motor de renderização, o que já foi feito neste projeto: `docs/javascripts/mathjax.js` (configuração customizada) somado ao script do CDN do MathJax 3 (ver `mkdocs.yml`). Sem esse segundo passo, o HTML preparado pelo Arithmatex ficaria pronto, mas nenhuma fórmula apareceria de fato na página.

Fórmula em bloco:

\[ \text{média} = \frac{\sum valores}{n} \]

Fórmula em linha, no meio de uma frase: a famosa equação \(E = mc^2\) relaciona massa e energia.

??? info "Ver o Markdown usado para as fórmulas"
    ````markdown
    Fórmula em bloco:

    \[ \text{média} = \frac{\sum valores}{n} \]

    Fórmula em linha: \(E = mc^2\).
    ````

## 12. Quantas extensões habilitar?

!!! tip "Comece pequeno"
    Não habilite todas as extensões do pacote `pymdown-extensions` de uma vez só, mesmo que isso seja tecnicamente possível. Comece pelo conjunto essencial para documentação técnica — `pymdownx.highlight`, `pymdownx.superfences`, `pymdownx.snippets`, `pymdownx.tabbed`, `pymdownx.details` e `pymdownx.tasklist` — e adicione as demais (como as extensões de referência, as de formatação de texto e o Arithmatex, catalogadas nesta página) apenas quando a necessidade real aparecer no conteúdo sendo escrito. Isso mantém o `mkdocs.yml` organizado e evita acumular funcionalidades redundantes ou nunca utilizadas.

Esta caixa também é um exemplo de `admonition`: `!!! tip "Título"` escolhe o tipo, e o tema Material adiciona o ícone correspondente. Veja a seção [Caixas de nota e aviso](#caixas-de-nota-e-aviso-com-admonition) para outros tipos e exemplos.
