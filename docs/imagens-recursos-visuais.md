# Imagens e recursos visuais

Até aqui, as imagens mencionadas neste tutorial — como o logo e o favicon em [Identidade visual](personalizacao.md) — foram tratadas de forma bem simples: apenas um caminho de arquivo apontado por uma chave do `mkdocs.yml`. Mas o ecossistema do [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) oferece recursos específicos para enriquecer a forma como imagens aparecem dentro do **conteúdo** das páginas Markdown.

Esta página cobre três formas de enriquecer imagens no Documentation_Site:

1. **Lightbox** com o plugin `mkdocs-glightbox`: zoom em tela cheia ao clicar em qualquer imagem.
2. **Legendas e alinhamento** com as extensões `attr_list` e `pymdownx.blocks.caption`.
3. **Otimização automática** de imagens com o recurso nativo `optimize` do tema Material.

## 1. Lightbox com `mkdocs-glightbox`

### Instalação

O plugin de lightbox não vem embutido no MkDocs nem no Material; é um pacote Python separado, instalado com:

```bash
uv add mkdocs-glightbox
```

### Configuração

Depois de instalado, basta registrá-lo na seção `plugins` do `mkdocs.yml`:

```yaml
plugins:
  - glightbox
```

Este projeto já tem exatamente essa entrada configurada (ver [Configuração do mkdocs.yml](configuracao-yaml.md)).

### O que o plugin faz

O `glightbox` atua no momento do `mkdocs build`: ele percorre o HTML gerado de **cada página** e envolve **toda imagem inserida via sintaxe Markdown** (`![alt](caminho)`) em um comportamento de lightbox — ou seja, ao clicar na imagem, ela se expande em uma camada de zoom sobre o restante da página, com suporte a navegação entre as imagens da mesma página e fechamento ao clicar fora ou pressionar <kbd>Esc</kbd>.

O ponto mais importante é que **isso acontece automaticamente para qualquer imagem Markdown**, sem exigir nenhuma marcação especial por imagem. Não é necessário envolver a imagem em um link, adicionar uma classe CSS ou qualquer atributo extra: basta que a imagem exista como `![alt](caminho)` em qualquer página do site, e o `glightbox` já cuida do resto durante o build.

!!! note "Logo e favicon DataRain"
    A pasta `docs/assets/` já contém o logo e o favicon do site, descritos em [Identidade visual](personalizacao.md). Eles são recursos do tema; ainda não há nesta página uma imagem de conteúdo para demonstrar o lightbox.

    O comportamento do `glightbox` pode ser descrito em prosa e através dos exemplos de sintaxe desta página. Assim que uma imagem de conteúdo for adicionada, o plugin aplicará o lightbox automaticamente.

### Comportamento esperado com uma imagem real

Suponha que, no futuro, um arquivo real seja salvo em `docs/assets/logo.png` e referenciado em uma página como:

```markdown
![Logo](assets/logo.png)
```

A partir do próximo `uv run mkdocs build` (ou recarregamento automático do `uv run mkdocs serve`), essa imagem passa a abrir em lightbox automaticamente ao ser clicada — sem nenhuma alteração adicional no Markdown e sem reconfigurar o plugin. O mesmo vale para qualquer outra imagem Markdown adicionada a qualquer página do tutorial, inclusive para as imagens de exemplo mencionadas apenas textualmente nas seções 2 e 3 abaixo.

## 2. Legendas e alinhamento com `attr_list` e `pymdownx.blocks.caption`

Duas extensões de Markdown já habilitadas neste projeto (ver `markdown_extensions` em [Configuração do mkdocs.yml](configuracao-yaml.md)) permitem controlar o tamanho, o alinhamento e a legenda de uma imagem diretamente no Markdown, sem recorrer a HTML bruto.

### `attr_list`: dimensionar e alinhar uma imagem

A extensão `attr_list` permite anexar atributos HTML — como `width`, `height`, `align` ou classes CSS — a praticamente qualquer elemento Markdown, escrevendo-os entre chaves `{: ... }` imediatamente após o elemento. Aplicada a uma imagem, a sintaxe é:

```markdown
![Diagrama de arquitetura](assets/logo.png){: width="300" align="right" }
```

Aqui:

- `![Diagrama de arquitetura](assets/logo.png)` é a sintaxe Markdown comum de imagem: o texto entre `[` e `]` é o texto alternativo (`alt`), e o texto entre `(` e `)` é o caminho do arquivo.
- `{: width="300" align="right" }` é o bloco de atributos do `attr_list`. Cada par `atributo="valor"` dentro das chaves é copiado para a tag `<img>` gerada. Neste exemplo, `width="300"` limita a largura da imagem a 300 pixels, e `align="right"` a alinha à direita do texto ao redor (fazendo o texto da página fluir ao lado dela, como em um documento tradicional).

O mesmo bloco de atributos funciona para qualquer outro elemento Markdown (parágrafos, cabeçalhos, links), não apenas imagens — mas aqui o uso mais comum é justamente controlar dimensão e alinhamento de imagens sem escrever HTML manualmente.

### `pymdownx.blocks.caption`: adicionar uma legenda

A extensão `pymdownx.blocks.caption` adiciona uma legenda visível abaixo de uma imagem (ou de outro bloco), usando a sintaxe de blocos `///` do pymdown-extensions:

```markdown
![Diagrama de arquitetura](assets/logo.png)
/// caption
Figura 1 — Diagrama de arquitetura do projeto.
///
```

A leitura dessa sintaxe é:

- A primeira linha é a imagem comum, exatamente como antes.
- O bloco que começa em `/// caption` e termina no `///` de fechamento é um **bloco pymdownx** do tipo `caption`. Na linha de abertura, o texto logo depois de `///` (`caption`) identifica o tipo de bloco; todo o texto entre essa linha e o `///` final é o conteúdo da legenda.
- No HTML gerado, o pymdownx.blocks.caption associa automaticamente essa legenda à imagem (ou bloco) imediatamente anterior, renderizando-a como um elemento `<figcaption>` — o equivalente semântico de uma legenda de figura em HTML.

As duas extensões podem ser combinadas na mesma imagem: primeiro o `attr_list` para controlar tamanho/alinhamento, depois o bloco `/// caption ... ///` para a legenda.

## 3. Otimização automática de imagens com `optimize`

Além do lightbox e das legendas, o Material for MkDocs oferece um plugin nativo chamado `optimize`, que **não precisa ser instalado separadamente** (já vem embutido no pacote `mkdocs-material`, já declarado no `pyproject.toml` deste projeto — ver [Instalação](instalacao.md)). Ele é habilitado apenas adicionando uma entrada em `plugins`:

```yaml
plugins:
  - optimize
```

Quando habilitado, o `optimize` processa automaticamente, durante o `mkdocs build`, todas as imagens referenciadas dentro de `docs/`: ele comprime o arquivo original e pode gerar variantes otimizadas (por exemplo, em formato `.webp`), reduzindo o tamanho final dos arquivos de imagem servidos pelo Documentation_Site — sem que o autor do conteúdo precise rodar nenhuma ferramenta externa de compressão de imagens antes de salvar o arquivo em `docs/assets/`.

Este projeto não habilita `optimize` no `mkdocs.yml` agora, porque — como explicado na seção 1 acima — ainda não há nenhuma imagem real em `docs/assets/` para otimizar. Fica registrado aqui como o próximo passo recomendado: assim que imagens reais (logo, favicon, diagramas, capturas de tela etc.) forem adicionadas ao projeto, basta acrescentar `optimize` à lista de `plugins` para que elas passem a ser comprimidas automaticamente a cada build, sem nenhum trabalho manual adicional.
