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

## 4. Checklist com `pymdownx.tasklist`

A extensão `pymdownx.tasklist` transforma itens de lista Markdown escritos como `- [x]` ou `- [ ]` em caixas de marcação **de verdade** — não apenas o texto literal `[x]`/`[ ]`, mas um elemento HTML renderizado visualmente como uma caixa de seleção. `[x]` marca o item como concluído (caixa marcada) e `[ ]` (um espaço entre os colchetes) marca o item como pendente (caixa vazia).

Exemplo real, representando um checklist de progresso deste próprio tutorial:

- [x] Instalar o MkDocs e o tema Material
- [x] Configurar o `mkdocs.yml`
- [ ] Publicar o site no GitHub Pages

No `mkdocs.yml` deste projeto, `pymdownx.tasklist` está configurada com a opção `custom_checkbox: true`. Sem essa opção, a extensão renderizaria um `<input type="checkbox" disabled>` HTML comum — a caixa de marcação padrão do navegador, com a aparência do sistema operacional do leitor. Com `custom_checkbox: true`, o tema Material substitui essa caixa padrão pelos ícones customizados do próprio tema (um quadrado com marca de visto para itens concluídos, um quadrado vazio para pendentes), mantendo a aparência visual consistente com o restante do site, em vez de depender do estilo nativo de cada navegador/sistema operacional.

## 5. Seção expansível com `pymdownx.details`

A extensão `pymdownx.details` cria uma seção de conteúdo que começa **recolhida** (escondida) e só é revelada quando o leitor clica em seu título — equivalente ao elemento HTML `<details>`/`<summary>`, mas escrito em uma sintaxe parecida com a dos admonitions (as caixas de aviso `!!! nota`/`!!! atenção` já usadas em páginas anteriores deste tutorial).

A diferença de sintaxe entre as duas é um único caractere no marcador de abertura:

- `!!! tipo "Título"` (três pontos de exclamação) — usado pela extensão `admonition` — cria uma caixa de aviso **sempre visível**, com todo o conteúdo exposto desde o carregamento da página.
- `??? tipo "Título"` (três pontos de interrogação) — usado pela extensão `pymdownx.details` — cria a mesma caixa visualmente, mas **colapsada por padrão**: o leitor só vê o título até clicar nele para expandir o conteúdo.

Exemplo real:

??? note "Clique para expandir"
    Este conteúdo começa escondido e só aparece quando o leitor clica no título.

Esse comportamento é útil para conteúdo complementar ou opcional — como um trecho de log de erro, uma explicação mais longa para quem quiser se aprofundar, ou uma seção "veja também" — que não precisa competir por atenção com o conteúdo principal da página, mas que continua disponível a um clique de distância.

## 6. Emoji com `pymdownx.emoji`

A extensão `pymdownx.emoji` substitui códigos no formato `:nome-do-emoji:` pelo ícone correspondente, renderizado como imagem/SVG em vez de depender da fonte de emoji nativa do sistema operacional ou navegador do leitor. No `mkdocs.yml` deste projeto, ela está configurada com:

```yaml
markdown_extensions:
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg
```

- `emoji_index` aponta para o índice de nomes de emoji do [Twemoji](https://twemoji.twitter.com/) (o conjunto de emojis de código aberto originalmente criado pelo Twitter, distribuído junto com o tema Material), que é a tabela usada para traduzir um nome como `rocket` para o emoji correspondente.
- `emoji_generator` define que cada emoji encontrado é gerado como uma imagem SVG embutida na página, em vez de depender de uma fonte de emoji instalada no sistema do leitor — garantindo que o emoji tenha a mesma aparência em qualquer navegador ou sistema operacional.

Exemplo real:

:rocket: Documentação publicada com sucesso!

Nesse parágrafo, `:rocket:` foi substituído pelo ícone de um foguete no momento em que esta página foi processada pelo `mkdocs build`/`mkdocs serve` — o texto `:rocket:` em si não aparece na versão final renderizada do site.

## 7. Caixas de nota vs. âncoras de referência: nem tudo é pymdownx

Até aqui, boa parte das extensões desta página pertence ao namespace `pymdownx`. Mas nem todo recurso visual de "caixa" ou "âncora" vem desse namespace — vale esclarecer a origem de cada um antes de seguir para as próximas seções.

**Caixas de nota/atenção**: existem duas variantes.

- `admonition` (extensão nativa do Python-Markdown, já usada em páginas anteriores deste tutorial) cria caixas de aviso **sempre visíveis**, com a sintaxe `!!! tipo "Título"` (três pontos de exclamação).
- `pymdownx.details` (vista na seção 5 desta página) cria a mesma caixa visualmente, mas **colapsada por padrão**, com a sintaxe `??? tipo "Título"` (três pontos de interrogação) — o leitor só vê o título até clicar para expandir o conteúdo.

**Âncoras de referência**: também existem duas origens.

- `toc`, configurada neste projeto com `permalink: true` desde a Tarefa 1.1, adiciona um link-âncora clicável ao lado de cada título de seção, permitindo copiar um link direto para aquele ponto da página.
- `footnotes` (nova nesta seção, detalhada a seguir) adiciona notas de rodapé com uma âncora de ida-e-volta: um número sobrescrito no texto (`Texto[^1]`) que leva até a explicação no rodapé (`[^1]: Explicação`), e uma seta no próprio rodapé que leva de volta ao ponto de origem no texto.

Das quatro extensões citadas nesta seção, apenas `pymdownx.details` pertence de fato ao namespace `pymdownx`. `admonition`, `toc` e `footnotes` são extensões nativas do Python-Markdown, reaproveitadas pelo tema Material — não é porque uma extensão produz uma caixa ou um ícone que ela necessariamente vem do pacote `pymdown-extensions`.

## 8. Extensões de referência: `abbr`, `def_list`, `footnotes`, `tables`

Estas quatro extensões nativas do Python-Markdown cobrem necessidades comuns de documentação de referência: abreviações, listas de definição, notas de rodapé e tabelas.

### `abbr`

A extensão `abbr` permite definir uma abreviação uma única vez (em qualquer ponto do documento, geralmente ao final) e faz com que toda ocorrência dessa sigla no texto da página ganhe um tooltip explicativo ao passar o mouse por cima, sem precisar marcar cada ocorrência manualmente.

Este site usa HTML e CSS para estruturar e estilizar o conteúdo.

*[HTML]: HyperText Markup Language
*[CSS]: Cascading Style Sheets

### `def_list`

A extensão `def_list` cria listas de definição — um termo seguido de sua explicação, com a sintaxe `Termo` em uma linha e `:   Definição` (dois espaços após os dois-pontos) na linha seguinte:

MkDocs
:   Gerador de site estático a partir de arquivos Markdown.

Material
:   Tema visual para o MkDocs.

### `footnotes`

A extensão `footnotes` cria notas de rodapé com âncora de ida-e-volta: a marcação `[^1]` no meio do texto gera um número de referência sobrescrito e clicável, que leva até a explicação correspondente no final da página; e a explicação, por sua vez, traz uma seta que leva de volta ao ponto exato do texto onde a nota foi referenciada.

O MkDocs é escrito em Python[^1].

[^1]: Uma linguagem de programação de alto nível.

### `tables`

A extensão `tables` interpreta a sintaxe de tabelas do Markdown (linhas separadas por `|`, com uma linha de `---` definindo o cabeçalho) e a renderiza como uma tabela HTML:

| Extensão | Namespace |
|---|---|
| `abbr` | nativa |
| `pymdownx.mark` | `pymdownx` |

## 9. Extensões de formatação de texto: `mark`, `caret`, `tilde`, `keys`, `critic`, `magiclink`, `smartsymbols`

Estas sete extensões do pacote `pymdown-extensions` adicionam sintaxes curtas para formatações de texto que o Markdown puro não cobre.

### `pymdownx.mark`

Marca um trecho como destacado (equivalente ao elemento HTML `<mark>`), com a sintaxe `==texto==`:

Este é um ==texto destacado==.

### `pymdownx.caret`

A sintaxe `texto^sobrescrito^` cria um sobrescrito, útil para fórmulas como potências: H^2^O. A sintaxe `^^texto^^` (com os dois acentos circunflexos duplicados) cria sublinhado: ^^sublinhado^^.

### `pymdownx.tilde`

A sintaxe `~~texto~~` cria texto tachado: ~~texto tachado~~. A sintaxe `texto~subscrito~` cria subscrito, útil para fórmulas químicas: H~2~O.

### `pymdownx.keys`

A sintaxe `++tecla1+tecla2++` renderiza uma combinação de teclas como teclas de teclado estilizadas:

Pressione ++ctrl+shift+p++ para abrir a paleta de comandos.

### `pymdownx.critic`

Marca revisões de texto no estilo "controle de alterações": `{--texto removido--}` mostra o trecho removido (com um traço sobre o texto) e `{++texto adicionado++}` mostra o trecho inserido (sublinhado), ambos visíveis simultaneamente para fins de revisão:

O MkDocs {--era--}{++é++} fácil de usar.

### `pymdownx.magiclink`

Converte automaticamente qualquer URL solta no texto em um link clicável, sem a necessidade da sintaxe `[texto](url)`:

Veja mais em https://www.mkdocs.org.

### `pymdownx.smartsymbols`

Converte sequências específicas de caracteres digitados em símbolos tipográficos equivalentes. Por exemplo, `-->` é convertido em → e `(c)` é convertido em ©, como neste parágrafo de exemplo: o fluxo segue de A --> B, e o conteúdo é (c) deste projeto.

## 10. Numeração e destaque de linhas de código

As opções `linenums` e `hl_lines` fazem parte da configuração de `pymdownx.highlight` (já habilitada neste projeto desde a Tarefa 9.4) e funcionam em conjunto com `pymdownx.superfences`, podendo ser aplicadas a qualquer bloco de código cercado por três crases, indicando as opções entre aspas logo após o nome da linguagem:

```python linenums="1" hl_lines="2 4"
import pandas as pd

df = pd.read_csv("dados.csv")
print(df.head())
```

`linenums="1"` numera as linhas do bloco a partir de 1, exibindo a numeração à esquerda do código. `hl_lines="2 4"` destaca visualmente (com um fundo diferenciado) as linhas 2 e 4 do bloco — nesse exemplo, a linha da leitura do CSV e a linha do `print`.

## 11. Fórmulas matemáticas com Arithmatex

A extensão `pymdownx.arithmatex`, configurada neste projeto com `generic: true`, prepara o HTML de fórmulas escritas em LaTeX para que um motor de renderização matemática no navegador possa processá-las — mas **sozinha ela não renderiza nada visualmente**. É necessário também configurar a opção raiz `extra_javascript` apontando para esse motor de renderização, o que já foi feito neste projeto: `docs/javascripts/mathjax.js` (configuração customizada) somado ao script do CDN do MathJax 3 (ver `mkdocs.yml`). Sem esse segundo passo, o HTML preparado pelo Arithmatex ficaria pronto, mas nenhuma fórmula apareceria de fato na página.

Fórmula em bloco:

\[ \text{média} = \frac{\sum valores}{n} \]

Fórmula em linha, no meio de uma frase: a famosa equação \(E = mc^2\) relaciona massa e energia.

## 12. Quantas extensões habilitar?

!!! tip "Comece pequeno"
    Não habilite todas as extensões do pacote `pymdown-extensions` de uma vez só, mesmo que isso seja tecnicamente possível. Comece pelo conjunto essencial para documentação técnica — `pymdownx.highlight`, `pymdownx.superfences`, `pymdownx.snippets`, `pymdownx.tabbed`, `pymdownx.details` e `pymdownx.tasklist` — e adicione as demais (como as extensões de referência, as de formatação de texto e o Arithmatex, catalogadas nesta página) apenas quando a necessidade real aparecer no conteúdo sendo escrito. Isso mantém o `mkdocs.yml` organizado e evita acumular funcionalidades redundantes ou nunca utilizadas.
